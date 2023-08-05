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
Module for management of detector devices.

A detector is a device which provides intensity values, often as a function of wavelength. These may
be small form fibre spectrometers, or larger CCD or CMOS cameras attached to spectrographs. Single
element detectors can be supported by returning a 1-element array of data, possibly also with an
arbitrary wavelength label.

The implementation of the actual control of the hardware is abstracted from the software interface.
The python `pluginlib <https://pluginlib.readthedocs.io/en/latest/index.html>`__ is used to find
classes which implement and extend the :class:`~Detector` class and actually communicate with
the detector device.

Detector plugin classes which are built-in are:

- :data:`~trspectrometer.plugins.detector.zylafixed.ZylaFixed`, for an Andor Zyla sCMOS camera
  attached to a fixed spectrograph unit. It may support other Andor sCMOS cameras which use the SDK3
  for communications with litle or no modifications. Support is provided using the `andor3 python
  package <https://andor3.readthedocs.io>`__

- :data:`~trspectrometer.plugins.detector.dummydetector.DummyDetector`, which simulates
  the presence of a detector for demonstration or testing purposes.

To load the detector plugin module, ensure ``"detector"`` is present in the
:ref:`configuration file`'s ``load=[...]`` list inside the :ref:`plugins` section. To configure the
module to use a specific driver class, ensure a ``[[hardware.detector]]`` section is present
such as the default:

.. code-block:: toml

    # Detector configuration
    # Each entry specifies a detector device
    #   name (string) : Friendly name for the detector to use in the application
    #   class (string) : Name of specific class to load to drive the detector
    #   options (dict) : Dictionary containing key=value pairs to pass to the class init() method
    [[hardware.detector]]
    name = "Detector"
    class = "DummyDetector"
    options = {}

Multiple detector devices can be specified by including multiple ``[[hardware.detector]]``
sections. The double rectangular brackets around ``[[hardware.detector]]`` indicate that
multiple sections are permitted. The same class type may be initialised multiple times with
different values for its options. Acquisition methods may then select which detector entry to use.
"""


import os
import sys
import logging
from typing import Optional, Union

import numpy as np
import numpy.typing as npt
import tomlkit
import pluginlib
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal

import configuration as config
import hardware as hw


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
# Detector configuration
# Each entry specifies a detector device
#   name (string) : Friendly name for the detector to use in the application
#   class (string) : Name of specific class to load to drive the detector
#   options (dict) : Dictionary containing key=value pairs to pass to the class init() method
[[hardware.detector]]
name = "Detector"
class = "DummyDetector"
options = {}
"""

_log = logging.getLogger(__name__)

#: QWidget class type to use for displaying hardware status.
statuspanel = None

#: List of instances of detector device classes.
#: The number of entries in the list should correspond to the ``[[hardware.detector]]``
#: entries in the configuration file. If a device is missing or not initialised,
#: a value of ``None`` should be used as a placeholder.
devices = []

#: List of functions to call when devices are refreshed.
_change_callbacks = set()

#: Plugin class loader
_loader = None

def init():
    """
    Initialise the detector devices specified in the configuration file.
    """
    global devices

    # Close any existing devices
    close()
    devices = []
    for d in config.data["hardware"]["detector"]:
        device = None
        # Attempt to initialise the detector class specified in the configuration file
        try:
            device_class = _loader.get_plugin("Detector", d["class"])
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
    Close any open detector devices.
    """
    global devices
    for i, device in enumerate(devices):
        if device:
            try:
                device.close()
            except:
                _log.exception(f"Error closing detector {type(device).__name__} device for {config.data['hardware']['detector'][i]}.")
    # None is a placeholder for closed/missing devices
    devices = [None for _ in config.data["hardware"]["detector"]]
    # Notify callbacks of device close
    for cb in _change_callbacks.copy(): cb()


@pluginlib.Parent(group="detector")
class Detector():
    """
    Parent class of all detector class plugins.

    Every detector driver class should derive from this parent, so that the automatic device class
    discovery can function.
    """
    def __init__(self, **kwargs):

         #: Friendly name to identify this unit.
        self.name = "Detector"

        #: Description of this detector device.
        self.description = "Unknown Detector"

        #: Set of functions to call on acquisition of individual spectra.
        self._spectrum_callbacks = set()

        #: Set of functions to call when acquisition of spectra is completed.
        self._acquisition_callbacks = set()
       
    def close(self) -> None:
        """
        Close the connection to the device.
        """
        pass

    def is_initialised(self) -> bool:
        """
        Test whether the detector hardware is present and initialised, and not in any error
        state.
        """
        return True
    
    def register_spectrum_callback(self, callback: callable) -> None:
        """
        Register a function to receive notifications for acquisition data of a single spectra.

        The callback method should take the form of ``spectrum_callback(data)``, where ``data`` is
        the data for the spectrum as a 1D numpy array.

        :param callback: Function to call on each spectrum acquisition event.
        """
        if callable(callback):
            self._spectrum_callbacks.add(callback)
        else:
            raise RuntimeError("Attempted to register non-callable function for spectrum callbacks.")
    
    def unregister_spectrum_callback(self, callback: callable) -> None:
        """
        Unregister a function previously registered to receive spectrum callbacks using
        :meth:`register_spectrum_callback`.

        :param callback: Function to unregister.
        """
        if callback in self._spectrum_callbacks:
            self._spectrum_callbacks.remove(callback)
        else:
            raise RuntimeWarning("Attempted to unregister an unknown function for spectrum callbacks.")

    def register_acquisition_callback(self, callback: callable) -> None:
        """
        Register a function to receive notifications for completion of acquisition.

        The callback method should take the form of ``acquisition_callback(data)``, where ``data``
        is the data for the spectra as a 2D numpy array.

        :param callback: Function to call on completion of acquisition.
        """
        if callable(callback):
            self._acquisition_callbacks.add(callback)
        else:
            raise RuntimeError("Attempted to register non-callable function for acquisition callbacks.")
    
    def unregister_acquisition_callback(self, callback: callable) -> None:
        """
        Unregister a function previously registered to receive acquisition callbacks using
        :meth:`register_acquisition_callback`.

        :param callback: Function to unregister.
        """
        if callback in self._acquisition_callbacks:
            self._acquisition_callbacks.remove(callback)
        else:
            raise RuntimeWarning("Attempted to unregister an unknown function for acquisition callbacks.")

    def get_triggermodes(self): # -> tuple[str]:
        """
        List the trigger modes available to the detector.

        :returns: Tuple of strings for available trigger modes.
        """
        return ("internal",)
    
    def set_triggermode(self, mode: str) -> None:
        """
        Set a acquisition triggering mode.

        The ``mode`` should be a value returned by :meth:`get_trigger_modes`.

        :param mode: Triggering mode.
        """
        pass

    def get_triggermode(self) -> str:
        """
        Get the current acquisition triggering mode.

        :returns: Current triggering mode.
        """
        return "internal"
    
    def get_exposure_limits(self): # -> tuple[float]:
        """
        Get the minimum and maximum allowed exposure times, in seconds.

        :returns: Tuple of minimum and maximum allowed exposure times.
        """
        return (1e-6, 1e-6)
    
    def get_exposure(self) -> float:
        """
        Get the currently set exposure time, in seconds.

        :returns: Current exposure time.
        """
        return 1e-6
    
    def set_exposure(self, time: float) -> None:
        """
        Set the desired exposure time, in seconds.

        :param time: Desired exposure time.
        """
        pass

    def get_wavelength_limits(self): # -> tuple[float]:
        """
        Get the minimum and maximum allowed values for the central wavelength selection, in
        nanometres.

        :returns: Tuple of minimum and maximum central wavelengths.
        """
        return (600.0, 600.0)
    
    def get_wavelength(self) -> float:
        """
        Get the current central wavelength, in nanometres.

        :returns: Current central wavelength.
        """
        return 600.0
    
    def set_wavelength(self, central_wavelength: float) -> None:
        """
        Set the central wavelength, in nanometres.

        :param central_wavelength: Desired central wavelength.
        """
        pass

    def get_gratings(self): # -> tuple[Optional[str]]:
        """
        List the gratings available for the detector.

        If the grating in the detector is not changeable, then an empty tuple may be returned.

        :returns: Tuple of strings for available gratings.
        """
        return ()
    
    def get_grating(self) -> Optional[str]:
        """
        Get the grating currently in use.

        If the grating is not selectable, then `None` may be returned.

        :returns: String describing the current grating.
        """
        return None
    
    def set_grating(self, grating: str) -> None:
        """
        Set the grating for the detector.

        :param: String describing desired grating.
        """
        pass

    def get_pixel_wavelengths(self) -> npt.ArrayLike:
        """
        Get an array containing the wavelength labels for each pixel in the acquired data.

        :returns: Wavelengths corresponding to data pixels.
        """
        return np.linspace(400.0, 800.0, 2048)

    def get_max_value(self) -> Union[int, float]:
        """
        Get the maximum value which may be returned for a pixel on the detector.

        For example, for a 16-bit detector, the maximum value should be 2^16 or 65536.

        :returns: Maximum value allowed for a pixel.
        """
        return 2**16

    def start(self, n: int=0) -> None:
        """
        Begin acquisition of spectra.

        The parameter `n` determines the number of spectra to acquire.
        If `n` is a positive integer then `n` spectra will be acquired, buffered, and passed to all
        functions subscribed to callbacks using :meth:`register_acquisition_callback` at the
        conclusion of the acquisition process.
        In this case, the acquisition of an individual spectrum will not cause callbacks to the
        functions registered using :meth:`register_spectrum_callback`.
        Alternatively, if `n` is zero or less (the default), then acquisition will continue
        indefinitely until the :meth:`stop` method is called.
        Callbacks will be made to subscribers to :meth:`register_spectrum_callback` on each
        spectrum acquisition event, but no callbacks will be made once the acquisition is stopped.

        :param n: Number of spectra to acquire, or `0` to acquire indefinitely.
        """
        pass

    def stop(self, wait: bool=False) -> None:
        """
        Stop any current acquisition process.

        :param wait: Wait (block) until the acquisition finishes before returning.
        """
        pass


class DetectorStatusPanel(QtWidgets.QFrame):
    """
    Panel to insert into the Hardware Status window to show status of the Detector's hardware
    connection.
    """
    
    #: Qt Signal to indicate the devices have changed in some way and the panel requires refreshing.
    devices_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Detector:")
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
        for i, d in enumerate(config.data["hardware"]["detector"]):
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
statuspanel = DetectorStatusPanel

# Create default config entries for device(s) if required
config.add_defaults(tomlkit.parse(_default_config))

# None is a placeholder for closed/missing devices
devices = [None for _ in config.data["hardware"]["detector"]]

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    # Look for valid plugin classes
    try:
        plugin_paths = [ os.path.join(d, "detector") for d in config.data["directories"]["plugins"] ]
        plugin_paths = [ d for d in plugin_paths if os.access(d, os.R_OK) ]
        _loader = pluginlib.PluginLoader(group="detector", modules=["detector"], paths=plugin_paths)
    except Exception as ex:
        raise RuntimeError(f"Error loading detector plugin classes: {ex}")
    _log.info(f"Available detector plugin classes: {', '.join(list(_loader.plugins['Detector']))}")


    # Add ourselves to the list of active hardware modules
    hw.modules[__name__] = sys.modules[__name__]
