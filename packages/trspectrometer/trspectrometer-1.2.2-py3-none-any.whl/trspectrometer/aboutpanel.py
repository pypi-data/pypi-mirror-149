#!/usr/bin/env python3

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

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import loadUiType

import trspectrometer

class AboutPanel(QtWidgets.QDialog, loadUiType(__file__.split(".py")[0] + ".ui")[0]):

    """
    Show a dialog box with information about the application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.versionLabel.setText(f"Version {trspectrometer.__version__}")