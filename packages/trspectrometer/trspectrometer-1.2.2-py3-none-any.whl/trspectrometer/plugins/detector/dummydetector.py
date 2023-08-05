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

from threading import Thread, Event
from time import sleep

import numpy as np
from scipy.stats import norm

import configuration as config
from . import Detector

class DummyDetector(Detector):
    """
    A dummy :data:`~trspectrometer.plugins.detector` class which simulates the presence of a real
    detector device.

    It is hard-coded to return 2048 pixels of data in a 400--800 nm range. When start acquisition of
    a fixed number of samples, adjacent spectra are slightly different so that change in absorption
    (ΔA) calculations produce some meaningful results.

    To use this detector driver class, ensure ``"detector"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.detector]]
        name = "Detector"
        class = "DummyDetector"
    
    Note that multiple detectors may be added, indicated by the double square brackets around the
    section header. Acquisition methods may then select which chopper entry to use.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: Description of the detector device.
        self.description = "Dummy Detector"

        # Wavelength axis
        self._wl = np.linspace(400.0, 800.0, 2048, dtype=np.float32)

        self._acq_thread = None
        self._acq_stop = Event()

    def get_pixel_wavelengths(self) -> np.typing.ArrayLike:
        return self._wl

    def start(self, n: int=0) -> None:
        # Stop any existing thread
        self.stop(wait=True)
        self._acq_thread = Thread(target=self._start_acq, args=(n,))
        self._acq_stop.clear()
        self._acq_thread.start()

    def stop(self, wait: bool=False) -> None:
        if self._acq_thread:
            self._acq_stop.set()
            if wait:
                self._acq_thread.join()

    def _start_acq(self, n):
        cycletime = 1.0/config.data["hardware"]["laser_reprate"]
        rng = np.random.default_rng()
        if n > 0:
            # Acquire n spectra as a block
            data = rng.logistic(loc=1000, scale=100, size=(n, 2048))
            np.clip(data, 0, 2**16, out=data).astype(np.uint16)
            spec = 1e7*norm.pdf(self._wl, loc=600.0, scale=100)
            data = np.add(data, spec)
            # Make every second spectrum slightly different so DeltaA calcs do something
            data[::2] += 1e5*norm.pdf(self._wl, loc=550.0, scale=40)
            data[::2] -= 5e4*norm.pdf(self._wl, loc=650.0, scale=25)
            sleep(n*cycletime)
            for cb in self._acquisition_callbacks.copy():
                cb(data)
        else:
            # Acquire spectra continuously
            while not self._acq_stop.is_set():
                data = rng.logistic(loc=1000, scale=100, size=(2048,))
                np.clip(data, 0, 2**16, out=data).astype(np.uint16)
                spec = 1e7*norm.pdf(self._wl, loc=600.0, scale=100)
                data = np.add(data, spec)
                for cb in self._spectrum_callbacks.copy():
                    cb(data)
                sleep(cycletime)
        self._acq_thread = None




