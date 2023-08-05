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
Module for management of optical choppers.

A chopper is used to modulate laser beams so that enhanced detection is possible by comparing the
difference between the laser "on" signal to that of the laser "off".

The implementation of the actual control of the hardware is abstracted from the software interface.
The python `pluginlib <https://pluginlib.readthedocs.io/en/latest/index.html>`__ is used to find
classes which implement and extend the :class:`~Chopper` class and actually communicate with the
chopper device.

Chopper plugin classes which are built-in are:

- :data:`~trspectrometer.plugins.chopper.thorlabs_mc2000b.Thorlabs_MC2000B`, for a Thorlabs MC2000B
  unit. Support is provided using the `thorlabs-mc2000b python package
  <https://thorlabs-mc2000b.readthedocs.io>`__

- :data:`~trspectrometer.plugins.chopper.dummychopper.DummyChopper`, which emulates a real chopper
  device for demonstration or testing purposes.

To load the chopper plugin module, ensure ``"chopper"`` is present in the :ref:`configuration
file`'s ``load=[...]`` list inside the :ref:`plugins` section. To configure the module to use a
specific driver class, ensure a ``[[hardware.chopper]]`` section is present such as the default:

.. code-block:: toml

    # Chopper configuration
    # Each entry specifies a chopper device
    #   name (string) : Friendly name for the chopper to use in the application
    #   class (string) : Name of specific class to load to drive the chopper
    #   options (dict) : Dictionary containing key=value pairs to pass to the class init() method
    [[hardware.chopper]]
    name = "Chopper"
    class = "DummyChopper"
    options = {}

Multiple chopper devices can be specified by including multiple ``[[hardware.chopper]]`` sections.
The double rectangular brackets around ``[[hardware.chopper]]`` indicate that multiple sections are
permitted. The same class type may be initialised multiple times with different values for its
options. Acquisition methods may then select which chopper entry to use.
"""


import os
import sys
import logging
from typing import Optional

import tomlkit
import pluginlib
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal

import configuration as config
import hardware as hw


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
# Chopper configuration
# Each entry specifies a chopper device
#   name (string) : Friendly name for the chopper to use in the application
#   class (string) : Name of specific class to load to drive the chopper
#   options (dict) : Dictionary containing key=value pairs to pass to the class init() method
[[hardware.chopper]]
name = "Chopper"
class = "DummyChopper"
options = {}
"""

_log = logging.getLogger(__name__)

#: QWidget class type to use for displaying hardware status.
statuspanel = None

#: List of instances of chopper device classes.
#: The number of entries in the list should correspond to the ``[[hardware.chopper]]``
#: entries in the configuration file. If a device is missing or not initialised,
#: a value of ``None`` should be used as a placeholder.
devices = []

#: List of functions to call when devices are refreshed.
_change_callbacks = set()

#: Plugin class loader
_loader = None

def init():
    """Initialise the chopper devices specified in the configuration file."""
    global devices

    # Close any existing devices
    close()
    devices = []
    for d in config.data["hardware"]["chopper"]:
        device = None
        # Attempt to initialise the chopper class specified in the configuration file
        try:
            device_class = _loader.get_plugin("Chopper", d["class"])
            if device_class is None:
                _log.error(f"Can't find plugin for {d['name']} class {d['class']}")
            else:
                # Get options dictionary from configuration file
                opts = {}
                try:
                    opts = d["options"]
                    if not isinstance(opts, dict):
                        _log.warning(f"Options entry for {d['name']} is not a dictionary type.")
                        opts = {}
                except: pass
                device = device_class(**opts)
                device.name = d["name"]
                _log.info(f"Initialised {d['name']} using class {d['class']}")
        except Exception as ex:
            _log.error(f"Unable to initialise {d['name']} using class {d['class']}: {ex}")
        # Add the device (or None placeholder) to list of devices
        devices.append(device)

    # Notify callbacks of device refresh
    for cb in _change_callbacks.copy(): cb()


def add_change_callback(callback_function):
    """
    Register a function to be called when the devices are refreshed.

    :param callback_function: Function to call when devices are refreshed.
    """
    if callable(callback_function):
        _change_callbacks.add(callback_function)


def remove_change_callback(callback_function):
    """
    Unregister a callback function added using :meth:`add_change_callback`.

    :param callback_function: Function to unregister.
    """
    if callback_function in _change_callbacks:
        _change_callbacks.remove(callback_function)


def close():
    """
    Close any open chopper devices.
    """
    global devices
    for i, device in enumerate(devices):
        if device:
            try:
                device.close()
            except:
                _log.exception(f"Error closing chopper {type(device).__name__} device for {config.data['hardware']['chopper'][i]}.")
    # None is a placeholder for closed/missing devices
    devices = [None for _ in config.data["hardware"]["chopper"]]
    # Notify callbacks of device close
    for cb in _change_callbacks.copy(): cb()


@pluginlib.Parent(group="chopper")
class Chopper():
    """
    Parent class of all :data:`~trspectrometer.plugins.chopper` plugins.

    Every chopper driver class should derive from this parent, so that the automatic device class
    discovery can function.
    """
    def __init__(self, **kwargs):

         #: Friendly name to identify this unit.
        self.name = "Chopper"

        #: Description of this chopper device.
        self.description = "Unknown Chopper"
       
    def close(self) -> None:
        """
        Close the connection to the device.
        """
        pass

    def is_initialised(self) -> bool:
        """
        Test whether the chopper hardware is present and initialised, and not in any error state.
        """
        return True
    
    def get_enabled(self) -> bool:
        """
        Get the current running state of the chopper.

        :returns: ``True`` if chopper is running, ``False`` if not.
        """
        return False
    
    def set_enabled(self, value: bool) -> None:
        """
        Set the current running state of the chopper.

        :param value: ``True`` to start the chopper, ``False`` to stop.
        """
        pass
 
    def get_divider(self) -> int:
        """
        Get the frequency divider of the chopper.

        :returns: Frequency divider.
        """
        return 1
    
    def set_divider(self, value: int) -> None:
        """
        Set the frequency divider of the chopper.

        :param value: Frequency divider.
        """
        pass

    def get_frequency(self) -> Optional[int]:
        """
        Get the source frequency of the chopper.

        A value of ``None`` indicates that the frequency is synced to an external source.

        :returns: Source frequency, or ``None`` if external sync.
        """
        return 0
    
    def set_frequency(self, value: Optional[int]) -> None:
        """
        Set the internal source frequency of the chopper.

        A value of ``None`` indicates that the frequency should be synced to an external source.

        :param value: Source frequency, or ``None`` if external sync.
        """
        pass


class ChopperStatusPanel(QtWidgets.QFrame):
    """
    Panel to insert into the Hardware Status window to show status of the Chopper's hardware
    connection.
    """
    
    #: Qt Signal to indicate the devices have changed in some way and the panel requires refreshing.
    devices_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Chopper:")
        self.label.setStyleSheet("QLabel { font-weight: bold }")
        self.horizontalLayout.addWidget(self.label)
        self.resetPushButton = QtWidgets.QPushButton("Reset")
        self.horizontalLayout.addWidget(self.resetPushButton)
        self.grid = QtWidgets.QGridLayout()
        self.grid.setContentsMargins(10, 0, 10, 0)
        self.layout().addLayout(self.horizontalLayout)
        self.layout().addLayout(self.grid)
        # Reset button triggers hardware re-init
        self.resetPushButton.clicked.connect(init)
        self.devices_changed.connect(self.refresh)
        self.refresh()

    def showEvent(self, event):
        """
        Handler for widget show events.
        """
        # Refresh UI when devices change
        add_change_callback(self._devices_changed)
    
    def hideEvent(self, event):
        """
        Handler for widget hide events.
        """
        # Remove change callback when not visible
        remove_change_callback(self._devices_changed)

    def _devices_changed(self):
        # Wrap signal emission so update happens in Qt thread
        self.devices_changed.emit()

    def refresh(self):
        """
        Refresh the state of the hardware connection and update the panel's display.
        """
        global devices
        # Remove all widgets from grid and destroy them
        while True:
            w = self.grid.takeAt(0)
            if w is None: break
            w.widget().deleteLater()
        # List the devices from configuration file
        for i, d in enumerate(config.data["hardware"]["chopper"]):
            self.grid.addWidget(QtWidgets.QLabel(d["name"]), i, 0)
            if devices[i]:
                self.grid.addWidget(QtWidgets.QLabel(devices[i].description), i, 1)
                if devices[i].is_initialised():
                    w = QtWidgets.QLabel("OK")
                    w.setStyleSheet("QLabel { color : green; }")
                else:
                    w = QtWidgets.QLabel("ERROR")
                    w.setStyleSheet("QLabel { color : red; }")
                self.grid.addWidget(w, i, 2, QtCore.Qt.AlignRight)
            else:
                self.grid.addWidget(QtWidgets.QLabel(d["class"]), i, 1)
                w = QtWidgets.QLabel("Missing")
                w.setStyleSheet("QLabel { color : orange; }")
                self.grid.addWidget(w, i, 2, QtCore.Qt.AlignRight)

# Point to the correct widget class for displaying the hardware status panel
statuspanel = ChopperStatusPanel

# Create default config entries for device(s) if required
config.add_defaults(tomlkit.parse(_default_config))

# None is a placeholder for closed/missing devices
devices = [None for _ in config.data["hardware"]["chopper"]]

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    # Look for valid plugin classes
    try:
        plugin_paths = [ os.path.join(d, "chopper") for d in config.data["directories"]["plugins"] ]
        plugin_paths = [ d for d in plugin_paths if os.access(d, os.R_OK) ]
        _loader = pluginlib.PluginLoader(group="chopper", modules=["chopper"], paths=plugin_paths)
    except Exception as ex:
        raise RuntimeError(f"Error loading chopper plugin classes: {ex}")
    _log.info(f"Available chopper plugin classes: {', '.join(list(_loader.plugins['Chopper']))}")


    # Add ourselves to the list of active hardware modules
    hw.modules[__name__] = sys.modules[__name__]