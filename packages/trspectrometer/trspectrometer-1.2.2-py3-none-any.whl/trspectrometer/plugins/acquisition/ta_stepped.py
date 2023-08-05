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
from utils import AcquisitionError, AcquisitionAbortedWarning, no_infs, si_unit_factor, status_message, now_string

from . import Acquisition


class TA_SteppedAcquisition(Acquisition):
    """
    An :data:`~trspectrometer.plugins.acquisition` method which obtains data by stepping the delay
    and acquiring spectra at each time point.


    An diagram illustrating the required connections between the interface and other hardware is
    below. An open-source design for an interface is documented `here
    <https://trs-interface.readthedocs.io>`__, which is supported using the
    :data:`~trspectrometer.plugins.interface.trsi.TRSI` interface driver class.

    .. code-block:: none
        
        +----+           +-----------+
        |    |           |           |<--- Laser Sync In
        | PC |<---USB--->| Interface |---> Chopper Sync Out
        |    |           |           |---> Detector Sync Out
        |    |           |           |<--- Chopper Sync In
        +----+           +-----------+   

    To use this acquisition method, ensure ``"acquisition"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.acquisition]]
        name = "Stepped"
        class = "TA_SteppedAcquisition"
        options = { averaging_method="mean of ratios", delay_move_timeout=20 }

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
    
    - ``averaging_method`` determines the way in which multiple samples will be averaged to compute DeltaA.

      - ``"mean of samples"`` will compute the mean of all "on" and all "off" samples, then compute DeltaA.
      
      - ``"mean of ratios"`` (default) will compute the mean of the adjacent "on" over "off" sample ratios, then compute DeltaA.

      - ``"mean of DeltaA"`` will compute DeltaA for adjacent "on" over "off" sample ratios, then take the mean.
      
    - ``delay_move_timeout`` time to allow for delay movement, in seconds. Default 20 s.
    """
    
    def __init__(self, 
                 delay_index:int=0,
                 chopper_index:int=0,
                 interface_index:int=0,
                 detector_index:int=0,
                 averaging_method:str="mean of ratios",
                 delay_move_timeout:float=20.0,
                 **kwargs):
        super().__init__(**kwargs)
        #: Description of the acquisition device.
        self.description = "Stepped Acquisition"

        self._log = logging.getLogger(__name__)

        # Options passed in from configuration file
        self._averaging_method = str(averaging_method)
        self._delay_move_timeout = float(delay_move_timeout)
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

        # References to hardware devices in use
        self._delay = None
        self._chopper = None
        self._interface = None
        self._detector = None

        self._acq_thread = None
        self._acq_stop = Event()

        if not self.is_initialised():
            self._log.warning("Required modules (delay, chopper, interface, detector) are not yet initialised.")


    def is_initialised(self):
        try:
            return (hw.modules["delay"].devices[self._delay_i].is_initialised() and
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
        self._log.info("Starting acquisition.")
        
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
        ds.d["raw"].full("data", np.nan, shape=(0, times.shape[0], wls.shape[0]), dtype=np.float32)
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
        self._acq_thread = Thread(name="Acquisition", target=self._start_acq, daemon=True, kwargs={
            "t_start": t_start,
            "data_density": data_density,
            "laser_reprate": config.data["hardware"]["laser_reprate"]}
        )
        self._acq_stop.clear()
        self._acq_thread.start()

    def _start_acq(self, t_start=0.0, scan_count=None, data_density=250, laser_reprate=1000):
        """Background thread to perform the data acquisition."""

        # We should catch any error that may occur in this background thread
        try:
            # TODO: Configure hardware better, using config parameters etc
            self._chopper.set_enabled(False)
            self._chopper.set_frequency(None)
            self._chopper.set_divider(1)
            self._chopper.set_enabled(True)
            
            # Wait for the chopper to spin up
            msg = "Waiting for chopper to spin up."
            self._log.info(msg)
            status_message(msg)
            clock = monotonic()
            while monotonic() < clock + 4.0:
                if self._acq_stop.is_set():
                    raise AcquisitionAbortedWarning()
                sleep(0.1)

            # Detector configuration
            self._detector.set_triggermode("External")
            self._detector.set_exposure(0.00005)
            
            # TODO: delay configuration?
            self._delay.set_velocity(2e-9)      # 2ns/s
            self._delay.set_acceleration(2e-8)  # 20ns/s/s

            # SI scaling factor for time unit (to seconds)
            si_f = si_unit_factor(ds.d["raw/time"].attrs["units"])

            # Array index of currently acquiring scan
            s_i = 0
            # Array index of currently acquiring time slice
            t_i = 0

            # Event for chopper state data received from the interface
            interface_done = Event()
            global chopper_state
            chopper_state = np.zeros((0,), dtype=bool)

            # Event for signal spectra obtained from the detector
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
            def _got_chopper_state(delay_pos, chop_state):
                global chopper_state
                chopper_state = chop_state
                interface_done.set()
            self._interface.register_data_callback(_got_chopper_state)

            # Loop through scans
            while s_i < (scan_count if scan_count else config.mainwindow.dataPanel.countSpinBox.value()):

                # Allocate space for the next scan's data
                ds.d["raw/data"].append(np.full(shape=(1, ds.d["raw/time"].shape[0], ds.d["raw/wavelength"].shape[0]), fill_value=np.nan, dtype=np.float32))
                # Start time of this scan
                start_time = now_string()
                t_i = 0
                
                # Loop through times and move the delay
                acquisition_attempt_count = 0
                while t_i < ds.d["raw/time"].shape[0]:
                    if self._acq_stop.is_set():
                        raise AcquisitionAbortedWarning()
                    
                    status_message(f"Scan {s_i+1}, t = {ds.d['raw/time'][t_i]:0.2f} {ds.d['raw/time'].attrs['units']}")

                    # Clear event signals and temporary storage for spectra and chopper state
                    interface_done.clear()
                    detector_done.clear()
                    chopper_state = np.zeros((0,), dtype=bool)
                    spectra = np.zeros((0, 0))
                    # Start detector, it will wait for external trigger pulses
                    self._detector.start(2*data_density)

                    # Move delay, wait for it to be in position
                    delay_move_attempt_max = 2
                    for delay_move_attempt in range(1, delay_move_attempt_max + 1):
                        self._delay.set_delay(si_f*(t_start + ds.d["raw/time"][t_i]))
                        clock = monotonic()
                        delay_move_failure = False
                        while self._delay.is_moving():
                            if self._acq_stop.is_set():
                                raise AcquisitionAbortedWarning()
                            if monotonic() > (clock + self._delay_move_timeout):
                                # Move didn't complete it time
                                delay_move_failure = True
                                break
                            sleep(0.1)
                        if delay_move_failure:
                            if delay_move_attempt < delay_move_attempt_max:
                                # Allow another retry
                                self._log.warning("Timeout waiting for delay movement, will retry.")
                            else:
                                # Second attempt, error out
                                raise AcquisitionError("Timeout waiting for delay movement.")
                        else:
                            # Move seems to have occurred OK
                            break
                    
                    # May need to wait a little for the detector to really be ready for trigger pulses,
                    # but waiting for the delay movement should be enough
                    # Manually trigger the interface which will then trigger the detector shutter
                    self._interface.start(2*data_density)

                    # Wait for acquisition to finish
                    clock = monotonic()
                    acquisition_failure = False
                    while not (interface_done.is_set() and detector_done.is_set()):
                        if self._acq_stop.is_set():
                            raise AcquisitionAbortedWarning()
                        if monotonic() > (clock + 5.0):
                            # TODO: Could decide on timeout value depending on number of samples and laser rep rate
                            acquisition_failure = True
                            break
                        sleep(0.1)
                    if acquisition_failure:
                        acquisition_attempt_count += 1
                        if acquisition_attempt_count >= 3:
                            # Too many retries have occurred
                            raise AcquisitionError(f"Failed to receive detector data after {acquisition_attempt_count} acquisition attempts.")
                        else:
                            # Retry acquisition at this time point
                            bad_devices = "detector" if not detector_done.is_set() else ""
                            bad_devices += " and " if (not detector_done.is_set()) and (not interface_done.is_set()) else ""
                            bad_devices += "interface" if not interface_done.is_set() else ""
                            msg = f"Timeout waiting for {bad_devices} data at scan={s_i+1} t={ds.d['raw/time'][t_i]}, will retry."
                            status_message(msg)
                            self._log.warning(msg)
                            self._interface.stop()
                            self._detector.stop()
                            self._delay.stop()
                            # Interface will return (possibly zero length) data once stopped, wait to receive that before continuing
                            sleep(1.0)
                            continue
                    else:
                        # Successful acquisition
                        acquisition_attempt_count = 0

                    if chopper_state.shape[0] > 0 and chopper_state.shape[0] == spectra.shape[0]:
                        # Acquired same number of chopper states and spectra... good
                        # Split into "chopper on" and "chopper off" sets
                        ons = spectra[chopper_state]
                        offs = spectra[~chopper_state]
                        # Ideally, they should alternate between on and off, but not always true
                        n = min(ons.shape[0], offs.shape[0])
                        if n == 0:
                            # Something wrong with chopper, all on or all off
                            raise AcquisitionError("Interface didn't detect chopper movement (check connections?).")
                        
                        # Compute DeltaA using method selected in configuration file
                        with warnings.catch_warnings():
                            # Ignore divide-by zero when computing deltaA
                            warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide")
                            warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
                            if self._averaging_method == "mean of samples":
                                # Average all "on" and all "off" samples, then compute DeltaA
                                ds.d["raw/data"][s_i,t_i] = no_infs(-np.log10(no_infs(np.nanmean(ons, axis=0, dtype=np.float32)/np.nanmean(offs, axis=0, dtype=np.float32))))
                            elif self._averaging_method == "mean of ratios":
                                # Compute ratio of adjacent "on" and "off" samples, then average the ratios
                                ons = ons[:n]
                                offs = offs[:n]
                                ds.d["raw/data"][s_i,t_i] = no_infs(-np.log10(np.nanmean(no_infs(ons/offs), axis=0, dtype=np.float32)))
                            else:
                                # Average DeltaA computed using adjacent "on" and "off" samples
                                ons = ons[:n]
                                offs = offs[:n]
                                ds.d["raw/data"][s_i,t_i] = np.nanmean(no_infs(-np.log10(no_infs(ons/offs))), axis=0, dtype=np.float32)
                    else:
                        # We can't match up the chopper state to the spectra
                        # TODO: Implement time stamps on spectra and try to sort them out
                        msg = f"Requested {2*data_density} spectra, received {chopper_state.shape[0]} chopper values and {spectra.shape[0]} spectra, retrying acquisition"
                        status_message(msg)
                        self._log.warning(msg)
                        continue

                    # Trigger the data update signal
                    signals.raw_data_updated.emit([s_i], [t_i], None)
                    
                    # Increment time index
                    t_i += 1

                # Record scan start and stop times
                # Not sure why an .append() to the zarr attributes doesn't work directly...?
                #ds.d["raw/data"].attrs["start_stop_times"].append([start_time, now_string()])
                sst = ds.d["raw/data"].attrs["start_stop_times"]
                sst.append([start_time, now_string()])
                ds.d["raw/data"].attrs["start_stop_times"] = sst

                # Increment scan index
                s_i += 1
        
        except Exception as ex:
            # Handle any errors which occurred during acquisition
            self._log.error(f"{ex}")
            error = ex
            # Record start and stop times of the partial scan
            sst = ds.d["raw/data"].attrs["start_stop_times"]
            sst.append([start_time, now_string()])
            ds.d["raw/data"].attrs["start_stop_times"] = sst
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
            self._interface.unregister_data_callback(_got_chopper_state)
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


