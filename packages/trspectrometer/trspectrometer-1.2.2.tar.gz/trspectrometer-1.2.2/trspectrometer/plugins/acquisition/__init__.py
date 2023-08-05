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
Module for management of data acquisition methods.

This acquisition plugin module is implemented as a :ref:`hardware` :ref:`plugin <plugins>`, even
though the built-in acquisition methods only indirectly depend on other hardware plugins to be
present. This results in the acquisition methods being displayed in the :ref:`hardware_status`, with
their availability changing depending on the presence or absence of any required hardware devices.

The implementation of the actual data acquisition is abstracted from the software interface. The
python `pluginlib <https://pluginlib.readthedocs.io/en/latest/index.html>`__ is used to find classes
which implement and extend the :class:`~Acquisition` class and actually control the hardware,
collect data, process it, and store into an appropriate :data:`data structure
<trspectrometer.datastorage>` for display by the :data:`~trspectrometer.datapanel.DataPanel`.

Acquisition plugin classes which are built-in include:

- :data:`~trspectrometer.plugins.acquisition.ta_stepped.TA_SteppedAcquisition`, which performs a
  traditional transient absorption acquisition using a "change delay, acquire" loop. This mode is
  compatible with all delay types.

- :data:`~trspectrometer.plugins.acquisition.ta_swept.TA_SweptAcquisition`, which is a rapid
  transient absorption acquisition mode that performs continuous data collection while sweeping the
  delay range. It requires a delay which can provide raw encoder (quadrature) signals to the
  :data:`~trspectrometer.plugins.interface` hardware.

- :data:`~trspectrometer.plugins.acquisition.ta_dummy.TA_DummySteppedAcquisition`, which simulates a
  stepped transient absorption acquisition for demonstration and testing purposes. It does not
  require any additional hardware devices.

To load the acquisition plugin module, ensure ``"acquisition"`` is present in the
:ref:`configuration file`'s ``load=[...]`` list inside the :ref:`plugins` section. To configure the
module to use a specific driver class, ensure a ``[[hardware.acquisition]]`` section is present such as
the default:

.. code-block:: toml

    # Acquisition configuration
    # Each entry specifies a acquisition device
    #   name (string) : Friendly name for the acquisition method to use in the application
    #   class (string) : Name of specific class to load to drive the acquisition
    #   options (dict) : Dictionary of key=value pairs to pass to the class init() method
    [[hardware.acquisition]]
    name = "Dummy Stepped"
    class = "TA_DummySteppedAcquisition"
    options = {}

Multiple acquisition methods can be specified by including multiple ``[[hardware.acquisition]]``
sections. The double rectangular brackets around (``[[hardware.acquisition]]``) indicate that
multiple sections are permitted. The same class type may be initialised multiple times with
different values for its options.
"""


import os
import sys
import logging

import numpy as np
import tomlkit
import pluginlib
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal

import configuration as config
import hardware as hw


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
# Acquisition configuration
# Each entry specifies a acquisition device
#   name (string) : Friendly name for the acquisition method to use in the application
#   class (string) : Name of specific class to load to drive the acquisition
#   options (dict) : Dictionary of key=value pairs to pass to the class init() method
[[hardware.acquisition]]
name = "Dummy Stepped"
class = "TA_DummySteppedAcquisition"
options = {}
"""

_log = logging.getLogger(__name__)

#: QWidget class type to use for displaying hardware status.
statuspanel = None

#: List of instances of acquisition method classes.
#: The number of entries in the list should correspond to the ``[[hardware.acquisition]]``
#: entries in the configuration file. If a device is missing or not initialised,
#: a value of ``None`` should be used as a placeholder.
devices = []

#: List of functions to call when devices are refreshed.
_change_callbacks = set()

#: Plugin class loader
_loader = None

def init():
    """
    Initialise the acquisition devices specified in the configuration file.
    """
    global devices
    # Close any existing devices
    close()
    devices = []
    for d in config.data["hardware"]["acquisition"]:
        device = None
        # Attempt to initialise the acquisition class specified in the configuration file
        try:
            device_class = _loader.get_plugin("Acquisition", d["class"])
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
    Unregister a callback function added using ``add_change_callback()``.

    :param callback_function: Function to unregister.
    """
    if callback_function in _change_callbacks:
        _change_callbacks.remove(callback_function)


def close():
    """
    Close any open acquisition devices.
    """
    global devices
    for i, device in enumerate(devices):
        if device:
            try:
                device.close()
            except:
                _log.exception(f"Error closing acquisition {type(device).__name__} device for {config.data['hardware']['acquisition'][i]}.")
    # None is a placeholder for closed/missing devices
    devices = [None for _ in config.data["hardware"]["acquisition"]]
    # Notify callbacks of device close
    for cb in _change_callbacks.copy(): cb()


@pluginlib.Parent(group="acquisition")
class Acquisition():
    """
    Parent class of all acquisition class plugins.

    Every acquisition driver class should derive from this parent, so that the automatic device
    class discovery can function.
    """
    def __init__(self, **kwargs):

        #: Friendly name to identify this unit.
        self.name = "Acquisition"

        #: Description of this acquisition device.
        self.description = "Unknown Acquisition Method"
       
    def close(self) -> None:
        """
        Close the connection to the device.
        """
        pass

    def is_initialised(self) -> bool:
        """
        Test whether the acquisition hardware is present and initialised, and not in any error state.
        """
        return True
    
    def start(self) -> None:
        """
        Begin acquisition of data.

        It is up to the sub-classes implementing this method to determine what and how much data
        should be obtained in whatever manner is appropriate. For example, the data range and number
        of scans can be extracted from the :class:`DataPanel` user interface.

        During acquisition, the presence of new data points can be communicated to other components
        by emitting the :data:`~trspectrometer.signals.raw_data_updated` Signal. Parameters can be
        used to specify which points in the data set have changed to allow more efficient re-drawing
        for example.

        Upon completion of the acquisition, the :data:`~trspectrometer.signals.acquisition_stopped`
        Signal should be emitted to notify other components. If an error occurred, an Exception
        instance can be passed to provide further information. For example:

        .. code-block:: python

            from signalstorage import signals
            from utils import AcquisitionError
            
            if error:
                # Acquisition completed with some error
                signals.acquisition_stopped.emit(AcquisitionError("Something bad happened."))
            else:
                # Acquisition completed OK
                signals.acquisition_stopped.emit(None)
        """
        pass

    def stop(self) -> None:
        """
        Abort the acquisition of data.
        """
        pass


class AcquisitionStatusPanel(QtWidgets.QFrame):
    """
    Panel to insert into the Hardware Status window to show status of the acquisition method.
    """

    #: Qt Signal to indicate the devices have changed in some way and the panel requires refreshing.
    devices_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Acquisition:")
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
        for i, d in enumerate(config.data["hardware"]["acquisition"]):
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
statuspanel = AcquisitionStatusPanel

# Create default config entries for device(s) if required
config.add_defaults(tomlkit.parse(_default_config))

# None is a placeholder for closed/missing devices
devices = [None for _ in config.data["hardware"]["acquisition"]]

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    # Look for valid plugin classes
    try:
        plugin_paths = [ os.path.join(d, "acquisition") for d in config.data["directories"]["plugins"] ]
        plugin_paths = [ d for d in plugin_paths if os.access(d, os.R_OK) ]
        _loader = pluginlib.PluginLoader(group="acquisition", modules=["acquisition"], paths=plugin_paths)
    except Exception as ex:
        raise RuntimeError(f"Error loading acquisition plugin classes: {ex}")
    _log.info(f"Available acquisition plugin classes: {', '.join(list(_loader.plugins['Acquisition']))}")


    # Add ourselves to the list of active hardware modules
    hw.modules[__name__] = sys.modules[__name__]

    # The DataPanel will want to know when acquisition hardware changes state
    add_change_callback(config.mainwindow.dataPanel.acquisition_plugins_changed)