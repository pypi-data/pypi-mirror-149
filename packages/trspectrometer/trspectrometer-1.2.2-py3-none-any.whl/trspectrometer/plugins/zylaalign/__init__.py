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
Module for assisting with aligning the input into an Andor Zyla camera.

This adds a "Zyla" tab to the main window which displays the raw image data from the camera's
sensor. A spectral display also shows the intensity of light falling on the central rows of pixels
which are used for reading data from the camera during high-speed acquisition.

Viewing the raw sensor data allows for the focussing of the input beam onto the slit of the
spectrograph, as well as adjustment of the beam's vertical alignment so that the light is incident
on the central rows which are used for acquiring spectral data.

Note that acquiring the full sensor image is relatively slow, so many laser shots will be collected
for each frame. This means that the intensity of the input light will likely need to be reduced
significantly using a neutral density filter, or else expect saturation of the detector.

.. figure:: ../images/zylaalign-image.png
    :alt: Alignment panel for the Andor Zyla camera, in full image mode.

    Raw image data from the Andor Zyla's sensor is shown in the top panel. The horizontal lines
    indicate the bounds of the active pixel rows used during spectral acquisition. The bottom panel
    shows the average intensity of light hitting these active pixels.

A second mode is available which displays only the active pixel rows which are used during normal
spectral acquisition. Once the vertical alignment has been performed using the ``Full image`` mode,
switching the view area to the ``Active rows`` option will display the image data using the normal
triggering and exposure settings. Saturated pixels will be highlighted in red, indicating that the
intensity of the probe light should be reduced. This can be done either by decreasing the power of
the seed beam, or by attenuating the white-light using a neutral density filter.

.. figure:: ../images/zylaalign-activerows.png
    :alt: Alignment panel for the Andor Zyla camera, in active rows mode.

    Raw image data from the active pixel rows of the sensor is shown in the top panel. The red
    colour highlights pixels which are at or near saturation point. The bottom panel shows the
    average intensity of light hitting these pixels, which is used to generate the spectral data.

Some options for the panel are available in the configuration file. The default values are:

.. code-block:: none

    [zylaalign.image]
    exposure = 0.001
    height = 1080

The ``exposure`` parameter is the camera exposure time, in seconds. The ``height`` parameter
determines the number of vertical pixels to acquire for each image when using the full image mode.
"""

import sys
from time import monotonic

import tomlkit
from PySide6.QtUiTools import loadUiType
import pyqtgraph as pg

import configuration as config
from .zylaalignpanel import ZylaAlign

#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
[zylaalign]
[zylaalign.ui]
viewarea = "full"

[zylaalign.image]
exposure = 0.001
height = 1080
"""

# Create default config entries if required
config.add_defaults(tomlkit.parse(_default_config))

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    
    # Add the scope panel tab to the main window
    config.mainwindow.zylaAlign = ZylaAlign()
    config.mainwindow.tabWidget.insertTab(1, config.mainwindow.zylaAlign, "Zyla")
