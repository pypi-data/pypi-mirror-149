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
Module for management of delay stages used to create pump--probe delays or similar.

A typical delay will use a linear translation stage with a retroreflecting mirror attached, which
creates delay by changing the laser propagation path length. However, a delay could also be
constructed using other technologies, such as electronic synchronisation, translating glass wedge
pairs, or rotating optical flats.

The implementation of the actual control of the hardware is abstracted from the software interface.
The python `pluginlib <https://pluginlib.readthedocs.io/en/latest/index.html>`__ is used to find
classes which implement and extend the :class:`~Delay` class and actually communicate with the delay
device.

Delay plugin classes which are built-in include:

- :data:`~trspectrometer.plugins.delay.thorlabs_apt.Thorlabs_BBD201_DDS600`, a Thorlabs BBD201
  controller paired with a DDS600 linear translation stage. This combination is able to provide raw
  quadrature encoder and triggering signals to the
  :data:`~trspectrometer.plugins.interface.trsi.TRSI` interface hardware and thus is compatible with
  the :data:`~trspectrometer.plugins.acquisition.ta_swept.TA_SweptAcquisition`
  :data:`~trspectrometer.plugins.acquisition` method.

- :data:`~trspectrometer.plugins.delay.dummydelay.DummyDelay`, which simulates the presence of a
  delay device for demonstration or testing purposes.

To load the delay plugin module, ensure ``"delay"`` is present in the :ref:`configuration file`'s
``load=[...]`` list inside the :ref:`plugins` section. To configure the module to use a specific
driver class, ensure a ``[[hardware.delay]]`` section is present such as the default:

.. code-block:: toml

    # Delay configuration
    # Each entry specifies a delay device
    #   name (string) : Friendly name for the delay to use in the application
    #   class (string) : Name of specific class to load to drive the delay
    #   options (dict) : Dictionary of key=value pairs to pass to the class init() method
    [[hardware.delay]]
    name = "Delay"
    class = "DummyDelay"
    options = {}

Multiple delay devices can be specified by including multiple ``[[hardware.delay]]`` sections. The
double rectangular brackets around ``[[hardware.delay]]`` indicate that multiple sections are
permitted. The same class type may be initialised multiple times with different values for its
options. Acquisition methods may then select which delay entry to use.
"""

import os
import sys
import logging

import tomlkit
import pluginlib
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal

import configuration as config
import hardware as hw


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
# Delay configuration
# Each entry specifies a delay device
#   name (string) : Friendly name for the delay to use in the application
#   class (string) : Name of specific class to load to drive the delay
#   options (dict) : Dictionary of key=value pairs to pass the the class init() method
[[hardware.delay]]
name = "Delay"
class = "DummyDelay"
options = {}
"""

_log = logging.getLogger(__name__)

#: QWidget class type to use for displaying hardware status.
statuspanel = None

#: List of instances of delay device classes.
#: The number of entries in the list should correspond to the ``[[hardware.delay]]``
#: entries in the configuration file. If a device is missing or not initialised,
#: a value of ``None`` should be used as a placeholder.
devices = []

#: List of functions to call when devices are refreshed.
_change_callbacks = set()

#: Plugin class loader
_loader = None

def init():
    """
    Initialise the delay devices specified in the configuration file.
    """
    global devices
    # Close any existing devices
    close()
    devices = []
    for d in config.data["hardware"]["delay"]:
        device = None
        # Attempt to initialise the delay class specified in the configuration file
        try:
            delay_class = _loader.get_plugin("Delay", d["class"])
            if delay_class is None:
                _log.error(f"Can't find plugin for {d['name']} class {d['class']}")
            else:
                # Get options dictionary from configuration file
                opts = {}
                try:
                    opts = d["options"]
                    if not isinstance(opts, dict):
                        _log.warning("Options entry for {d['name']} is not a dictionary type.")
                        opts = {}
                except: pass
                device = delay_class(**opts)
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
    Close any open delay devices.
    """
    global devices
    for i, device in enumerate(devices):
        if device:
            try:
                device.close()
            except:
                _log.exception(f"Error closing delay {type(device).__name__} device for {config.data['hardware']['delay'][i]}.")
    # None is a placeholder for closed/missing devices
    devices = [None for _ in config.data['hardware']['delay']]
    # Notify callbacks of device close
    for cb in _change_callbacks.copy(): cb()


@pluginlib.Parent(group="delay")
class Delay():
    """
    Parent class of all :data:`~trspectrometer.plugins.delay` module plugins.

    Every delay driver class should derive from this parent, so that the automatic device class
    discovery can function.
    """
    def __init__(self, **kwargs):
        
        #: Friendly name to identify this unit.
        self.name = "Delay"

        #: Description of this delay device.
        self.description = "Unknown Delay"
       
        #: Dictionary containing current status information about the device.
        self.status = {}

        #: Target delay time requested for this device, in seconds.
        self._target = 0.0

    def close(self) -> None:
        """
        Close the connection to the device.
        """
        pass

    def min_delay(self) -> float:
        """
        Get the minimum available delay time provided by this unit, in seconds.

        :returns: Minimum available delay time, in seconds.
        """
        return 0.0

    def max_delay(self) -> float:
        """
        Get the maximum available delay time provided by this unit, in seconds.

        :returns: Maximum available delay time, in seconds.
        """
        return 10e-9

    def min_increment(self) -> float:
        """
        Get the minimum possible delay time increment for this unit, in seconds.

        :returns: Minimum possible delay time increment, in seconds.
        """
        return 1e-15

    def get_delay(self) -> float:
        """
        Get the current delay time provided by this unit, in seconds.

        The current delay corresponds to the (best estimate) of the current delay time,
        which may be updated during the device's movement and therefore may not immediately
        correspond to the time which was requested.
        The :meth:`get_target` method instead provides the target delay time.

        :returns: Current delay time, in seconds.
        """
        return self._target

    def set_delay(self, delay_time: float) -> None:
        """
        Set the delay time to an absolute value, in seconds.

        :param delay_time: Absolute delay time to set, in seconds.
        """
        if delay_time < self.min_delay() or delay_time > self.max_delay():
            raise RuntimeWarning(f"Requested delay_time of {delay_time} outside of limits {self.min_delay()} to {self.max_delay()} s")
        else:
            self._target = delay_time
    
    def increment_delay(self, delay_increment: float) -> None:
        """
        Set the delay to a value relative to its current target delay time, in seconds.
        
        Negative values for the delay increment are allowed.

        :param delay_increment: Relative delay time to set, in seconds.
        """
        self.set_delay(self._target + delay_increment)

    def get_target(self) -> float:
        """
        Target delay time requested from this unit, in seconds.

        The requested and current delay times may differ due to the time the device
        needs to physically move in order to create the delay.

        :returns: Requested delay time, in seconds.
        """
        return self._target

    def home(self) -> None:
        """
        Reset the delay and perform a homing operation.
        """
        pass

    def stop(self) -> None:
        """
        Stop any current delay movement operation.
        """
        pass

    def get_velocity(self):
        """
        Get the movement velocity of the delay stage, in delay/s.

        The value is technically unitless, but represents (delay seconds) per (wall clock seconds).

        Note that this is the velocity at which the delay stage is programmed to move at, not the
        current velocity.

        :returns: Maximum delay stage movement velocity, in delay/s.
        """
        return 1e-8

    def set_velocity(self, velocity) -> None:
        """
        Set the delay stage movement speed, in delay/s.

        The value is technically unitless, but represents (delay seconds) per (wall clock seconds).

        :param velocity: New delay stage movement velocity, in delay/s.
        """
        pass

    def get_acceleration(self):
        """
        Get the delay stage movement acceleration, in delay/s/s.

        The units represent (delay seconds) per (wall clock seconds squared).

        :returns: Delay stage movement acceleration, in delay/s/s.
        """
        return 1e-7
    
    def set_acceleration(self, acceleration) -> None:
        """
        Set the delay movement acceleration, in delay/s/s.

        The units represent (delay seconds) per (wall clock seconds squared).

        :param acceleration: New delay stage movement acceleration, in delay/s/s.
        """
        pass
    
    def is_initialised(self) -> bool:
        """
        Test whether the delay hardware is present and initialised, and not in any error state.
        """
        return True

    def is_moving(self) -> bool:
        """
        Test whether the delay is currently moving into position.

        The default method for determining whether the delay is moving is to check if the current
        delay does not match the requested target delay, within the tolerances of the minimum
        possible delay time increment given by :meth:`min_increment`.

        :returns: Boolean indicating whether the delay is currently moving.
        """
        return (abs(self.get_delay() - self.get_target()) >= self.min_increment())

    def get_encoder_count(self) -> int:
        """
        Retrieve the current position of the delay in raw encoder counts.

        If this functionality is not available, ``None`` will be returned.

        :returns: Position as raw encoder counts.
        """
        return None

    def encoder_to_delay(self, counts:int) -> float:
        """
        Convert from the raw device encoder counts to delay time.

        If this functionality is not available, ``None`` will be returned.

        :param counts: Encoder counts.
        :returns: Delay time, in seconds.
        """
        return None

    def delay_to_encoder(self, delay_time:float) -> int:
        """
        Convert from delay time to the raw device encoder counts.

        If this functionality is not available, ``None`` will be returned.

        :param delay_time: Delay time, in seconds.
        :returns: Encoder counts.
        """
        return None


class DelayStatusPanel(QtWidgets.QFrame):
    """
    Panel to insert into the Hardware Status window to show status of the Delay's hardware
    connection.
    """
    
    #: Qt Signal to indicate the devices have changed in some way and the panel requires refreshing.
    devices_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Delay:")
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
        for i, d in enumerate(config.data["hardware"]["delay"]):
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
statuspanel = DelayStatusPanel

# Create default config entries for delay device(s) if required
config.add_defaults(tomlkit.parse(_default_config))

# None is a placeholder for closed/missing devices
devices = [None for _ in config.data["hardware"]["delay"]]

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    # Look for valid plugin classes
    try:
        plugin_paths = [ os.path.join(d, "delay") for d in config.data["directories"]["plugins"] ]
        plugin_paths = [ d for d in plugin_paths if os.access(d, os.R_OK) ]
        _loader = pluginlib.PluginLoader(group="delay", modules=["delay"], paths=plugin_paths)
    except Exception as ex:
        raise RuntimeError(f"Error loading delay plugin classes: {ex}")
    _log.info(f"Available delay plugin classes: {', '.join(list(_loader.plugins['Delay']))}")

    # Add ourselves to the list of active hardware modules
    hw.modules[__name__] = sys.modules[__name__]

    # The DataPanel will want to know when delay hardware changes state
    add_change_callback(config.mainwindow.dataPanel.delay_plugins_changed)