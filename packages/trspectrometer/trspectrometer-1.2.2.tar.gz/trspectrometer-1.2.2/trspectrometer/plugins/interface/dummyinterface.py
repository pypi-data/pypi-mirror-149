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

import configuration as config
from . import Interface

class DummyInterface(Interface):
    """
    An :data:`~trspectrometer.plugins.interface` class which simulates the presence of an interface device.

    To use this interface driver class, ensure ``"interface"`` is present in the :ref:`configuration
    file`'s ``load=[...]`` list inside the :ref:`plugins` section, then include a section such as
    this in the :ref:`configuration file` under the ``[hardware]`` section:

    .. code-block:: toml

        [[hardware.interface]]
        name = "Interface"
        class = "DummyInterface"
    
    Note that multiple interfaces may be added, indicated by the double square brackets around the
    section header. The same class type may be initialised multiple times with different values for
    its options. Acquisition methods may then select which interface entry to use.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #: Description of this interface device.
        self.description = "Dummy Interface"

        # Simulated encoder count tracking
        self._enc_count = 0

        # Background thread to acquire simulated data
        self._acq_thread = None
        self._acq_stop = Event()

    def start(self, count=0) -> None:
        # Stop any existing thread
        self.stop()
        self._acq_thread = Thread(target=self._start_acq, args=(count,))
        self._acq_stop.clear()
        self._acq_thread.start()

    def arm(self) -> None:
        self.start(count=10000)

    def stop(self) -> None:
        if self._acq_thread:
            self._acq_stop.set()
            self._acq_thread.join()
    
    def set_encoder_count(self, value: int) -> None:
        self._enc_count = value

    def _start_acq(self, n):
        cycletime = 1.0/config.data["hardware"]["laser_reprate"]
        chop_state = np.zeros(n, dtype=bool)
        chop_state[::2] = True
        quad_pos = np.arange(self._enc_count, self._enc_count + n*1000, n*1000, dtype=np.uint32)
        sleep(n*cycletime)
        for cb in self._data_callbacks.copy():
            cb(quad_pos, chop_state)