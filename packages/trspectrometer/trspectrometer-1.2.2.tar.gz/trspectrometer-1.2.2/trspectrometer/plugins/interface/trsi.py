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
from time import sleep

from trs_interface import TRSInterface

import hardware as hw
import configuration as config

from . import Interface

class TRSI(Interface):
    """
    An :data:`~trspectrometer.plugins.interface` class to connect to the TRS-Interface hardware.

    The TRS-Interface is open-source hardware documented at `<https://trs-interface.readthedocs.io>`__.

    Currently the interface requires knowledge of the laser repetition rate (in Hz) to be included
    in the ``laser_reprate`` entry under the ``[hardware]`` section of the :ref:`configuration
    file`. This may change in the future if another mechanism is implemented, eg if the interface is
    able to reliably detect the laser repetition rate and accept negative delay parameter values.

    To use this interface driver class, ensure ``"interface"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.interface]]
        name = "Interface"
        class = "TRSI"
    
    Note that multiple interfaces may be added, indicated by the double square brackets around the
    section header. The same class type may be initialised multiple times with different values for
    its options. Acquisition methods may then select which interface entry to use.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._log = logging.getLogger(__name__)

        #: Description of this interface device.
        self.description = "TRS-Interface"

        self._init_trsi()

    def _init_trsi(self):
        """Initialise the interface hardware."""
        self.trsi = TRSInterface()
        self.trsi.register_data_callback(self._data_handler)
        self.trsi.register_error_callback(self._error_handler)
        # We'll assume other configuration of the device has been done and saved into flash memory
        self.trsi.camera_sync_duration = 1

    def _data_handler(self, quad_pos, chop_state):
        for cb in self._data_callbacks.copy():
            cb(quad_pos, chop_state)

    def _error_handler(self, msg):
        self._log.warning(f"{self.description} hardware reported an error ({msg}), will attempt to recover.")
        # Try to do a close/open cycle on the device
        self.trsi.close()
        sleep(5.0)
        try:
            self._init_trsi()
        except:
            self._log.error(f"Unable to re-initialise {self.description} hardware.")
            # TODO: This should really be handled by the interface module with a close(device=...) or similar
            # Remove ourself from the list of initialised interfaces
            try:
                for i, device in enumerate(hw.modules["interface"].devices):
                    if device == self:
                        hw.modules["interface"].devices[i] = None
            except:
                self._log.debug(f"Unable to remove {self.description} from interface hardware list.")
            # Notify of change in devices
            for cb in hw.modules["interface"]._change_callbacks.copy(): cb()

    def close(self) -> None:
        self.trsi.close()

    def is_initialised(self) -> bool:
        return self.trsi.connected

    def trigger(self) -> None:
        self.trsi.camera_sync_delay = int(42e6/config.data["hardware"]["laser_reprate"] - 2400)
        self.trsi.trigger()

    def start(self, count=0) -> None:
        self.trsi.camera_sync_delay = int(42e6/config.data["hardware"]["laser_reprate"] - 2400)
        self.trsi.start(frame_count=count)

    def arm(self) -> None:
        self.trsi.camera_sync_delay = int(42e6/config.data["hardware"]["laser_reprate"] - 2400)
        self.trsi.arm()

    def stop(self) -> None:
        self.trsi.stop()
    
    def set_encoder_count(self, value: int) -> None:
        self.trsi.quadrature_value = int(value)