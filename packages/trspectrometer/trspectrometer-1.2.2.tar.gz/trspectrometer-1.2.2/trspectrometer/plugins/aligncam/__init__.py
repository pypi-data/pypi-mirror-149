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
Module for management of simple camera devices used for beam alignment.

Loading this plugin module will add the "Align" tab to the main window which shows the
:data:`~trspectrometer.plugins.aligncam.alignmentpanel.AlignmentPanel` and is useful during the
:ref:`alignment` process.

To load the aligncam plugin module, ensure ``"aligncam"`` is present in the :ref:`configuration
file`'s ``load=[...]`` list inside the :ref:`plugins` section.

Currently, only webcam devices are supported using the OpenCV library. The devices can be added
using sections in the :ref:`configuration file`, for example:

.. code-block:: toml

    # Alignment camera list
    # Each entry specifies an alignment camera
    #   name (string) : Friendly name for the camera to use in the application
    #   filter (string) : Regular expression to match the camera device name, eg. "Logitech"
    #   index (int) : If multiple devices match the filter, index of the match
    #   focus (int) : Fixed focus point, ranging from 0 (infinity) to 51 (macro).
    [[hardware.aligncam]]
    name = "Alignment 1"
    filter = ""
    index = 0
    focus = 49

Multiple camera devices can be specified by including multiple ``[[hardware.aligncam]]`` sections.
The double rectangular brackets around ``[[hardware.aligncam]]`` indicate that multiple sections
are permitted.
"""

import os
import sys

import tomlkit
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal

from . import cv2camera
from .alignmentpanel import AlignmentPanel

import configuration as config
import hardware as hw


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
[alignment]

[alignment.ui]
cameraindex = 0
auto = false

[[alignment.ui.rois]]
pos = [600, 300]
size = [75, 75]
angle = 0

[[alignment.ui.rois]]
pos = [700, 400]
size = [75, 75]
angle = 0
"""

#: QWidget class type to use for displaying hardware status.
statuspanel = None

#: List of configured alignment camera devices.
devices = []

#: List of functions to call when device list is refreshed.
_change_callbacks = set()


def init():
    """
    Initialise the alignment cameras.
    """
    # First close any opened devices
    close()
    # Initialise the camera module
    cv2camera.init()
    # Notify callbacks of device refresh
    for cb in _change_callbacks.copy(): cb()


def add_change_callback(callback_function):
    """
    Register a function to be called when the list of alignment camera devices is refreshed.

    :param callback_function: Function to call when devices are refreshed.
    """
    global _change_callbacks
    if callable(callback_function):
        _change_callbacks.add(callback_function)


def remove_change_callback(callback_function):
    """
    Unregister a callback function added using ``add_change_callback()``.

    :param callback_function: Function to unregister.
    """
    global _change_callbacks
    if callback_function in _change_callbacks:
        _change_callbacks.remove(callback_function)


def close():
    """
    Close any used alignment camera devices.
    """
    global devices
    for cam in devices:
        cam.close()
    devices = []
    # Notify callbacks of device close
    for cb in _change_callbacks.copy(): cb()


class AlignmentCameraStatusPanel(QtWidgets.QFrame):
    """
    Panel to insert into the Hardware Status window to show status of the camera's hardware
    connection.
    """
    
    #: Qt Signal to indicate the devices have changed in some way and the panel requires refreshing.
    devices_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel("Alignment Camera:")
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
        
        if devices:
            # Build the list of devices
            for row, cam in enumerate(devices):
                self.grid.addWidget(QtWidgets.QLabel(cam.name), row, 0)
                self.grid.addWidget(QtWidgets.QLabel(cam.description), row, 1)
                # TODO: Should be able to handle no instance of class instead of checking for presence of vidcap
                if cam.vidcap is None:
                    w = QtWidgets.QLabel("ERROR")
                    w.setStyleSheet("QLabel { color : red; }")
                else:
                    w = QtWidgets.QLabel("OK")
                    w.setStyleSheet("QLabel { color : green; }")
                self.grid.addWidget(w, row, 2, QtCore.Qt.AlignRight)
        else:
            w = QtWidgets.QLabel("Missing or uninitialised")
            w.setStyleSheet("QLabel { color : orange; }")
            self.grid.addWidget(w, 0, 2, QtCore.Qt.AlignRight)


# Point to the correct widget class for displaying the hardware status panel
statuspanel = AlignmentCameraStatusPanel

# Add ourselves to the list of active hardware modules
hw.modules[__name__] = sys.modules[__name__]

# Create default config entries for the ui elements if required
config.add_defaults(tomlkit.parse(_default_config))

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    print(sys.argv)
    # Add the alignmentpanel tab to the main window
    config.mainwindow.alignmentPanel = AlignmentPanel(config.mainwindow)
    config.mainwindow.tabWidget.insertTab(0, config.mainwindow.alignmentPanel, "Align")
