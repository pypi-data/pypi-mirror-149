# Copyright 2021 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from threading import Thread, Event
from time import sleep, monotonic
import warnings

import numpy as np

import configuration as config
from signalstorage import signals
import hardware as hw
import datastorage as ds
from utils import AcquisitionError, AcquisitionAbortedWarning, no_infs, status_message, si_unit_factor, now_string

from . import Acquisition

class TA_SweptAcquisition(Acquisition):
    """
    An transient absorption :data:`~trspectrometer.plugins.acquisition` method which uses a modern
    rapid-acquisition technique that obtains data by sweeping the delay stage while continuously
    acquiring spectra.

    So-called "rapid acquisition" methods rely on tight integration between the
    :data:`~trspectrometer.plugins.delay` and the :data:`~trspectrometer.plugins.interface`
    hardware. As with the traditional :data:`stepped acquisition
    <trspectrometer.plugins.acquisition.ta_stepped.TA_SteppedAcquisition>` method, the laser
    synchronisation pulses are sent to the :data:`~trspectrometer.plugins.interface`, which then
    generates trigger pulses for the :data:`detector <trspectrometer.plugins.detector>` device
    and the :data:`~trspectrometer.plugins.chopper`. However, in addition to the chopper's
    synchronisation output being fed back to an input on the interface, the raw delay position
    encoder (quadrature) signal is also tracked directly by the interface hardware. In this way, the
    interface knows both the chopper "on" or "off" state as well as the precise delay position on
    each and every triggering of the detector. The delay movement trigger signal is also sent to the
    interface, which it uses to know when to begin sending trigger pulses on to the detector.

    The stepped acquisition carefully positions the delay, waits for it to settle, starts the
    detector, and acquires data. In contrast, the swept acquisition starts the delay moving at a
    constant velocity and blindly triggers the detector. It then uses the arrays of chopper and
    delay position measurements received from the interface to sort the data out into appropriate
    time bins. The efficiency gain comes from the fact that the detector is almost always acquiring
    data and capturing every laser shot, while in the stepped acquisition method, many laser shots
    are lost during the time spent positioning the delay.

    An diagram illustrating the required connections between the interface and other hardware is
    below. An open-source design for an interface is documented `here
    <https://trs-interface.readthedocs.io>`__, which is supported using the
    :data:`~trspectrometer.plugins.interface.trsi.TRSI` interface driver class.

    .. code-block:: none
        
        +----+           +-----------+
        |    |           |           |<--- Laser Sync In
        |    |           |           |---> Chopper Sync Out
        | PC |<---USB--->| Interface |---> Detector Sync Out
        |    |           |           |<--- Chopper Sync In
        |    |           |           |<--- Delay Encoder In
        |    |           |           |<--- Delay Trigger In
        +----+           +-----------+   

    To use this acquisition method, ensure ``"acquisition"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.acquisition]]
        name = "Swept"
        class = "TA_SweptAcquisition"
        options = { max_acquisitions=50000 }

    Note that multiple acquisition methods may be added, indicated by the double square brackets
    around the section header.

    Configuration file options are:

    - ``delay_index`` is the index of the :data:`~trspectrometer.plugins.delay` device to use, where
      ``0`` (default) corresponds to the first ``[[hardware.delay]]`` entry defined in the
      configuration file.
    
    - ``chopper_index`` is the index of the :data:`~trspectrometer.plugins.chopper` device to use,
      where ``0`` (default) corresponds to the first ``[[hardware.chopper]]`` entry defined in the
      configuration file.

    - ``interface_index`` is the index of the :data:`~trspectrometer.plugins.interface` device to use,
      where ``0`` (default) corresponds to the first ``[[hardware.interface]]`` entry defined in the
      configuration file.

    - ``detector_index`` is the index of the :data:`~trspectrometer.plugins.detector` device to use,
      where ``0`` (default) corresponds to the first ``[[hardware.detector]]`` entry defined in the
      configuration file.

    - ``max_acquisitions`` determines the maximum number of laser shots allowed to be collected over
      a single sweep of the delay. A larger number allows for higher densities of time points over
      larger time windows, but at the expense of greater consumption of the computer's RAM. The
      default value of 50000 is somewhat conservative and may result in the desired data point
      density not being achieved. Increasing this value may be beneficial, but do so while
      monitoring the software's RAM usage, and ensure at least 1--2 GB are free at all times to
      retain good system performance.
    """
    
    def __init__(self,
                 delay_index:int=0,
                 chopper_index:int=0,
                 interface_index:int=0,
                 detector_index:int=0,
                 max_acquisitions:int=50000,
                 **kwargs):
        super().__init__(**kwargs)
        #: Description of the acquisition device.
        self.description = "Swept Acquisition"

        self._log = logging.getLogger(__name__)

        # Options passed in from configuration file
        try:
            self._delay_i = max(0, min(int(delay_index), len(hw.modules["delay"].devices) - 1))
        except:
            self._delay_i = 0
        if self._delay_i != delay_index:
            self._log.warning(f"Invalid parameter for delay_index={delay_index}, will use delay_index={self._delay_i}") 
        try:
            self._chopper_i = max(0, min(int(chopper_index), len(hw.modules["chopper"].devices) - 1))
        except:
            self._chopper_i = 0
        if self._chopper_i != chopper_index:
            self._log.warning(f"Invalid parameter for chopper_index={chopper_index}, will use chopper_index={self._chopper_i}")
        try:
            self._interface_i = max(0, min(int(interface_index), len(hw.modules["interface"].devices) - 1))
        except:
            self._interface_i = 0
        if self._interface_i != interface_index:
            self._log.warning(f"Invalid parameter for interface_index={interface_index}, will use interface_index={self._interface_i}")
        try:
            self._detector_i = max(0, min(int(detector_index), len(hw.modules["detector"].devices) - 1))
        except:
            self._detector_i = 0
        if self._detector_i != detector_index:
            self._log.warning(f"Invalid parameter for detector_index={detector_index}, will use detector_index={self._detector_i}")
        # Maximum number of acquisitions permitted for each sweep
        self._max_acquisitions = int(max_acquisitions)

        # References to hardware devices in use
        self._delay = None
        self._chopper = None
        self._interface = None
        self._detector = None

        self._acq_thread = None
        self._acq_stop = Event()

        if not self.is_initialised():
            self._log.warning("Required modules (delay with encoder functionality, chopper, interface, detector) are not yet initialised.")


    def is_initialised(self):
        try:
            return (hw.modules["delay"].devices[self._delay_i].is_initialised() and
                    (hw.modules["delay"].devices[self._delay_i].get_encoder_count() is not None) and
                    hw.modules["chopper"].devices[self._chopper_i].is_initialised() and
                    hw.modules["interface"].devices[self._interface_i].is_initialised() and
                    hw.modules["detector"].devices[self._detector_i].is_initialised())
        except:
            return False
    
    
    def start(self) -> None:
        """
        Begin acquisition of data.
        """
        
        if not self.is_initialised():
            raise RuntimeError("Acquisition method not initialised (missing required hardware?)")
        try:
            self._delay = hw.modules["delay"].devices[self._delay_i]
            self._chopper = hw.modules["chopper"].devices[self._chopper_i]
            self._interface = hw.modules["interface"].devices[self._interface_i]
            self._detector = hw.modules["detector"].devices[self._detector_i]
        except:
            raise RuntimeError("Acquisition method failed to connect to required hardware.")
        msg = "Starting acquisition."
        self._log.info(msg)
        status_message(msg)
        
        # Get parameters from user interface selections
        _, data_density, t_start, steps, metadata = config.mainwindow.dataPanel.get_acquisition_params()

        # Generate time axis points from step list
        times = [0.0]
        for row in steps:
            for _ in range(row[0]):
                times.append(times[-1] + row[1])
        times = np.array(times, dtype=np.float32)
        # SI scaling factor for time unit (to seconds)
        si_f = si_unit_factor(ds.d["raw/time"].attrs["units"])
        # Crop times to those possible for the delay stage
        times = times[(self._delay.min_delay()/si_f <= t_start + times) & (t_start + times <= self._delay.max_delay()/si_f)]

        # Get wavelength axis points from detector
        wls = self._detector.get_pixel_wavelengths()

        # Create new zarr data structure for storing data
        ds.new_zarr()
        ds.d.create_group("raw")
        ds.d["raw"].array("wavelength", data=wls)
        ds.d["raw"].array("time", data=times)
        # No need to allocate space now, we can append scans as they come
        ds.d["raw"].zeros("data", shape=(0, times.shape[0], wls.shape[0]), dtype=np.float32)
        ds.d["raw"].zeros("data_density", shape=(0, times.shape[0]), dtype=np.uint32)
        ds.d["raw/wavelength"].attrs["units"] = config.data["rawdata"]["units"]["wavelength"]
        ds.d["raw/time"].attrs["units"] = config.data["rawdata"]["units"]["time"]
        ds.d["raw/data"].attrs["units"] = config.data["rawdata"]["units"]["data"]
        # Tuple of scan start and stop times
        ds.d["raw/data"].attrs["start_stop_times"] = []

        # Add metadata fields to the zarr storage
        ds.d["raw"].attrs["acquisition_method"] = self.name
        ds.d["raw"].attrs.update(metadata)
        ds.d["raw"].attrs["config"] = config.data.copy()

        # Notify that the data structures have changed
        signals.data_changed.emit(False)  # Don't update UI

        # Start up the acquisition thread
        self._acq_thread = Thread(name="Acquisition", target=self._start_acq, kwargs={
            "t_start": t_start,
            "data_density": data_density,
            "step_list": steps,
            "max_acquisitions": self._max_acquisitions,
            "laser_reprate": config.data["hardware"]["laser_reprate"]}
        )
        self._acq_stop.clear()
        self._acq_thread.start()

    def _start_acq(self, t_start=0.0, scan_count=None, data_density=250, step_list=None, laser_reprate=1000, max_acquisitions=50000):
        """Background thread to perform the data acquisition."""

        # We should catch any error that may occur in this background thread
        try:
            self._delay.stop()

            # TODO: Configure hardware better, using config parameters etc
            self._chopper.set_enabled(False)
            self._chopper.set_frequency(None)
            self._chopper.set_divider(1)
            self._chopper.set_enabled(True)

            # Wait for the chopper to spin up            
            msg = "Waiting for chopper to spin up."
            self._log.info(msg)
            status_message(msg)
            start_time = monotonic()
            while monotonic() < start_time + 5.0:
                if self._acq_stop.is_set():
                    raise AcquisitionAbortedWarning()
                sleep(0.1)

            # TODO: detector configuration? Can we assume this is set up already?
            self._detector.set_triggermode("External")
            self._detector.set_exposure(0.00005)
            # Ensure interface and delay quadrature encoder counts are synced up
            self._interface.set_encoder_count(self._delay.get_encoder_count())

            # Time and wavelength axes (force use of RAM, don't rely on zarr/disk)
            t = ds.d["raw/time"][:]
            wl = ds.d["raw/wavelength"][:]
            # SI scaling factor for time unit (to seconds)
            si_f = si_unit_factor(ds.d["raw/time"].attrs["units"])

            # Make a list of start and end time indices for each sweep range from the step list
            if step_list is None:
                sweep_ranges = [(0, t.shape[0] - 1)]
            else:
                sweep_ranges = []
                last_range_edge = 0
                for row in step_list:
                    this_range_edge = last_range_edge + row[0]
                    # Ensure we don't exceed the limits of delay hardware
                    # (time point list should already be truncated, but not steplist)
                    if this_range_edge >= t.shape[0]:
                        sweep_ranges.append((last_range_edge, t.shape[0] - 1))
                        break
                    sweep_ranges.append((last_range_edge, this_range_edge))
                    last_range_edge = this_range_edge
                sweep_ranges = np.array(sweep_ranges)

            # Determine the bins used to place data on the correct time grid
            # Partitions equidistant between time points, though note time points are not centred on each bin
            partitions = np.diff(t, prepend=t[0], append=t[-1])/2
            partitions[1:] += t
            partitions[0] += (partitions[0] - partitions[1])
            partitions[-1] += (partitions[-1] - partitions[-2])
            # Calculate radius (width/2) of each bin which will be centred on the time point
            bin_radii = [ min(v - partitions[i], partitions[i+1] - v) for i, v in enumerate(t) ]
          
            # Storage for delay and chopper state data received from the interface
            interface_done = Event()
            global delay_positions, chopper_states
            delay_positions = np.zeros((0,), dtype=np.float64)
            chopper_states = np.zeros((0,), dtype=bool)

            # Storage for spectral data obtained from the detector
            detector_done = Event()
            global spectra
            spectra = np.zeros((0, 0))

            # Handle the detector data acquisition callback
            def _got_spectra(data):
                global spectra
                spectra = data
                detector_done.set()
            self._detector.register_acquisition_callback(_got_spectra)

            # Handle the interface acquisition completion callback
            def _got_interface_state(delay_pos, chop_state):
                global delay_positions, chopper_states
                delay_positions = self._delay.encoder_to_delay(delay_pos)/si_f - t_start
                chopper_states = chop_state
                # Stop the detector in case it didn't finish automatically
                self._detector.stop()
                interface_done.set()
            self._interface.register_data_callback(_got_interface_state)

            # Array index of currently acquiring scan
            s_i = 0
            # Loop through scans
            while s_i < (scan_count if scan_count else config.mainwindow.dataPanel.countSpinBox.value()):

                msg = f"Starting scan #{s_i + 1}."
                self._log.info(msg)
                status_message(msg)
                # Allocate temporary storage for the next scan's data
                data = np.zeros(shape=(t.shape[0], wl.shape[0]), dtype=np.float32)
                # Keep track of number of acquisitions at each time point
                density = np.zeros(shape=t.shape[0], dtype=np.uint32)
                # Start time of this scan
                start_time = now_string()

                acquisition_attempt_count = 0

                # Loop through the sweep ranges
                r_i = 0
                while r_i < sweep_ranges.shape[0]:

                    delay_target = max(self._delay.min_delay(), si_f*(t_start + t[sweep_ranges[r_i][0]]))
                    if abs(self._delay.get_target() - delay_target) > self._delay.min_increment():
                        # Move delay to the first required time point.
                        msg = f"Moving delay to start of sweep range {r_i + 1} = {t[sweep_ranges[r_i][0]]} {ds.d['raw/time'].attrs['units']}"
                        self._log.info(msg)
                        status_message(msg)
                        self._delay.stop()
                        self._delay.set_velocity(3e-9)      # 3ns/s
                        self._delay.set_acceleration(2e-8)  # 20ns/s/s
                        self._delay.set_delay(delay_target)
                        start_time = monotonic()
                        while self._delay.is_moving():
                            if self._acq_stop.is_set():
                                self._delay.stop()
                                raise AcquisitionAbortedWarning()
                            if monotonic() > (start_time + 30.0):
                                raise AcquisitionError("Timeout waiting for delay movement.")
                            sleep(0.1)
                    
                    # Choose number of spectra to acquire based on desired data density, limited by max acquisitions possible
                    spectra_count = min(2*data_density*(sweep_ranges[r_i][1] - sweep_ranges[r_i][0]), max_acquisitions)
                    # Set delay velocity according to sweep size, laser rep rate, required data density etc
                    self._delay.set_velocity(1.02*si_f*laser_reprate*(t[sweep_ranges[r_i][1]] - t[sweep_ranges[r_i][0]])/spectra_count)

                    # Acquire spectra and chopper state
                    msg = f"Acquiring {spectra_count} spectra to {t[sweep_ranges[r_i][1]]} {ds.d['raw/time'].attrs['units']}, density target {0.5*spectra_count/(sweep_ranges[r_i][1] - sweep_ranges[r_i][0]):0.0f} samples/step."
                    self._log.info(msg)
                    status_message(msg)
                    interface_done.clear()
                    detector_done.clear()
                    spectra = np.zeros((0, 0))
                    delay_positions = np.zeros((0,), dtype=np.float64)
                    chopper_states = np.zeros((0,), dtype=bool)
                    # Start detector
                    self._detector.start(max_acquisitions)
                    # Arm the interface which will then wait for the delay movement to trigger the detector shutter
                    self._interface.arm()
                    sleep(0.5)
                    # Move the delay to the last required time point.
                    self._delay.set_delay(min(self._delay.max_delay(), si_f*(t_start + t[sweep_ranges[r_i][1]])))

                    # Wait for acquisition to finish
                    start_time = monotonic()
                    acquisition_failure = False
                    while not (interface_done.is_set() and detector_done.is_set()):
                        if self._acq_stop.is_set():
                            self._interface.stop()
                            self._detector.stop()
                            self._delay.stop()
                            raise AcquisitionAbortedWarning()
                        if monotonic() > (start_time + spectra_count/laser_reprate + 10.0):
                            # Acquisition is taking longer than expected...
                            acquisition_failure = True
                            break
                        sleep(0.01)
                    if acquisition_failure:
                        # Count acquisition attempts
                        acquisition_attempt_count += 1
                        if acquisition_attempt_count >= 3:
                            # Too many retries have occurred
                            raise AcquisitionError(f"Failed to receive detector data after {acquisition_attempt_count} acquisition attempts.")
                        else:
                            # Retry acquisition at this time point
                            bad_devices = "detector" if not detector_done.is_set() else ""
                            bad_devices += " and " if (not detector_done.is_set()) and (not interface_done.is_set()) else ""
                            bad_devices += "interface" if not interface_done.is_set() else ""
                            msg = f"Timeout waiting for {bad_devices} data, will retry."
                            self._log.warning(msg)
                            status_message(msg)
                            self._interface.stop()
                            self._detector.stop()
                            self._delay.stop()
                            # Interface will return (possibly zero length) data once stopped, wait to receive that before continuing
                            sleep(1.0)
                            continue
                    else:
                        # Successful acquisition
                        acquisition_attempt_count = 0

                    if chopper_states.shape[0] > 0 and chopper_states.shape[0] == spectra.shape[0]:
                        # Acquired same number of chopper states and spectra... good
                        # Split into "chopper on" and "chopper off" sets
                        ons = spectra[chopper_states]
                        offs = spectra[~chopper_states]
                        delay_positions = delay_positions[chopper_states]
                        # Ideally, they should alternate between on and off, but not always true
                        n = min(ons.shape[0], offs.shape[0])
                        if n == 0:
                            # Something wrong with chopper, all on or all off
                            raise AcquisitionError("Interface didn't detect chopper movement (check connections?).")
                        msg = f"Computing ΔA using {n} spectra pairs."
                        self._log.info(msg)
                        status_message(msg)
                        # Compute DeltaA using adjacent "on" and "off" samples
                        ons = ons[:n]
                        offs = offs[:n]
                        delay_positions = delay_positions[:n]
                        with warnings.catch_warnings():
                            # Ignore divide-by zero when computing deltaA
                            warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide")
                            warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
                            deltaA = no_infs(-np.log10(no_infs(ons/offs)))
                        # Determine index of closest time point (p_i) for each data point (d_i)
                        for d_i, p_i in enumerate(np.searchsorted(partitions, delay_positions, side="right") - 1):
                            if (0 <= p_i < t.shape[0]) and (abs(t[p_i] - delay_positions[d_i]) <= bin_radii[p_i]):
                                data[p_i] += deltaA[d_i]
                                density[p_i] += 1
                    else:
                        if chopper_states.shape[0] == 0:
                            # Didn't receive any real data from the interface.
                            msg = "Did not receive any data from the interface, retrying acquisition."
                        else:
                            # We can't match up the chopper state to the spectra
                            # TODO: Implement time stamps on spectra and try to sort them out
                            msg = f"Acquisition produced {chopper_states.shape[0]} chopper values but {spectra.shape[0]} spectra, retrying acquisition."
                        self._log.warning(msg)
                        status_message(msg)
                        continue

                    # Increment sweep range index
                    r_i += 1

                # Average data points
                with warnings.catch_warnings():
                    # Ignore divide-by zero when computing average
                    warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide")
                    warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
                    data /= density[:,np.newaxis]
                no_infs(data, copy=False)
                msg = f"Completed scan #{s_i + 1}, storing data to disk."
                self._log.info(msg)
                status_message(msg)
                # Store scan data to the zarr array on disk
                ds.d["raw/data"].append(data[np.newaxis])
                ds.d["raw/data_density"].append(density[np.newaxis])
                # Record scan start and stop times
                # Not sure why an .append() to the zarr attributes doesn't work directly...?
                #ds.d["raw/data"].attrs["start_stop_times"].append([start_time, now_string()])
                sst = ds.d["raw/data"].attrs["start_stop_times"]
                sst.append([start_time, now_string()])
                ds.d["raw/data"].attrs["start_stop_times"] = sst

                # Trigger the data update signal
                signals.raw_data_updated.emit([s_i], sweep_ranges[:,0], None)

                # Increment scan index
                s_i += 1
        
        except Exception as ex:
            # Handle any errors which occurred during acquisition
            self._log.error(f"{ex}")
            error = ex
        else:
            # Looks like it went OK
            error = None
 
        # Clean up and notify about acquisition completion
        # Be careful cleaning up, as we don't want to raise any exceptions within this thread
        self._acq_stop.set()    
        # It's possible that these callback functions haven't been defined if an error occurs early
        try:
            self._detector.unregister_acquisition_callback(_got_spectra)
        except: pass
        try:
            self._interface.unregister_data_callback(_got_interface_state)
        except: pass
        try:
            self._detector.stop()
        except:
            self._log.warning("Error stopping Detector.")
        try:
            self._interface.stop()
        except:
            self._log.warning("Error stopping Interface.")
        try:
            self._chopper.set_enabled(False)
        except:
            self._log.warning("Error stopping Chopper.")

        self._log.info("Stopped acquisition.")
        signals.acquisition_stopped.emit(error)
        self._acq_thread = None

            
    def stop(self) -> None:
        """
        Abort the acquisition of data.
        """
        self._acq_stop.set()


