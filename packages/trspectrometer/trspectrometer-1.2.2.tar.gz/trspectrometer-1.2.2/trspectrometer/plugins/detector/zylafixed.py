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

from time import monotonic, sleep

import numpy as np
from scipy.stats import norm
import andor3

from . import Detector

class ZylaFixed(Detector):
    """
    A class for a :data:`~trspectrometer.plugins.detector` built from an Andor Zyla sCMOS camera
    attached to a fixed-range spectrograph.

    Support is provided by the `andor3 python package <https://andor3.readthedocs.io>`__

    To use this detector driver class, ensure ``"detector"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.detector]]
        name = "Detector"
        class = "ZylaFixed"
        options = { calibration_coeffs=[431.34, 1.73637103e-01], flip_data=true }

    Note that multiple detectors may be added, indicated by the double square brackets around the
    section header. The same class type may be initialised multiple times with different values for
    its options. Acquisition methods may then select which chopper entry to use.

    Configuration file options are:

    - ``device_index`` is the index for the camera device as used by the Andor SDK3. A value of 0
      (default) uses the first detected device.

    - ``calibration_coeffs`` is an array of polynomial coefficients used to assign wavelength values
      to each of the detector pixels. The wavelengths for the :math:`x` pixels are determined from
      the :math:`n` coefficients, :math:`c_n`, by :math:`\lambda_x = \sum_n c_n x^{(n-1)}`.
    
    - ``flip_data`` may be needed so that the pixel wavelength values are monotonically increasing.
      That is, the pixel wavelengths calculated by the ``calibration_coeffs`` must range from
      shortest wavelength to largest. If the data received by the camera is opposite to that, use
      ``flip_data=true``, which will flip the image data received from the camera.
    """
    
    def __init__(self, device_index=0, calibration_coeffs=[431.34, 1.73637103e-01], flip_data=True, **kwargs):
        super().__init__(**kwargs)
        #: Description of the detector device.
        self.description = "Zyla"

        #: Reference to the Andor camera device. The device will be selected using the
        #: ``device_index`` if specified in the configuration file.
        self.cam = andor3.Andor3(device_index=device_index)
        self.cam.SensorCooling = True
        self.cam.FanSpeed = "On"
        self.cam.CycleMode = "Fixed"
        self.cam.AccumulateCount = 1
        self.cam.TriggerMode = "External"
        self.cam.ExposureTime = 0.00005
        self.cam.ElectronicShutteringMode = "Rolling"
        self.cam.SimplePreAmpGainControl = "16-bit (low noise & high well capacity)"
        self.cam.PixelReadoutRate = "280 MHz"
        self.cam.PixelEncoding = "Mono16"
        self.cam.SpuriousNoiseFilter = False
        self.cam.StaticBlemishCorrection = False
        self.cam.MetadataEnable = False
        # Capture only the middle pixels of the sensor for fastest readout
        self.cam.AOIHeight = 8
        self.cam.AOILeft = 1
        self.cam.AOIWidth = self.cam.max("AOIWidth")
        self.cam.VerticallyCentreAOI = True
        self.cam.FastAOIFrameRateEnable = True

        #: List of polynomial coefficients used to convert detector pixel numbers to wavelength.
        #: The wavelengths for the :math:`x` pixels are determined from the :math:`n` coefficients,
        #: :math:`c_n`, by :math:`\lambda_x = \sum_n c_n x^{(n-1)}`.
        #: The wavelength axis should be monotonically increasing (from lowest to highest wavelength).
        #: If the data array needs to be flipped to match, use the :data:`flip_data` option.
        self.calibration_coeffs = calibration_coeffs

        #: The wavelength axis should be increasing (from lowest to highest wavelength).
        #: If the data obtained from the detector runs from highest to lowest wavelength instead,
        #: setting this to ``True`` will flip the obtained data to correctly match the wavelength axis.
        self.flip_data:bool = flip_data

        # Reference to the Andor3 FrameServer which will do acquisition for us
        self._fsvr = None

    def get_triggermodes(self): # -> tuple[str]:
        feature = "TriggerMode"
        modes = []
        for i in range(self.cam.getEnumCount(feature)):
            if self.cam.isEnumIndexImplemented(feature, i) and self.cam.isEnumIndexAvailable(feature, i):
                modes.append(self.cam.getEnumStringByIndex(feature, i))
        return modes
    
    def set_triggermode(self, mode: str) -> None:
        self.cam.TriggerMode = mode

    def get_triggermode(self) -> str:
        return self.cam.TriggerMode[1]
    
    def get_exposure_limits(self): # -> tuple[float]:
        return (self.cam.min("ExposureTime"), self.cam.max("ExposureTime"))
    
    def get_exposure(self) -> float:
        return self.cam.ExposureTime
    
    def set_exposure(self, time: float) -> None:
        self.cam.ExposureTime = time

    def get_pixel_wavelengths(self) -> np.typing.ArrayLike:
        pixels = np.arange(self.cam.AOIWidth)
        wl = np.zeros(pixels.shape[0], dtype=np.float32)
        for n, c in enumerate(self.calibration_coeffs):
            wl += c*pixels**n
        return wl

    def get_max_value(self):
        return 2**16

    def start(self, n: int=0) -> None:
        # Stop any existing acquisition
        self.stop(wait=True)
        if n > 0:
            self._fsvr = andor3.FrameDump(self.cam, completion_callback=self._completion_handler, fvb=True)
            self._fsvr.start(n_images=n)
        else:
            self._fsvr = andor3.FrameServer(self.cam, frame_callback=self._frame_handler, fvb=True, frame_rate_max=30)
            self._fsvr.start()
        # Wait for the camera to begin acquiring before returning
        t_start = monotonic()
        while not self.cam.CameraAcquiring:
            sleep(0.05)
            if monotonic() > t_start + 3.0:
                raise RuntimeError("Andor camera failed to enter Acquiring state.")

    def _completion_handler(self, data, timestamps):
        """
        Handler for the FrameDump completion callback.
        """
        if self.flip_data:
            # Flip horizontally for to match the increasing wavelength
            data = data[:,::-1]
        # Notify our callbacks
        for cb in self._acquisition_callbacks.copy():
            cb(data)

    def _frame_handler(self, n, data, timestamp):
        """
        Handler for the FrameServer frame callback.
        """
        if self.flip_data:
            # Flip horizontally to match the increasing wavelength axis
            data = data[::-1]
        # Notify out callbacks
        for cb in self._spectrum_callbacks.copy():
            cb(data)

    def stop(self, wait: bool=False) -> None:
        if self._fsvr:
            self._fsvr.stop()




