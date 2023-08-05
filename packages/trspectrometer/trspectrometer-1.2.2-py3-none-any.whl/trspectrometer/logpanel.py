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

import logging
import time
import os

from PySide6 import QtGui, QtWidgets
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QFileDialog, QMessageBox

import configuration as config

class LogPanel(QtWidgets.QFrame, loadUiType(__file__.split(".py")[0] + ".ui")[0]):

    """
    A UI panel which attaches to the root logger to display logged messages.

    Note that this panel is unable to display log messages which occur prior to
    its initialisation.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Configure the log handler with default format etc.
        self.handler = logging.StreamHandler(self)
        self.handler.terminator = ""
        self.handler.setFormatter(logging.Formatter(fmt=logging.BASIC_FORMAT))
        # Attach to the root logger
        logging.getLogger().addHandler(self.handler)

        # Finish setting up UI and connect signals
        self.log.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.wordwrapCheckBox.clicked.connect(self._wordwrap_clicked)
        self.savePushButton.clicked.connect(self._save_clicked)

    #def __del__(self):
        # TODO: Disconnect ourselves as a handler for the logger

    def write(self, data):
        """
        Write data to the log window.

        Primarily used to handle input provided from the ``StreamHandler``.
        """
        try:
            # TODO: Temporary workaround until logger disconnection implemented
            self.log.append(data)
        except: pass

    def flush(self):
        """
        Does nothing, but required to support stream-like behaviour.
        """
        pass

    def _wordwrap_clicked(self):
        if self.wordwrapCheckBox.isChecked():
            self.log.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        else:
            self.log.setWordWrapMode(QtGui.QTextOption.NoWrap)


    def _save_clicked(self):
        """
        Save the current log text out to a file.
        """
        initial_dir = config.data["directories"]["data"]
        datecode = time.strftime("%y%m%d_%H%M%S", time.localtime())
        initial_filename = os.path.join(initial_dir, f"{datecode}_trspectrometer.log")
        filename, _ = QFileDialog.getSaveFileName(self, "Save Log", initial_filename, "Log Files (*.log)")
        if filename:
            try:
                with open(filename, "x") as f:
                    f.write(self.log.toPlainText().encode("utf-8").decode('cp1252'))
            except Exception as ex:
                QMessageBox.warning(self, "TRSpectrometer", f"Unable to save log to file at:\n{filename}")

