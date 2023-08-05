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

class DummyChopper(Chopper):
    """
    A dummy :data:`~trspectrometer.plugins.chopper` class which simulates the presence of a real
    chopper device.

    To use this chopper driver class, ensure ``"chopper"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.chopper]]
        name = "Chopper"
        class = "DummyChopper"
    
    Note that multiple choppers may be added, indicated by the double square brackets around the
    section header. Acquisition methods may then select which chopper entry to use.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: Description of the chopper device.
        self.description = "Dummy Chopper"

        self._enabled = False
        self._divider = 1
        self._freq = 500

    def get_enabled(self) -> bool:
        return self._enabled
    
    def set_enabled(self, value: bool) -> None:
        self._enabled = bool(value)

    def get_divider(self) -> int:
        return self._divider
    
    def set_divider(self, value: int) -> None:
        self._divider = int(value)

    def get_frequency(self) -> Optional[int]:
        return self._freq
    
    def set_frequency(self, value: Optional[int]) -> None:
        try:
            self._freq = int(value)
        except (TypeError, ValueError):
            self._freq = None
    

    