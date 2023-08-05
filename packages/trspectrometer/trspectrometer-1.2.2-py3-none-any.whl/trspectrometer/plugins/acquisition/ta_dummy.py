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
from time import sleep

import numpy as np
from scipy.stats import norm

import configuration as config
from signalstorage import signals
import datastorage as ds
from utils import AcquisitionAbortedWarning, si_unit_factor, status_message, now_string

from . import Acquisition

class TA_DummySteppedAcquisition(Acquisition):
    """
    An :data:`~trspectrometer.plugins.acquisition.Acquisition` class which simulates the acquisition
    of transient absorption data using a stepped acquisition style, useful for demonstration or
    testing purposes. It does not require the presence of any other hardware devices.

    Time-zero is hard-coded to be at an absolute delay time of 50 ps, and the signal decay is
    dependent on the total size of the acquisition time window.

    To use this acquisition method, ensure ``"acquisition"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.acquisition]]
        name = "Dummy Stepped"
        class = "TA_DummySteppedAcquisition"
        options = {}

    Note that multiple acquisition methods may be added, indicated by the double square brackets
    around the section header.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: Description of the acquisition device.
        self.description = "Dummy Stepped Acquisition"

        self._log = logging.getLogger(__name__)

        self._acq_thread = None
        self._acq_stop = Event()


    def start(self) -> None:
        """
        Begin the (simulated) acquisition of data.
        """
        self._log.info("Starting acquisition.")
        
        # Get parameters from user interface selections
        _, _, t_start, steps, metadata = config.mainwindow.dataPanel.get_acquisition_params()

        # Generate time axis points from step list
        times = [0.0]
        for row in steps:
            for _ in range(row[0]):
                times.append(times[-1] + row[1])
        times = np.array(times, dtype=np.float32)
        # SI scaling factor for time unit (to seconds)
        si_f = si_unit_factor(ds.d["raw/time"].attrs["units"])
        
        # Make up some wavelength axis data
        wls = np.linspace(400.0, 800.0, num=2048, dtype=np.float32)

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
        # Tuple of scan start and stop times for each scan
        ds.d["raw/data"].attrs["start_stop_times"] = []

        # Add metadata fields to the zarr storage
        ds.d["raw"].attrs["acquisition_method"] = self.name
        ds.d["raw"].attrs.update(metadata)
        ds.d["raw"].attrs["config"] = config.data.copy()

        # Notify that the data structures have changed
        signals.data_changed.emit(False)  # Don't update UI

        # Start up the acquisition thread
        self._acq_thread = Thread(name="Acquisition", target=self._start_acq, kwargs={"t_start": t_start})
        self._acq_stop.clear()
        self._acq_thread.start()

    def _start_acq(self, t_start=0.0, scan_count=None):
        """
        Background thread to perform the data acquisition.
        """
        # We should catch errors that occur in this background thread
        try:
            rng = np.random.default_rng()

            # SI scaling factor for time unit (to seconds)
            si_f = si_unit_factor(ds.d["raw/time"].attrs["units"])

            # Array index of currently acquiring scan
            s_i = 0
            # Array index of currently acquiring time slice
            t_i = 0

            # Loop through scans
            while s_i < (scan_count if scan_count else config.mainwindow.dataPanel.countSpinBox.value()):
                
                # Allocate space for the next scan's data
                ds.d["raw/data"].append(np.full(shape=(1, ds.d["raw/time"].shape[0], ds.d["raw/wavelength"].shape[0]), fill_value=np.nan, dtype=np.float32))
                # Start time of this scan
                start_time = now_string()

                t_i = 0

                # Loop through times
                while t_i < ds.d["raw/time"].shape[0]:
                    if self._acq_stop.is_set():
                        raise AcquisitionAbortedWarning()
                    
                    status_message(f"Scan {s_i+1}, t = {ds.d['raw/time'][t_i]:0.2f} {ds.d['raw/time'].attrs['units']}")
 
                    # Simulate waiting for delay to be in position
                    sleep(0.1)
                    
                    # Generate some pretend spectra
                    t0 = 50.0
                    a1 = -0.5
                    tau1 = 0.1*ds.d["raw/time"][-1]
                    a2 = 1.0
                    tau2 = 0.3*ds.d["raw/time"][-1]
                    t = t_start + ds.d["raw/time"][t_i]
                    intensity1 = 0.0
                    intensity2 = 0.0
                    if t > t0:
                        intensity1 = a1*np.exp(-(t - t0)/tau1)
                        intensity2 = a2*np.exp(-(t - t0)/tau2)
                    dummydata = 5e-4*rng.logistic(size=ds.d["raw/wavelength"].shape[0])
                    dummydata += intensity1*norm.pdf(ds.d["raw/wavelength"], loc=500.0, scale=30)
                    dummydata += intensity2*norm.pdf(ds.d["raw/wavelength"], loc=650.0, scale=60)
                    ds.d["raw/data"][s_i,t_i] = dummydata
                    
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
        self._acq_stop.set()    
        self._log.info("Stopped acquisition.")
        signals.acquisition_stopped.emit(error)
        self._acq_thread = None

    def stop(self) -> None:
        self._acq_stop.set()
