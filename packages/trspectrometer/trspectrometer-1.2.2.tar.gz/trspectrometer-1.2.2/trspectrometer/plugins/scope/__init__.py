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
Module for the Scope panel for real-time display of spectra.
"""

import os
import sys

import tomlkit

import configuration as config
from .scopepanel import ScopePanel


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
[scope]
[scope.ui]
mode = "raw"
samples = 50
reference_raw = ""
reference_deltaA = ""

[scope.crosshair]
# An RGBA colour for the crosshairs
colour = [0, 255, 0, 128]
"""

# Create default config entries if required
config.add_defaults(tomlkit.parse(_default_config))

# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:
    
    # Add the scope panel tab to the main window
    config.mainwindow.scopePanel = ScopePanel()
    config.mainwindow.tabWidget.insertTab(1, config.mainwindow.scopePanel, "Scope")
