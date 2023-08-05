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
Module for management of the interface hardware.

The interface hardware is responsible for several tasks related to synchronising the various devices
to the laser sync pulses, and getting that information sent back to the host computer:

- Externally trigger the detector with the correct timings so that the detector exposure period
  captures the arrival of the laser's light pulse.

- Start detector triggering when requested by software, or on receipt of an external trigger input
  signal such as the delay movement.

- Generate the appropriate synchronisation signal to drive the chopper.

- Read and return the state of the chopper ("on" or "off") on each triggering of the detector.

- Read and return the state of the delay encoder (quadrature) on each triggering of the detector.

Not all functions are necessarily essential depending, for example, on the particular
:data:`~trspectrometer.plugins.acquisition` mode in use.

The implementation of the functionality is abstracted from the software interface. The python
`pluginlib <https://pluginlib.readthedocs.io/en/latest/index.html>`__ is used to find classes which
implement and extend the :class:`~Interface` class and actually communicate with the attached
interface hardware.

Interface classes which are built-in include:

- :data:`~trspectrometer.plugins.interface.trsi.TRSI`, which supports the `TRS-Interface
  <https://trs-interface.readthedocs.io>`__. The hardware and firmware are open source, and may be
  built as-is to work with the :ref:`reference design`, or modified to better integrate with
  alternative hardware devices.

- :data:`~trspectrometer.plugins.interface.dummyinterface.DummyInterface`, which simulates the
  presence of the interface hardware for testing or demonstration purposes.

To load the interface plugin module, ensure ``"interface"`` is present in the :ref:`configuration
file`'s ``load=[...]`` list inside the :ref:`plugins` section. To configure the module to use a
specific driver class, ensure a ``[[hardware.interface]]`` section is present such as the default:

.. code-block:: toml

    # Interface configuration
    # The entry specifies a single device
    #   name (string) : Friendly name for the interface to use in the application
    #   class (string) : Name of specific class to load to drive the interface
    #   options (dict) : Dictionary of key=value pairs to pass the the class init() method
    [[hardware.interface]]
    name = "Interface"
    class = "DummyInterface"
    options = {}

Multiple interface devices can be specified by including multiple ``[[hardware.interface]]``
sections. The double rectangular brackets around ``[[hardware.interface]]`` indicate that multiple
sections are permitted. The same class type may be initialised multiple times with different values
for its options. Acquisition methods may then select which interface entry to use.
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
# Interface configuration
# Each entry specifies an interface device
#   name (string) : Friendly name for the interface to use in the application
#   class (string) : Name of specific class to load to drive the interface
#   options (dict) : Dictionary of key=value pairs to pass the the class init() method
[[hardware.interface]]
name = "Interface"
class = "DummyInterface"
options = {}
"""

_log = logging.getLogger(__name__)

#: QWidget class type to use for displaying hardware status.
statuspanel = None

#: Reference to a Interface class.
#: The number of entries in the list should correspond to the ``[[hardware.interface]]``
#: entries in the configuration file. If a device is missing or not initialised,
#: a value of ``None`` will be used as a placeholder.
devices = None

#: List of functions to call when devices are refreshed.
_change_callbacks = set()

#: Plugin class loader
_loader = None

def init():
    """
    Initialise the Interface device specified in the configuration file.
    """
    global devices

    # Close any existing devices
    close()
    devices = []
    for d in config.data["hardware"]["interface"]:
        device = None
        # Attempt to initialise the interface class specified in the configuration file
        try:
            device_class = _loader.get_plugin("Interface", d["class"])
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
    Close any open Interface devices.
    """
    global devices
    for i, device in enumerate(devices):
        if device:
            try:
                device.close()
            except:
                _log.exception(f"Error closing interface {type(device).__name__} device for {config.data['hardware']['interface']}.")
    # None is a placeholder for closed/missing devices
    devices = [None for _ in config.data["hardware"]["interface"]]
    # Notify callbacks of device close
    for cb in _change_callbacks.copy(): cb()


@pluginlib.Parent(group="interface")
class Interface():
    """
    Parent class for all :data:`~trspectrometer.plugins.interface` plugins.

    Every :data:`~trspectrometer.plugins.interface` driver class should derive from this parent, so
    that the automatic device class discovery can function.
    """
    def __init__(self, **kwargs):

         #: Friendly name to identify this unit.
        self.name = "Interface"

        #: Description of this interface device.
        self.description = "Unknown Interface"

        #: Set of functions to call when data is acquired.
        self._data_callbacks = set()

    def close(self) -> None:
        """
        Close the connection to the device.
        """
        pass

    def is_initialised(self) -> bool:
        """
        Test whether the interface hardware is present and initialised, and not in any error state.
        """
        return True
    
    def register_data_callback(self, callback: callable) -> None:
        """
        Register a function to receive notifications for data received from the device.

        The callback method should take the form of ``data_callback(quad_pos, chop_state)``,
        where ``quad_pos`` is an array of quadrature positions, and ``chop_state`` is the chopper
        on/off state.

        :param callback: Function to call when data is received.
        """
        if callable(callback):
            self._data_callbacks.add(callback)
        else:
            raise RuntimeError("Attempted to register non-callable function for data callbacks.")
    
    def unregister_data_callback(self, callback: callable) -> None:
        """
        Unregister a function previously registered to receive data callbacks using
        :meth:`register_data_callback`.

        :param callback: Function to unregister.
        """
        if callback in self._data_callbacks:
            self._data_callbacks.remove(callback)
        else:
            raise RuntimeWarning("Attempted to unregister an unknown function for data callbacks.")

    def trigger(self) -> None:
        """
        Begin triggering the detector, but do not collect chopper or delay state information.

        Note that data related to the delay encoder or chopper state will `not` be passed to any
        registered data callback functions when using this mode of triggering.
        """
        pass

    def start(sel, count: int=0) -> None:
        """
        Begin acquisition of data.

        The triggering of the detector will start immediately, and the state of the delay encoder
        and chopper will be collected for each trigger pulse sent to the detector. To stop the
        triggering, call the :meth:`~stop` method. Once stopped, data will be returned to any
        functions previously registered using the :meth:`~register_data_callback` method.

        Setting the ``count`` parameter to a positive integer will cause the triggering to stop
        after the given number of trigger pulses have been sent. The default of 0 means to trigger
        until the :meth:`stop` method is called.

        :param count: Number of trigger of trigger pulses to send.
        """
        pass

    def arm(self) -> None:
        """
        Arm the device, ready to be triggered by an external signal.

        This acts similarly to using the :meth:`~start` method, but instead of immediately starting
        to trigger the detector, the interface will wait for a trigger signal from an external
        input, such as the "movement" signal from an attached delay stage.

        This method is used by the :data:`~trspectrometer.plugins.acquisition.ta_swept`
        :data:`~trspectrometer.plugins.acquisition` method, which requires a delay which provides
        both raw encoder position and movement trigger signals to the interface hardware.
        """
        pass

    def stop(self) -> None:
        """
        Abort the acquisition of data.

        This will stop the interface regardless of whether it was started with the :meth:`~trigger`,
        :meth:`~start`, or :meth:`~arm` methods.
        """
        pass

    def set_encoder_count(self, value: int) -> None:
        """
        Configure the current value for the delay quadrature encoder reading.

        This should be set to match the delay's own record of its quadrature value. Note that to
        ensure accuracy, the delay should be homed and stopped prior to reading its quadrature
        position.

        :param value: New quadrature encoder value.
        """
        pass


class InterfaceStatusPanel(QtWidgets.QFrame):
    """
    Panel to insert into the Hardware Status window to show status of the Interface hardware
    connection.
    """

    #: Qt Signal to indicate the devices have changed in some way and the panel requires refreshing.
    devices_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Interface:")
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
        for i, d in enumerate(config.data["hardware"]["interface"]):
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
statuspanel = InterfaceStatusPanel

# Create default config entries for device(s) if required
config.add_defaults(tomlkit.parse(_default_config))

# None is a placeholder for closed/missing device
devices = [None for _ in config.data["hardware"]["interface"]]

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    # Look for valid plugin classes
    try:
        plugin_paths = [ os.path.join(d, "interface") for d in config.data["directories"]["plugins"] ]
        plugin_paths = [ d for d in plugin_paths if os.access(d, os.R_OK) ]
        _loader = pluginlib.PluginLoader(group="interface", modules=["interface"], paths=plugin_paths)
    except Exception as ex:
        raise RuntimeError(f"Error loading interface plugin classes: {ex}")
    _log.info(f"Available interface plugin classes: {', '.join(list(_loader.plugins['Interface']))}")

    # Add ourselves to the list of active hardware modules
    hw.modules[__name__] = sys.modules[__name__]
