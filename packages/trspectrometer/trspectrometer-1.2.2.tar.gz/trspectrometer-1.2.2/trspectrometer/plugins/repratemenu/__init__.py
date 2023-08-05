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
Module to add a menu to change the laser repetition rate configuration option.

It will create a "Configure" menu (if not already present), and add to it a "Laser Reprate" menu
containing a selection of rates. The listed rates are determined by a setting in the config file.
The defaults are:

.. code-block:: none

    [repratemenu]
    rates = [500, 1000, 2000, 2500, 3333.3333, 5000, 10000]

where the numbers in the ``rates`` list are in Hz.

To use this plugin module, ensure ``"repratemenu"`` is present in the :ref:`configuration file`'s
``load=[...]`` list inside the :ref:`plugins` section.

Note this does not change the actual output of any laser system, it just configures the software to
work with the selected repetition rate. If your laser system only ever runs at a single rate, then
this plugin is unnecessary. Instead, simply set the correct rate in the :ref:`configuration file`'s
``laser_reprate = ...`` entry under the ``[hardware]`` section.
"""

import sys
import logging

import tomlkit
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QActionGroup

import configuration as config
from signalstorage import signals


#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
# Laser Reprate Menu configuration
# Parameters are:
#  rates : list of numeric laser repetition rates in Hz
[repratemenu]
rates = [500, 1000, 2000, 2500, 3333.3333, 5000, 10000]
"""
# Create default config entries if required
config.add_defaults(tomlkit.parse(_default_config))

_log = logging.getLogger(__name__)

# Reference to the MainWindow stored in the config module
_mw = config.mainwindow


def update_reprate(value):
    """
    Update the configuration with an updated laser repetition rate, in Hz.

    Note this does not change the actual laser repetition rate, instead it configures the software
    to work with the given value, which should match that of the input laser.

    :param value: Laser repetition rate in Hz.
    """
    # Update value in config file, emit signal to notify other interested components
    value = float(value)
    config.data["hardware"]["laser_reprate"] = value
    _log.info(f"Configuration updated to work with a laser repetition rate of {value:0.0f} Hz.")
    signals.laser_reprate_changed.emit()


# Bypass this code block if module was imported by sphinx documentation generation utility
if not "sphinx" in sys.argv[0]:

    # Create the "Configure" menu if it doesn't already exist.
    if not hasattr(_mw, "menuConfigure"):
        _mw.menuConfigure = QMenu("Confi&gure")
        _mw.menubar.insertMenu(_mw.menuView.menuAction(), _mw.menuConfigure)

    # Add a reprate sub-menu to the configure menu
    _mw.menuReprate = _mw.menuConfigure.addMenu("Laser &Reprate")
    _actiongroup = QActionGroup(_mw.menuReprate)
    for v in config.data["repratemenu"]["rates"]:
        action = _mw.menuReprate.addAction(f"{v:0.0f} Hz")
        action.setCheckable(True)
        action.setChecked(round(v) == round(config.data["hardware"]["laser_reprate"]))
        action.triggered.connect(lambda checked=False, value=v,: update_reprate(value))
        _actiongroup.addAction(action)

    # Handle acquisition start signals, disable the menu.
    signals.acquisition_started.connect(lambda: _mw.menuReprate.setEnabled(False))
    # Handle acquisition stop signals, re-enable the menu.
    signals.acquisition_stopped.connect(lambda error: _mw.menuReprate.setEnabled(True))

    
