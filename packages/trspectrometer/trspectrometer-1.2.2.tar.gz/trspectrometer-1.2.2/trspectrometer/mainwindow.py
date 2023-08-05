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

# TODO: We want to load the log window before hardware detection etc,
# but at the moment that's really messy. It should be possible to clean it up
# so we're not loading modules inside __init__() etc.

import os
import sys
import importlib
import argparse
import traceback
import logging

from PySide6 import QtWidgets
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal
import zarr

# This is a workaround for loadUiType not finding the resource _rc.py inside the package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from signalstorage import signals
from busydialog import BusyDialog

_log = logging.getLogger(__name__)


def exception_handler(extype, value, tb):
    """
    Global handler for exceptions.
    Not particularly smart, but stops crashes from minor recoverable errors.
    The exception details are sent to the log.
    """
    logging.error("Caught an unhandled exception:\n  " + "  ".join(traceback.format_exception(extype, value, tb)).rstrip("\n"))
sys.excepthook = exception_handler

class MainWindow(QtWidgets.QMainWindow, loadUiType(__file__.split(".py")[0] + ".ui")[0]):
    """
    Main window for the various components of the spectrometer software.
    """

    #: Signal to trigger a status bar message.
    show_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the show_message signal to display message on the status bar
        self.show_message.connect(self.statusbar.showMessage)

        # Note we are doing imports as late as possible so that the logPanel
        # is able to catch and display as much as possible from the logger.

        # Intialise logging system
        from logpanel import LogPanel
        self.logPanel = LogPanel()
        self.actionLog.triggered.connect(lambda: _show_and_activate(self.logPanel))

        # Initialise configuration
        import configuration as config

        # Initialise data panel
        import datastorage as ds
        self.ds = ds
        from datapanel import DataPanel
        self.dataPanel = DataPanel(self)
        self.tabWidget.insertTab(1, self.dataPanel, "Data")

        # Initialise about panel
        from aboutpanel import AboutPanel
        self.aboutPanel = AboutPanel(self)

        # Start with data panel selected
        self.tabWidget.setCurrentIndex(1)

        # Connect UI signals
        self.actionNew.triggered.connect(self._new_clicked)
        self.actionOpen.triggered.connect(self._open_clicked)
        self.actionSaveAs.triggered.connect(self._save_clicked)
        self.actionImportRawData.triggered.connect(self._import_raw_data_clicked)
        self.actionExportRawDataAverage.triggered.connect(self._export_raw_data_average_clicked)
        self.actionAbout.triggered.connect(self._about_clicked)
        self.actionHardwareStatus.triggered.connect(self._hardwarestatus_clicked)

        # Start new data set
        self._new_clicked()

    def closeEvent(self, event):
        """Handler for window close event."""
        if not self.dataPanel.close():
            # Data acquisition in progress, close cancelled
            event.ignore()
            return
        self.logPanel.close()
        try:
            self.hardwarestatusPanel.close()
        except:
            pass
        import hardware as hw
        hw.close()
        event.accept()

    def _new_clicked(self):
        """Handler for the File->New menu item."""
        if not self.ds.prompt_unsaved(parent=self):
            return
        self.ds.new_raw_zarr(location=None)
        signals.data_changed.emit(False) # Don't update UI controls
        self.actionSaveAs.setEnabled(False)
        self.menuExport.setEnabled(False)
        self.actionProperties.setEnabled(False)
        self.statusbar.showMessage("New data set ready.")

    def _open_clicked(self):
        """Handler for the File->Open menu item."""
        if not self.ds.prompt_unsaved(parent=self):
            return
        try:
            dirname = self.ds.open_zarr(parent=self)
        except Exception as ex:
            _log.error(f"{ex}")
            QMessageBox.critical(self, "Error opening data directory", f"{ex}")
            return
        if not dirname: return
        signals.data_changed.emit(True)
        self.actionSaveAs.setEnabled(True)
        self.menuExport.setEnabled(True)
        self.actionProperties.setEnabled(True)
        msg = f"Data opened from {dirname}"
        _log.info(msg)
        self.statusbar.showMessage(msg)

    def _save_clicked(self):
        """Handler for the File->Save menu item."""
        try:
            dirname = self.ds.save_zarr(parent=self)
        except Exception as ex:
            _log.error(f"{ex}")
            QMessageBox.critical(self, "Error saving data directory", f"{ex}")
            return
        if dirname == None: return
        msg = f"Data saved to {dirname}"
        _log.info(msg)
        self.statusbar.showMessage(msg)

    def _import_raw_data_clicked(self):
        """Handler for the File->Import->Raw Data menu item."""
        if not self.ds.prompt_unsaved(parent=self):
            return
        try:
            filename, data = self.ds.import_raw(parent=self)
        except Exception as ex:
            _log.error(f"{ex}")
            QMessageBox.critical(self, "Error importing raw data", f"{ex}")
            return
        if not filename: return
        self.ds.d = data
        self.ds.t = zarr.group()
        signals.data_changed.emit(True)
        self.actionSaveAs.setEnabled(True)
        self.menuExport.setEnabled(True)
        self.actionProperties.setEnabled(True)
        msg = f"Data imported from {filename}"
        _log.info(msg)
        self.statusbar.showMessage(msg)

    def _export_raw_data_average_clicked(self):
        """Handler for the File->Export->Raw Data Average menu item."""
        try:
            filename = self.ds.export_raw_average(parent=self)
        except Exception as ex:
            _log.exception(f"{ex}")
            QMessageBox.critical(self, "Error exporting raw data average", f"{ex}")
            return
        if filename is None: return
        msg = f"Data exported to {filename}"
        _log.info(msg)
        self.statusbar.showMessage(msg)

    def _about_clicked(self):
        self.aboutPanel.exec_()

    def _hardwarestatus_clicked(self):
        import hardware as hw
        self.hardwarestatusPanel = hw.HardwareStatusPanel()
        self.hardwarestatusPanel.show()
        self.hardwarestatusPanel.activateWindow()

    def _hardware_init(self):
        import hardware as hw
        BusyDialog(parent=self, modal=True, title="Initialising Hardware", label="Initialising hardware devices...", task=lambda dialog: hw.init())


def _show_and_activate(widget):
    """Show and activate a given QWidget."""
    widget.show()
    widget.activateWindow()


def main():
    """Run the launcher application."""

    # Respond to command line arguments
    argparser = argparse.ArgumentParser(description="Run the TRSpectrometer application.")
    argparser.add_argument("--hardware", help="Perform hardware detection and initialisation.", nargs=1, choices=["true", "false"])
    argparser.add_argument("--loglevel", help="Verbosity of the log output.", nargs=1, choices=["critical", "error", "warning", "info", "debug"], default=["info"])
    args = argparser.parse_args()
    if not args.hardware is None:
        args.hardware = (args.hardware[0] == "true")
    logging.basicConfig(level=args.loglevel[0].upper())

    # Initialise the main application window
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    import configuration as config
    config.mainwindow = mw

    # Load plugin modules from user plugin or builtin plugin locations
    for p in config.plugin_dirs()[::-1]:
        sys.path.insert(0, os.path.abspath(p))
    if config.data["plugins"]["load"]:
        _log.info(f"Plugin search path is: {sys.path}")
    for p in config.data["plugins"]["load"]:
        try:
            _log.info(f"Loading plugin module: {p}")
            importlib.import_module(p, package=__package__)
        except ModuleNotFoundError:
            _log.error(f"Module not found for plugin: {p}")
        except Exception:
            _log.exception(f"Error loading plugin module: {p}")
    
    # Adjust config based on provided command line arguments
    if not args.hardware is None:
        config.data["hardware"]["init_hardware"] = args.hardware
    
    # Initialise hardware if requested
    if config.data["hardware"]["init_hardware"]:
        config.mainwindow._hardware_init()
    else:
        _log.info("Hardware not initialised. Set \"init_hardware = true\" in configuration file, or run with \"--hardware=true\" command line parameter to enable automatic initialisation.")

    # Show main application window and run Qt event loop
    config.mainwindow.showMaximized()
    config.mainwindow.activateWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
