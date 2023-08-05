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

from . import Delay

class DummyDelay(Delay):
    """
    A dummy :data:`~trspectrometer.plugins.delay` class which simulates the presence of a real delay
    device.

    To use this delay driver class, ensure ``"delay"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.delay]]
        name = "Delay"
        class = "DummyDelay"
    
    Note that multiple delays may be added, indicated by the double square brackets around the
    section header. The same class type may be initialised multiple times with different values for
    its options. Acquisition methods may then select which delay entry to use.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #: Description of the delay device.
        self.description = "Dummy Delay"
    
    def home(self) -> None:
        self._target = 0.0
