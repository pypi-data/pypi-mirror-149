# Copyright 2020 Patrick C. Tapping
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
Module for management of various spectrometer hardware devices.

This does not actually control any hardware itself, but instead stores
references to plugin modules which do the hard work.

A hardware plugin is a normal plugin module, but must also:

  - Implement a ``init()`` method to connect to and initialise the device(s).
  - Implement a ``close()`` method to disconnect from devices and free any used resources.
  - Implement a ``statuspanel`` property to return a QWidget class type
    (not an instance of the class!) to display device status information in the
    hardware status panel. This may be ``None`` if no panel is required.
  - Add a reference to itself to the :data:`modules` dictionary, for example using
    ``hardware.modules[__name__] = sys.modules[__name__]``.

Calling of the plugin's ``init()`` and ``close()`` methods will be handled automatically,
as will creation and display of the ``statuspanel`` if provided.
"""

import os
import logging
from collections import namedtuple
import time

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import loadUiType

_log = logging.getLogger(__name__)

#: Dictionary of configured hardware device modules.
#: The keys are strings containing the name of the module, with values being
#: the loaded module instance.
#: Hardware plugin modules should add themselves to this, for example by using
#: ``hardware.modules[__name__] = sys.modules[__name__]``.
modules = {}

def init():
    """Initialise all hardware devices."""
    global modules
    _log.info("Initialising hardware devices.")
    for name, module in modules.items():
        try:
            module.init()
        except Exception:
            _log.exception(f"Error initialising module: {name}")
    # Wait for final init to occur, such as delay homing operations
    _log.info("Waiting for all device initialisations to complete...")
    # Give a second for devices to update their status etc
    time.sleep(1.0)
    ready = False
    clock = time.monotonic()
    while not ready:
        if time.monotonic() > clock + 60.0:
            _log.warning("Timeout waiting for device initialisations to complete!")
            break
        ready = True
        # Wait for delay(s) to finish homing
        if "delay" in modules:
            for delay in modules["delay"].devices:
                if not delay is None and delay.is_initialised():
                    ready &= not delay.is_moving()
        time.sleep(0.5)
    _log.info("Hardware initialisation finished.")


def close():
    """Close connections to all hardware devices."""
    global modules
    _log.info("Closing hardware devices.")
    for name, module in modules.items():
        try:
            module.close()
        except:
            _log.exception(f"Error closing module: {name}")


class HardwareStatusPanel(QtWidgets.QScrollArea):
    """
    Window in which to place the individual hardware status panels.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # Build the UI
        self.setWindowTitle("Hardware Status")
        self.setWindowIcon(QtGui.QIcon("trspectrometer.png"))
        self.setWidgetResizable(True)
        self.setMinimumSize(500, 50)
        self.panel = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self)
        # Add the various hardware status panels
        global modules
        for _, module in modules.items():
            if module.statuspanel:
                w = module.statuspanel(self)
                self.layout.addWidget(w)
        self.layout.addStretch(1)
        self.panel.setLayout(self.layout)
        self.setWidget(self.panel)
