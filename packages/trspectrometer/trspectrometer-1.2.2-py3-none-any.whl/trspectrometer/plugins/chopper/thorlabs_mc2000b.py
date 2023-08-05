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

from typing import Optional

from . import Chopper
from thorlabs_mc2000b import MC2000B, Blade

class Thorlabs_MC2000B(Chopper):
    """
    Interface to the Thorlabs MC2000B optical chopper unit.

    Support is provided using the `thorlabs-mc2000b python package
    <https://thorlabs-mc2000b.readthedocs.io>`__

    To use this chopper driver class, ensure ``"chopper"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.chopper]]
        name = "Chopper"
        class = "Thorlabs_MC2000B"
    
    Note that multiple choppers may be added, indicated by the double square brackets around the
    section header. Acquisition methods may then select which chopper entry to use.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: Description of the chopper device.
        self.description = "Thorlabs MC2000B"

        self._device = MC2000B()
        
        # Choose between the inner vs outer slots for sync using existing configuration
        if "inner" in self._device.get_inref_string():
            self._in_or_out = "-inner"
        elif "outer" in self._device.get_inref_string():
            self._in_or_out = "-outer"
        else:
            self._in_or_out = ""
    
    def get_enabled(self) -> bool:
        return self._device.enable
    
    def set_enabled(self, value: bool) -> None:
        self._device.enable = bool(value)

    def get_divider(self) -> int:
        return self._device.dharmonic
    
    def set_divider(self, value: int) -> None:
        self._device.dharmonic = int(value)

    def get_frequency(self) -> Optional[int]:
        if "external" in self._device.get_inref_string():
            return None
        return self._device.freq
    
    def set_frequency(self, value: Optional[int]) -> None:
        try:
            value = int(value)
            # Valid value was passed, use internal sync
            self._device.set_inref_string(f"internal{self._in_or_out}")
            self._device.freq = value
        except (TypeError, ValueError):
            # None or invalid value, use external sync
            self._device.set_inref_string(f"external{self._in_or_out}")
