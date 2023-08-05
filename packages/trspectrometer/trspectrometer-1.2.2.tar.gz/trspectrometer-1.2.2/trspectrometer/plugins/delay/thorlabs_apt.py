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

"""
:data:`~trspectrometer.plugins.delay.Delay` plugin classes for Thorlabs devices which communicate using
the APT protocol.

Support for the devices is provided by the `python thorlabs_apt_device
<https://thorlabs-apt-device.readthedocs.io>`__ library. See the documentation there and the official
`Thorlabs APT protocol documentation
<https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf>`__ for
information required to add support for a particular device.
"""

from time import sleep

import pluginlib
import thorlabs_apt_device

from . import Delay

class Thorlabs_BBD201_DDS600(Delay):
    """
    A :data:`~trspectrometer.plugins.delay` device built upon the Thorlabs BBD201 controller and
    DDS600 translation stage.

    To use this delay driver class, ensure ``"delay"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.delay]]
        name = "Delay"
        class = "Thorlabs_BBD201_DDS600"
        options = {calibration_slope=-6.6711140760507e-16, calibration_offset=8.00533689126084e-09}

    Note that multiple delays may be added, indicated by the double square brackets around the
    section header. Acquisition methods may then select which delay entry to use.

    The configuration file options are:

    - ``calibration_slope``, for the calibration curve slope, in seconds per encoder count.
    
    - ``calibration_offset``, for the calibration curve offset, in seconds.

    The method for converting between delay (in seconds) and device encoder counts is using a linear
    calibration curve of the form :math:`t = mx + z`, where :math:`t` is the delay time, :math:`m`
    is the calibration curve slope, :math:`x` is the device encoder count, and :math:`z` is the
    calibration curve offset. The calibration slope is specified in seconds per encoder count, and
    the offset in seconds.

    The BBD201 and DDS600 has 20000 encoder counts per millimetre, so the default value for the
    calibration slope is :math:`4/20000c`, where :math:`c` is the speed of light in millimetres per
    second, and the factor of 4 is due to there being four paths through the delay line (in and out,
    for each of the two passes through the delay line).

    Note that the default parameters assume two passes through the delay line. For a single pass,
    the ``calibration_slope`` should be divided by 2 accordingly. The defaults also use a
    "backwards" arrangement of the delay track, where smaller encoder counts equate to a longer
    delay time, as indicated by the negative value of ``calibration_slope``. For a "normal"
    arrangement, use a positive value of ``calibration_slope`` and set ``calibration_offset=0.0``.
    """
    
    # From the APT protocol document:
    # POSAPT = EncCnt * Pos
    # VELAPT = EncCnt * T * 65536 * Vel
    # ACCAPT = EncCnt * T^2 * 65536 * Acc
    # T = 102.4e-6
    # EncCnt per mm = 20000

    # Maximum delay 8.00533689126084e-09 s

    #: Encoder counts per millimeter for the DDS600 translation stage.
    counts_per_mm = 20000
    #: Time unit for velocity and acceleration for the BBD201 controller.
    time_unit = 102.4e-6

    def __init__(self, calibration_slope=-6.6711140760507e-16, calibration_offset=8.00533689126084e-09, **kwargs):
        super().__init__(**kwargs)

        #: Description of this delay device.
        self.description = "Thorlabs BBD201 + DDS600"

        #: Encoder counts to delay time calibration curve slope (linear factor), in seconds per count.
        #: The factor is for a single pass (in and out) of the delay. This will be multiplied by the
        #: number of passes to compute the actual delay value.
        self.calibration_slope = calibration_slope

        #: Encoder counts to delay time calibration curve offset (constant term), in seconds.
        self.calibration_offset = calibration_offset

        #: The :class:`thorlabs_apt_device.BBD201` controller for this device.
        self.bbd = thorlabs_apt_device.BBD201()
        self.bbd.set_trigger(output_logic="high", output_mode="in_motion")

        # Link status dictionary to that of the BBD, that's easy
        self.status = self.bbd.status

        # Initial target delay corresponding to home position
        self._target = self.encoder_to_delay(0)

        # Flag to indicate manual stop (target delay not reached)
        self._stopped = False

    def close(self) -> None:
        self.bbd.close()
        # Note that the bbd.close() returns before the port is actually closed
        # We can wait until the port actually closes, though this then blocks the GUI thread
        # Could wait up to 2 seconds as a compromise
        for _ in range(20):
            sleep(0.1)
            if self.bbd._port is None: break

    def min_delay(self) -> float:
        # Minimum delay time for the translation stage. Consider negative calibration slopes!
        return min(self.encoder_to_delay(0), self.encoder_to_delay(12000000))

    def max_delay(self) -> float:
        # Maximum delay time for the 600 mm translation stage. Consider negative calibration slopes!
        return max(self.encoder_to_delay(0), self.encoder_to_delay(12000000))

    def min_increment(self) -> float:
        # Minimum delay time increment is equal to one encoder count. Consider negative calibration slopes!
        return abs(self.encoder_to_delay(0) - self.encoder_to_delay(1))

    def get_delay(self) -> float:
        return self.encoder_to_delay(self.bbd.status["position"])
    
    def set_delay(self, delay_time:float) -> None:
        try:
            super().set_delay(delay_time)
            if self.is_moving():
                self.bbd.stop()
            self._stopped = False
            self.bbd.move_absolute(self.delay_to_encoder(delay_time))
        except RuntimeWarning:
            raise
    
    def home(self) -> None:
        if self.is_moving():
            self.bbd.stop()
        self._stopped = False
        self.bbd.home()
        # Update the status immediately, don't wait to receive a status update
        self.bbd.status["homing"] = True
    
    def stop(self) -> None:
        self.bbd.stop()
        self._stopped = True
    
    def get_velocity(self) -> float:
        """
        Get the programmed movement velocity of the translation stage, in delay/s.

        The value is technically unitless, but represents (delay seconds) per (wall clock seconds).

        Note that this is the velocity at which the translation stage is programmed to move at, not
        the current velocity. For getting the current velocity, use :data:`status["velocity"]`,
        though note that is in device-specific units.

        :returns: Maximum stage movement velocity, in delay/s.
        """
        return abs(self.encoder_to_delay(self.bbd.velparams['max_velocity']/(Thorlabs_BBD201_DDS600.time_unit*2**16)) - self.encoder_to_delay(0))
    
    def set_velocity(self, velocity:float) -> None:
        """
        Set the delay stage movement speed, in delay/s.

        The value is technically unitless, but represents (delay seconds) per (wall clock seconds).

        A typical value for ``velocity`` would be around 1.33e-9 (1.33 ns of delay per second),
        equivalent to 100 mm/s when two passes through the delay stage.

        :param velocity: Maximum velocity for translation stage movements, in delay/s.
        """
        v = abs(int(self.delay_to_encoder(velocity + self.encoder_to_delay(0))*(Thorlabs_BBD201_DDS600.time_unit*2**16)))
        self.bbd.set_velocity_params(acceleration=self.bbd.velparams["acceleration"], max_velocity=v)
        # Update the valparams immediately, don't wait to receive a status update
        # Otherwise, if set_acceleration() is used immediately it will not know of the new velocity
        self.bbd.velparams["max_velocity"] = v

    def get_acceleration(self) -> float:
        """
        Get the delay stage movement acceleration, in delay/s/s.

        The units represent (delay seconds) per (wall clock seconds squared).

        Note that this is the acceleration at which the translation stage is programmed to move at,
        not the current acceleration. For getting the current acceleration, use
        ``status["acceleration"]``, though note that is in device-specific units.

        :returns: Delay stage movement acceleration, in delay/s/s.
        """
        return abs(self.encoder_to_delay(self.bbd.velparams['acceleration']/((Thorlabs_BBD201_DDS600.time_unit**2)*(2**16))) - self.encoder_to_delay(0))
    
    def set_acceleration(self, acceleration:float) -> None:
        """
        Set the delay movement acceleration, in delay/s/s.

        The units represent (delay seconds) per (wall clock seconds squared).

        A typical value for ``acceleration`` would be around 1.33e-8 (13.33 ns of delay per second
        squared), equivalent to 1000 mm/s/s when two passes through the delay stage.

        :param acceleration: New delay stage movement acceleration, in delay/s/s.
        """
        a = abs(int(self.delay_to_encoder(acceleration + self.encoder_to_delay(0))*((Thorlabs_BBD201_DDS600.time_unit**2)*(2**16))))
        self.bbd.set_velocity_params(acceleration=a, max_velocity=self.bbd.velparams["max_velocity"])
        # Update the valparams immediately, don't wait to receive a status update
        # Otherwise, if set_velocity() is used immediately, it will not know of the new acceleration
        self.bbd.velparams["acceleration"] = a

    def is_initialised(self) -> bool:
        # TODO: Other means of detecting errors? What is motion_error value?
        return (self.bbd._port is not None) and (not self.bbd.status["motion_error"])

    def is_moving(self) -> bool:
        """
        Test whether the delay is currently moving into position.

        The delay is determined to be moving if it is in the process of a homing operation, or if
        the current delay does not match the requested target delay, within the tolerances of the
        minimum possible delay time increment given by :meth:`min_increment`.

        :returns: Boolean indicating whether the delay is currently moving.
        """
        # 5e-16 is approximately 2*eps for a float64
        return self.bbd.status["homing"] or ((not self._stopped) and (abs(self.get_delay() - self.get_target()) - self.min_increment() >= 5e-16))

    def get_encoder_count(self) -> int:
        """
        Retrieve the current position of the delay in raw encoder counts.

        If this functionality is not available, ``None`` will be returned.

        :returns: Position as raw encoder counts.
        """
        return self.bbd.status["position"]

    def encoder_to_delay(self, counts:int) -> float:
        """
        Convert from encoder counts to delay time using a basic model involving the hardware
        parameters, number of passes through the delay, and the speed of light.

        :param counts: Encoder counts.
        :returns: Delay time, in seconds.
        """
        # delay_time = (2*num_passes)*(1e-3*counts/counts_per_mm)/c
        return self.calibration_slope*counts + self.calibration_offset

    def delay_to_encoder(self, delay_time:float) -> int:
        """
        Convert from delay time to encoder counts using a basic model involving the hardware
        parameters, number of passes through the delay, and the speed of light.
        
        :param delay_time: Delay time, in seconds.
        :returns: Encoder counts.
        """
        return int((delay_time - self.calibration_offset)/self.calibration_slope)



