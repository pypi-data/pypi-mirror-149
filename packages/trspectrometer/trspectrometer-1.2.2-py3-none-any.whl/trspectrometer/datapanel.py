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

import os
import warnings

import tomlkit
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Signal
from PySide6.QtCore import QRectF
import numpy as np

import pyqtgraph as pg
import configuration as config
import hardware as hw
import datastorage as ds
from qtwidgets import FlowLayout

from signalstorage import signals
from utils import si_unit_factor

#: Default settings to place in configuration file if not existing already.
_default_config = \
"""
[datapanel]

[datapanel.ui]
start = 0.0
steptype = "Variable"
stepsize = 1.0
window = 1000.0
steps = [[24, 2.0], [30, 0.1], [50, 0.5], [50, 2.0], [200, 25.0]]
scancount = 5
method = "Dummy Stepped"
density = 100

[datapanel.ui.metadata]
sample = ""
pump = ""
operator = ""
note = ""

[datapanel.crosshair]
# An RGBA colour for the crosshairs
colour = [0, 255, 0, 255]
# An RGBA colour for the crosshairs when highlighted
highlight = [255, 0, 0, 255]

[datapanel.scangradient]
# Gradient start and stop RGBA colours to use for individual scan traces
start = [0, 64, 255, 128]
stop  = [192, 0, 0, 128]
# Highlight RGBA colour to use when highlighting a specific scan trace
highlight = [192, 192, 192, 255]
"""

class DataPanel(QtWidgets.QWidget, loadUiType(__file__.split(".py")[0] + ".ui")[0]):
    """
    UI panel to facilitate the collection and viewing of data.

    :param parent: Parent of the QWidget.
    """    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Set defaults in config if needed
        config.add_defaults(tomlkit.parse(_default_config))

        # Listen for when data set is changed
        signals.data_changed.connect(self._data_changed)
        signals.raw_data_updated.connect(self._data_updated)
        signals.raw_selection_changed.connect(self._raw_selection_changed)
        signals.acquisition_started.connect(self._acquisition_started)
        signals.acquisition_stopped.connect(self._acquisition_complete)

        # Setup pyqtgraph plot areas
        pg.setConfigOptions(imageAxisOrder='row-major', antialias=True)
        self.overview = self.glw.addPlot(row=0, col=0, enableMenu=False)
        self.overview.setLabels(bottom=f"Wavelength ({config.data['rawdata']['units']['wavelength']})", left=f"Delay ({config.data['rawdata']['units']['time']})")
        [ self.overview.getAxis(ax).setZValue(10) for ax in self.overview.axes ] # Draw axes and ticks above image/data
        self.overview_composite_image = pg.ImageItem()
        self.overview_images = []
        self.overview.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.crosshairx = pg.InfiniteLine(pos=0.0, angle=90, movable=True, pen=config.data["datapanel"]["crosshair"]["colour"], hoverPen=config.data["datapanel"]["crosshair"]["highlight"])
        self.crosshairy = pg.InfiniteLine(pos=0.0, angle=0, movable=True, pen=config.data["datapanel"]["crosshair"]["colour"], hoverPen=config.data["datapanel"]["crosshair"]["highlight"])
        self.crosshairx.setZValue(9)
        self.crosshairy.setZValue(9)
        self.overview.addItem(self.crosshairx, ignoreBounds=True)
        self.overview.addItem(self.crosshairy, ignoreBounds=True)
        self.crosshair = pg.ROI(pos=(0.0, 0.0), size=(0.0, 0.0), handlePen=config.data["datapanel"]["crosshair"]["colour"], handleHoverPen=config.data["datapanel"]["crosshair"]["highlight"])
        self.crosshair.addTranslateHandle((0.0, 0.0))
        self.overview.addItem(self.crosshair, ignoreBounds=True)
        self.crosshair.sigRegionChanged.connect(self._crosshair_changed)
        self.crosshairx.sigPositionChanged.connect(self._crosshairx_changed)
        self.crosshairy.sigPositionChanged.connect(self._crosshairy_changed)
        # Indicies of currently selected wavelength, time
        self.selected_w_i = 0
        self.selected_t_i = 0

        # Colourmap bar
        self.cbar = pg.HistogramLUTItem(self.overview_composite_image)
        self.cbar.gradient.restoreState({"mode": "rgb",
            "ticks": [(0.00, (0, 0, 0)),
                      (0.25, (0, 0, 128)),
                      (0.50, (144, 0 , 0)),
                      (0.85, (224, 224, 0)),
                      (1.00, (255, 255, 255))]})
        self.cbar.axis.setStyle(autoExpandTextSpace=False)
        self.cbar.sigLookupTableChanged.connect(self._cbar_changed)
        self.cbar.sigLevelsChanged.connect(self._cbar_changed)
        self.glw.addItem(self.cbar, row=0, col=2, rowspan=2)

        # Slice along the y direction, kinetics for a given wavelength
        self.xslice = self.glw.addPlot(row=0, col=1, enableMenu=False)
        self.xslice.showGrid(x=True, y=True)
        self.xslice.addLegend(offset=(-10, 5))
        self.xslice.setLabels(bottom=f"Delay ({config.data['rawdata']['units']['time']})", left=f"{config.data['rawdata']['units']['data']}")
        self.xslice.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.xslice_plot = self.xslice.plot(pen=(255, 255, 0), name=f"Temporal slice @ 000.0 {config.data['rawdata']['units']['wavelength']}")
        self.xslice_plot.setZValue(9)
        #self.latest_scan_plot = self.xslice.plot(pen=0.3, name="Latest scan")
        #self.latest_scan_plot.setZValue(8)
        self.xslice_scan_plots = []
        self.xslice_crosshair = pg.InfiniteLine(pos=0.0, angle=90, movable=True, pen=config.data["datapanel"]["crosshair"]["colour"], hoverPen=config.data["datapanel"]["crosshair"]["highlight"])
        self.xslice.addItem(self.xslice_crosshair, ignoreBounds=True)
        self.xslice_crosshair.sigPositionChanged.connect(self._xslice_crosshair_changed)

        # Slice along the x direction, spectrum for a given time
        self.yslice = self.glw.addPlot(row=1, col=0, enableMenu=False)
        self.yslice.showGrid(x=True, y=True)
        self.yslice.addLegend(offset=(-10, 5))
        self.yslice.setLabels(bottom=f"Wavelength ({config.data['rawdata']['units']['wavelength']})", left=f"{config.data['rawdata']['units']['data']}")
        self.yslice.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.yslice_plot = self.yslice.plot(pen=(255, 255, 0), name=f"Spectral slice @ 0000.0 {config.data['rawdata']['units']['time']}")
        self.yslice_plot.setZValue(9)
        #self.latest_acq_plot = self.yslice.plot(pen=0.33, name="Latest spectrum")
        #self.latest_acq_plot.setZValue(8)
        self.yslice_scan_plots = []
        self.yslice_crosshair = pg.InfiniteLine(pos=0.0, angle=90, movable=True, pen=config.data["datapanel"]["crosshair"]["colour"], hoverPen=config.data["datapanel"]["crosshair"]["highlight"])
        self.yslice.addItem(self.yslice_crosshair, ignoreBounds=True)
        self.yslice_crosshair.sigPositionChanged.connect(self._yslice_crosshair_changed)

        # Link axes
        self.overview.getViewBox().sigRangeChangedManually.connect(self._link_axes_overview)
        self.xslice.getViewBox().sigRangeChangedManually.connect(self._link_axes_xslice)
        self.yslice.setXLink(self.overview)

        # Bottom right panel containing list of scans
        self.scansWidget = DataPanelScansWidget()
        self.proxyWidget = QtWidgets.QGraphicsProxyWidget()
        self.proxyWidget.setWidget(self.scansWidget)
        self.glw.addItem(self.proxyWidget, row=1, col=1)

        # Set up the step size table
        self.stepmodel = QtGui.QStandardItemModel(0, 2)
        self.stepmodel.dataChanged.connect(self._step_table_changed)
        self.stepmodel.rowsInserted.connect(self._step_table_changed)
        self.stepmodel.rowsRemoved.connect(self._step_table_changed)
        self.stepTableView.setModel(self.stepmodel)
        self.stepTableView.setItemDelegate(StepsSpinBoxDelegate())
        self._reset_step_table()

        # Connect signals
        self.startDoubleSpinBox.valueChanged.connect(self._start_value_changed)
        self.fixedStepDoubleSpinBox.valueChanged.connect(self._step_value_changed)
        self.windowDoubleSpinBox.valueChanged.connect(self._window_value_changed)
        self.stepComboBox.currentIndexChanged.connect(self._steptype_changed)
        self.addStepPushButton.clicked.connect(self._addstep_clicked)
        self.removeStepPushButton.clicked.connect(self._removestep_clicked)
        self.startPushButton.clicked.connect(self._start_clicked)
        self.sampleLineEdit.editingFinished.connect(self._update_metadata)
        self.pumpLineEdit.editingFinished.connect(self._update_metadata)
        self.operatorLineEdit.editingFinished.connect(self._update_metadata)
        self.noteLineEdit.editingFinished.connect(self._update_metadata)

        # Acquisition hardware won't be initialised yet, disable controls
        self._enable_acquisition_controls(False)

        self._load_ui_config()

        # Reference to any currently running acquisition
        self._acquisition = None


    def _link_axes_overview(self):
        self.xslice.setXRange(*self.overview.viewRange()[1])


    def _link_axes_xslice(self):
        self.overview.setYRange(*self.xslice.viewRange()[0])


    def _crosshair_changed(self):
        """
        Handle changes to crosshair target position.
        """
        pos = self.crosshair.pos()
        if not self.crosshairx.value() == pos[0]:
            self.crosshairx.setPos(pos[0])
        if not self.crosshairy.value() == pos[1]:
            self.crosshairy.setPos(pos[1])


    def _crosshairx_changed(self):
        """
        Handle changes to crosshair x position.
        """
        self.crosshair.setPos(self.crosshairx.value(), self.crosshairy.value())
        if not self.yslice_crosshair.value() == self.crosshairx.value():
            self.yslice_crosshair.setPos(self.crosshairx.value())
        new_i = np.argmin(np.abs(ds.d["raw/wavelength"][:] - self.crosshairx.value()))
        if new_i != self.selected_w_i:
            self.selected_w_i = new_i
            #self._acquisition_lock.acquire()
            # Update individual scan traces
            for scan_i, plotitem in enumerate(self.xslice_scan_plots):
                scan_data = ds.d["raw/data"][scan_i]
                nonzero_t_i = np.any(scan_data, axis=1)
                plotitem.setData(ds.d["raw/time"][:][nonzero_t_i], scan_data[nonzero_t_i,self.selected_w_i])
            # Update average trace
            nonzero_t_i = np.any(ds.t["raw/data_avg"], axis=1)
            self.xslice_plot.setData(ds.d["raw/time"][:][nonzero_t_i], ds.t["raw/data_avg"][:][nonzero_t_i,self.selected_w_i])
            #self._acquisition_lock.release()
            self._update_legend()


    def _crosshairy_changed(self):
        """
        Handle changes to crosshair y position.
        """
        self.crosshair.setPos(self.crosshairx.value(), self.crosshairy.value())
        if not self.xslice_crosshair.value() == self.crosshairy.value():
            self.xslice_crosshair.setPos(self.crosshairy.value())
        new_i = np.argmin(np.abs(ds.d["raw/time"][:] - self.crosshairy.value()))
        if new_i != self.selected_t_i:
            self.selected_t_i = new_i
            #self._acquisition_lock.acquire()
            # Update individual scan traces
            for scan_i, plotitem in enumerate(self.yslice_scan_plots):
                plotitem.setData(ds.d["raw/wavelength"], ds.d["raw/data"][scan_i,self.selected_t_i,:])
            # Update average trace
            self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
            #self._acquisition_lock.release()
            self._update_legend()


    def _xslice_crosshair_changed(self):
        """
        Handle changes to the x-slice crosshair position.
        """
        if not self.xslice_crosshair.value() == self.crosshairy.value():
            self.crosshairy.setPos(self.xslice_crosshair.value())


    def _yslice_crosshair_changed(self):
        """
        Handle changes to the y-slice crosshair position.
        """
        if not self.yslice_crosshair.value() == self.crosshairx.value():
            self.crosshairx.setPos(self.yslice_crosshair.value())


    def _crosshair_reset(self):
        """
        Reset the position and limits of the cursor/crosshairs to match currently loaded data.
        """
        # Restrict bounds of crosshairs
        self.crosshair.maxBounds = QRectF(ds.d["raw/wavelength"][0], ds.d["raw/time"][0], ds.d["raw/wavelength"][-1] - ds.d["raw/wavelength"][0], ds.d["raw/time"][-1] - ds.d["raw/time"][0])
        self.crosshairx.setBounds((ds.d["raw/wavelength"][0], ds.d["raw/wavelength"][-1]))
        self.crosshairy.setBounds((ds.d["raw/time"][0], ds.d["raw/time"][-1]))
        self.xslice_crosshair.setBounds((ds.d["raw/time"][0], ds.d["raw/time"][-1]))
        self.yslice_crosshair.setBounds((ds.d["raw/wavelength"][0], ds.d["raw/wavelength"][-1]))
        # Position the crosshairs
        self.selected_w_i = int(ds.d["raw/wavelength"].shape[0]/2)
        self.crosshairx.setPos(ds.d["raw/wavelength"][self.selected_w_i])
        self.selected_t_i = 0
        self.crosshairy.setPos(ds.d["raw/time"][self.selected_t_i])
        self.crosshair.setPos(ds.d["raw/wavelength"][self.selected_w_i], ds.d["raw/time"][self.selected_t_i])
        self.xslice_crosshair.setPos(ds.d["raw/time"][self.selected_t_i])
        self.yslice_crosshair.setPos(ds.d["raw/wavelength"][self.selected_w_i])


    def _axes_reset(self):
        """
        Reset the plots with new zoom and limits to match currently loaded data.
        """
        wavelength_scale = (ds.d["raw/wavelength"][-1] - ds.d["raw/wavelength"][0])/(ds.d["raw/wavelength"].shape[0]-1) if ds.d["raw/wavelength"].shape[0] > 1 else 1.0
        delaytime_scale = (ds.d["raw/time"][-1] - ds.d["raw/time"][0])/(ds.d["raw/time"].shape[0]-1) if ds.d["raw/time"].shape[0] > 1 else 1.0
        self.overview.setLimits(xMin=ds.d["raw/wavelength"][0] - wavelength_scale/2, xMax=ds.d["raw/wavelength"][-1] + wavelength_scale/2,
                                yMin=ds.d["raw/time"][0] - delaytime_scale/2, yMax=ds.d["raw/time"][-1] + delaytime_scale/2)
        self.xslice.setLimits(xMin=ds.d["raw/time"][0] - delaytime_scale/2, xMax=ds.d["raw/time"][-1] + delaytime_scale/2,
                              yMin=-2**16, yMax=2**16)
        self.yslice.setLimits(xMin=ds.d["raw/wavelength"][0] - wavelength_scale/2, xMax=ds.d["raw/wavelength"][-1] + wavelength_scale/2,
                                yMin=-2**16, yMax=2**16)
        self.overview.autoRange(pg.ViewBox.XYAxes)
        self.xslice.autoRange(pg.ViewBox.XYAxes)
        self.yslice.autoRange(pg.ViewBox.XYAxes)
        self.overview.enableAutoRange(pg.ViewBox.XYAxes)
        self.xslice.enableAutoRange(pg.ViewBox.XYAxes)
        self.yslice.enableAutoRange(pg.ViewBox.XYAxes)
        self._update_legend()


    def _update_legend(self):
        """
        Update the plot legends to match current values of cursor crosshairs.
        """
        # Select units for each axis
        try:
            wl_units = ds.d.raw.wavelength.attrs["units"]
        except:
            wl_units = config.data['rawdata']['units']['wavelength']
        try:
            t_units = ds.d.raw.time.attrs["units"]
        except:
            t_units = config.data['rawdata']['units']['time']
        try:
            self.xslice.legend.items[0][1].setText(f"Temporal slice λ = {np.round(ds.d['raw/wavelength'][self.selected_w_i].astype(np.float64), 1)} {wl_units}")
            self.yslice.legend.items[0][1].setText(f"Spectral slice t = {np.round(ds.d['raw/time'][self.selected_t_i].astype(np.float64), 1)} {t_units}")
        except Exception:
            # Probably zarr bounds check error when selected index out of range when loading new data
            pass


    def _reset_step_table(self):
        """
        Clear and re-initialize the variable step table.
        """
        self.stepmodel.clear()
        try:
            t_unit = ds.d["raw/time"].attrs["units"]
        except:
            t_unit = config.data['rawdata']['units']['time']
        self.stepmodel.setHorizontalHeaderLabels(["#", f"Window ({t_unit})", f"Step ({t_unit})"])
        self.stepTableView.setColumnWidth(0, 35)
        self.stepTableView.setColumnWidth(1, 100)
        self.stepTableView.setColumnWidth(2, 65)


    def _steptype_changed(self, value):
        """
        Handler for the fixed/variable combo box change.

        :param value: Index of selected entry in the combo box.
        """
        self.fixedStepDoubleSpinBox.setEnabled(not value)
        self.windowDoubleSpinBox.setEnabled(not value)
        self.variableControls.setEnabled(bool(value))
        if value:
            self._update_table_totals()
        else:
            self._update_fixedstep_totals()


    def _addstep_clicked(self):
        """
        Handler for the step table's "add" button click.
        """
        self._add_step_table_row()


    def _removestep_clicked(self):
        """
        Handler for the step table's "remove" button click.
        """
        selected_row = self.stepTableView.selectionModel().currentIndex().row()
        if selected_row == -1: selected_row = self.stepmodel.rowCount() - 1
        self.stepmodel.takeRow(selected_row)
        self.stepTableView.selectionModel().clear()
        self.removeStepPushButton.setEnabled(self.stepmodel.rowCount() > 1)
        self.addStepPushButton.setEnabled(True)


    def _add_step_table_row(self, window=100.0, step=1.0):
        """
        Add a new row to the end of the variable step table.

        :param window: Value to use for window size column.
        :param step: Value to use for step size column.
        """
        windowitem = QtGui.QStandardItem(f"{window:f}".rstrip("0").rstrip(".") + " @")
        windowitem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        stepitem = QtGui.QStandardItem(f"{step:f}".rstrip("0").rstrip("."))
        countitem = QtGui.QStandardItem(f"{int(window/step) if not step == 0.0 else '?'}")
        countitem.setEditable(False)
        self.stepmodel.appendRow([countitem, windowitem, stepitem])
        # Limit number of rows
        self.addStepPushButton.setEnabled(self.stepmodel.rowCount() < 20)
        self.removeStepPushButton.setEnabled(self.stepmodel.rowCount() > 1)


    def _step_table_changed(self, *args):
        """
        Handle changes to the variable step table entries.
        """
        self._update_table_totals()


    def _update_table_totals(self):
        """
        Update step and time total display to match current entries in the variable step table.
        """
        stepwindow = 0.0
        stepcount = 0
        for row in range(self.stepmodel.rowCount()):
            count = int(self.stepmodel.data(self.stepmodel.index(row, 0)).split(" ")[0])
            stepcount += count
            stepwindow += count*float(self.stepmodel.data(self.stepmodel.index(row, 2)).split(" ")[0])
        self._update_totals_label(stepwindow, stepcount)

    
    def _update_fixedstep_totals(self):
        """
        Update step and time total display to match current values in fixed step UI controls.
        """
        stepwindow = self.windowDoubleSpinBox.value()
        stepcount = int(stepwindow/self.fixedStepDoubleSpinBox.value())
        self._update_totals_label(stepwindow, stepcount)


    def _update_totals_label(self, stepwindow, stepcount):
        """
        Update the label showing the total acquisition time window and number of steps/data points.

        Highlight in red if maximum delay required exceeds that possible using current delay hardware.
        """
        try:
            t_unit = ds.d["raw/time"].attrs["units"]
        except:
            t_unit = config.data['rawdata']['units']['time']
        self.steptotalLabel.setText(f"{stepwindow:.0f} {t_unit} / {stepcount} points")
        try:
            # Highlight in red if delay is unable to achieve required window size
            excess = stepwindow + self.startDoubleSpinBox.value() - (hw.modules["delay"].devices[0].max_delay()/si_unit_factor(t_unit))
            if excess > 0:
                self.steptotalLabel.setText(self.steptotalLabel.text() + f" (+{excess:.0f} {t_unit})")
                self.steptotalLabel.setStyleSheet("QLabel { color : red; }")
                self.steptotalLabel.setToolTip("Required acquisition time window exceeds the capability of the delay hardware. Time steps will be truncated.")
            else:
                self.steptotalLabel.setStyleSheet("")
                self.steptotalLabel.setToolTip("")
        except:
            pass


    def _start_value_changed(self, value):
        """
        Handle changes to the scan start time value.
        """
        # Highlight step totals if range no longer achievable
        if self.stepComboBox.currentIndex():
            # Variable step mode selected
            self._update_table_totals()
        else:
            # Fixed step mode selected
            self._update_fixedstep_totals()
        

    def _step_value_changed(self, value):
        """
        Handle changes to the scan fixed step size value.
        """
        self._update_fixedstep_totals()

    
    def _window_value_changed(self, value):
        """
        Handle changes to the scan window size value.
        """
        self._update_fixedstep_totals()


    def _data_changed(self, update_ui=False):
        """
        Perform a complete rebuild of plots when new data is loaded etc.

        Handler for the :data:`datastorage.SignalStorage.data_changed` signal.

        The ``update_ui`` parameter determines if the user interface controls should also be updated
        to match the data. The default is ``False``, which will update the plots but leave the UI
        controls as they are. This behaviour is suitable when a new data acquisition is started,
        which would be using the current UI settings. Using ``update_ui=True`` would be appropriate
        when loading a new data set in from disk, where the controls should be updated to reflect
        the settings used to collect the loaded data set.

        :param update_ui: Update the GUI controls to match the data.
        """
        # Generate average if needed
        if not "raw/data_avg" in ds.t:
            ds.t["raw/data_avg"] = ds.raw_data_average()

        # Remove old scan traces from xslice panel
        for plot in self.xslice_scan_plots:
            self.xslice.removeItem(plot)
        self.xslice_plot.setData()
        self.xslice_scan_plots = []
        # Remove old scan traces from yslice panel
        for plot in self.yslice_scan_plots:
            self.yslice.removeItem(plot)
        self.yslice_plot.setData()
        self.yslice_scan_plots = []
        # Remove overview images
        for img in self.overview_images:
            self.overview.removeItem(img)
        self.overview_images = []

        # Build new kinetic and spectral scan traces
        self.selected_w_i = int(ds.d["raw/wavelength"].shape[0]/2)
        self.selected_t_i = 0
        c_start = np.array(config.data["datapanel"]["scangradient"]["start"])
        c_stop = np.array(config.data["datapanel"]["scangradient"]["stop"])
        # Include all scans if excluded scans not specified yet
        if not "exclude_scans" in ds.t["raw"].attrs:
            ds.t["raw"].attrs["exclude_scans"] = []
        # Ensure any excluded scans are invisible
        scan_enabled_list = np.ones((ds.d["raw/data"].shape[0],), dtype=bool)
        scan_enabled_list[ds.t["raw"].attrs["exclude_scans"]] = False
        for i, scan_data in enumerate(ds.d["raw/data"]):
            # Compute colour in the gradient to use
            c = tuple((c_start + ((i/(ds.d["raw/data"].shape[0] - 1)) if ds.d["raw/data"].shape[0] > 1 else 0)*(c_stop - c_start)).astype(np.int64))
            nonzero_t_i = np.any(scan_data, axis=1)
            self.xslice_scan_plots.append(self.xslice.plot(ds.d["raw/time"][:][nonzero_t_i], scan_data[nonzero_t_i,self.selected_w_i], pen=c if scan_enabled_list[i] else None)) 
            self.yslice_scan_plots.append(self.yslice.plot(ds.d["raw/wavelength"], scan_data[self.selected_t_i,:], pen=c if scan_enabled_list[i] else None))
            # Store the assigned colour in the PlotItem so we can retrieve it later
            # This way we can toggle pen=None/pen=baseColor to hide an individual trace
            self.xslice_scan_plots[-1].baseColor = c
            self.yslice_scan_plots[-1].baseColor = c
            # Connect to click events
            self.xslice_scan_plots[-1].sigClicked.connect(self.scansWidget.highlight_scan)
            self.xslice_scan_plots[-1].curve.setClickable(True)
            self.yslice_scan_plots[-1].sigClicked.connect(self.scansWidget.highlight_scan)
            self.yslice_scan_plots[-1].curve.setClickable(True)
        # Update the scan selection checkboxes
        self.scansWidget.set_scans(list(zip(self.xslice_scan_plots, self.yslice_scan_plots)), checked=scan_enabled_list)
        
        # Update the average traces
        nonzero_t_i = np.any(ds.t["raw/data_avg"], axis=1)
        self.xslice_plot.setData(ds.d["raw/time"][:][nonzero_t_i], ds.t["raw/data_avg"][:][nonzero_t_i,self.selected_w_i])
        self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
        
        # Generate an image segment for each detected step size range
        steplist = ds.find_stepsizes(ds.d["raw/time"])
        # Wavelength axis should be fairly uniform and common to all segments
        wavelength_scale = (ds.d["raw/wavelength"][-1] - ds.d["raw/wavelength"][0])/(ds.d["raw/wavelength"].shape[0]-1) if ds.d["raw/wavelength"].shape[0] > 1 else 1.0
        # Ignore warning when an image contains all NaNs
        warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="All-NaN slice encountered")
        tslice_start = 0
        for i, (step_count, _) in enumerate(steplist):
            # Build slice indices for this segment
            tslice_end = tslice_start + step_count + (1 if i == 0 else 0)
            image = pg.ImageItem(ds.t["raw/data_avg"][tslice_start:tslice_end if tslice_end < ds.d["raw/time"].shape[0] else None])
            # Perhaps a bit hacky, but also store the time index range inside the ImageItem
            image.tslice_start = tslice_start
            image.tslice_end = tslice_end
            # TODO: Images don't look absolutely perfectly aligned, may be off-by one errors in indexing here...
            delaytime_scale = (ds.d["raw/time"][tslice_end if tslice_end < ds.d["raw/time"].shape[0] else -1] - ds.d["raw/time"][tslice_start])/(tslice_end - tslice_start) if (tslice_end - tslice_start) > 0 else 1.0
            tr = QtGui.QTransform()
            tr.translate(ds.d["raw/wavelength"][0] - wavelength_scale/2, ds.d["raw/time"][tslice_start] - delaytime_scale/2)
            tr.scale(wavelength_scale, delaytime_scale)
            image.setTransform(tr)
            image.setLookupTable(self.cbar.getLookupTable)
            self.overview.addItem(image)
            self.overview_images.append(image)
            tslice_start = tslice_end
        
        # Update colour bar (which links to the invisible composite image)
        # HistogramLUTItem doesn't automatically clear and update when linked image is None...
        self.cbar.plot.clear()
        self.cbar.setLevels(min=-1, max=1)
        self.cbar.update()
        # TODO: Can probably downsample this image data to get better performance
        self.overview_composite_image.setImage(ds.t["raw/data_avg"][:])
        
        
        # Update axes unit labels
        self.overview.setLabels(bottom=f"Wavelength ({ds.d['raw/wavelength'].attrs['units']})", left=f"Delay ({ds.d['raw/time'].attrs['units']})")
        self.xslice.setLabels(bottom=f"Delay ({ds.d['raw/time'].attrs['units']})", left=f"{ds.d['raw/data'].attrs['units']}")
        self.yslice.setLabels(bottom=f"Wavelength ({ds.d['raw/wavelength'].attrs['units']})", left=f"{ds.d['raw/data'].attrs['units']}")

        # Reset view
        self._axes_reset()
        self._crosshair_reset()

        # Enable save and export of data
        if config.mainwindow:
            config.mainwindow.actionSaveAs.setEnabled(True)
            config.mainwindow.menuExport.setEnabled(True)

        # If data was loaded from file, UI controls should be updated to match
        if update_ui:
            self._data_to_ui_config()


    def _raw_selection_changed(self):
        """
        Handle changes to the selection of displayed raw data traces.

        Generates new average of the currently selected traces.
        """
        # Compute new average traces and update
        ds.t["raw/data_avg"] = ds.raw_data_average()
        nonzero_t_i = np.any(ds.t["raw/data_avg"], axis=1)
        self.xslice_plot.setData(ds.d["raw/time"][:][nonzero_t_i], ds.t["raw/data_avg"][:][nonzero_t_i,self.selected_w_i])
        self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
        # Recompute overview image sections
        steplist = ds.find_stepsizes(ds.d["raw/time"])
        tslice_start = 0
        for i, (step_count, _) in enumerate(steplist):
            tslice_end = tslice_start + step_count + (1 if i == 0 else 0)
            self.overview_images[i].setImage(ds.t["raw/data_avg"][tslice_start:tslice_end if tslice_end < ds.d["raw/time"].shape[0] else None])
            tslice_start = tslice_end
        self._cbar_changed()


    def _cbar_changed(self):
        """
        Handle changes to the colour bar control.
        """
        for image in self.overview_images:
            image.setLookupTable(self.cbar.getLookupTable(n=512))
            image.setLevels(self.cbar.getLevels())


    def acquisition_plugins_changed(self):
        """
        Notify the DataPanel that the acquisition hardware plugins or status has changed.
        """
        self._enable_acquisition_controls()


    def delay_plugins_changed(self):
        """
        Notify the DataPanel that the delay hardware plugins or status has changed.
        """
        # TODO
        try:
            delay = hw.modules["delay"].devices[0]
            t_unit = ds.d["raw/time"].attrs["units"]
            self.startDoubleSpinBox.setMaximum(delay.max_delay()/si_unit_factor(t_unit))
            self.windowDoubleSpinBox.setMaximum(delay.max_delay()/si_unit_factor(t_unit))
        except:
            #print("Error setting delay limits.")
            pass


    def _enable_acquisition_controls(self, enable=None):
        """
        Enable relevant controls if acquisition methods available.

        :param enable: Force the enabling or disabling of controls.
        """
        # Remember the currently selected item
        old_item = self.methodComboBox.currentText()
        # Populate the method combo box
        self.methodComboBox.clear()
        if "acquisition" in hw.modules: 
            for d in hw.modules["acquisition"].devices:
                if d and d.is_initialised():
                    self.methodComboBox.addItem(d.name, d)
        # Re-select old item if it is still available
        if self.methodComboBox.findText(old_item) >= 0:
            self.methodComboBox.setCurrentText(old_item)
        else:
            # Or try to use previous one from config file
            self.methodComboBox.setCurrentText(config.data["datapanel"]["ui"]["method"])
        # Enable controls if an acquisition method is available
        if enable is None:
            enable = "acquisition" in hw.modules and any([d.is_initialised() for d in hw.modules["acquisition"].devices if d])
        self.timeGroupBox.setEnabled(enable)
        self.scansGroupBox.setEnabled(enable)
        self.metadataGroupBox.setEnabled(enable)
        self.startPushButton.setEnabled(enable)


    def _start_clicked(self):
        """
        Handle clicking of the start acquisition button.
        """
        if self._acquisition:
            # Acquisition in progress, act as stop button
            reply = QMessageBox.question(self, "TRSpectrometer", "Really stop the current data acquisition process?")
            if reply == QMessageBox.No:
                return
            self._acquisition.stop()
        else:
            if not ds.prompt_unsaved(parent=self):
                return
            d = self.methodComboBox.currentData()
            if not d.is_initialised():
                raise RuntimeWarning("Selected acquisition method is not available and ready.")
            self._acquisition = d
            self._acquisition.start()
            signals.acquisition_started.emit()
            

    def _acquisition_started(self):
        """
        Handle the signal for starting of acquisition. Disable controls etc.
        """
        self.startPushButton.setText("Stop")
        self.timeGroupBox.setEnabled(False)
        self.methodComboBox.setEnabled(False)
        self.densitySpinBox.setEnabled(False)
        config.mainwindow.menuDataset.setEnabled(False)
        for i in range(config.mainwindow.tabWidget.count()):
            config.mainwindow.tabWidget.setTabEnabled(i, i == config.mainwindow.tabWidget.currentIndex())
        self._save_ui_config()
        config.mainwindow.statusbar.showMessage("Acquisition started" + f" to {ds.d_path}" if ds.d_path else ".")


    def _acquisition_complete(self, error=None):
        """
        Handle the signal for completion of acquisition. Re-enable controls etc.
        """
        self._acquisition = None
        self.startPushButton.setText("Start")
        self.timeGroupBox.setEnabled(True)
        self.methodComboBox.setEnabled(True)
        self.densitySpinBox.setEnabled(True)
        config.mainwindow.menuDataset.setEnabled(True)
        for i in range(config.mainwindow.tabWidget.count()):
                config.mainwindow.tabWidget.setTabEnabled(i, True)
        if error:
            if isinstance(error, UserWarning):
                # Cancelled manually
                config.mainwindow.statusbar.showMessage("Acquisition stopped.")
                # TODO: Ask to remove incomplete scan?
            else:
                # Error occurred
                config.mainwindow.statusbar.showMessage("Error occurred during acquisition.")
                QtWidgets.QMessageBox.critical(self, "Data acquisition error", f"An error occurred during data acquisition:\n\n{error}")
        else:
            # Seems to have completed OK
            config.mainwindow.statusbar.showMessage("Acquisition complete.")
            ds.prompt_unsaved(parent=self)
        

    def _save_ui_config(self):
        """
        Save GUI control values out to configuration file.
        """
        config.data["datapanel"]["ui"]["start"] = self.startDoubleSpinBox.value()
        config.data["datapanel"]["ui"]["steptype"] = self.stepComboBox.currentText()
        config.data["datapanel"]["ui"]["stepsize"] = self.fixedStepDoubleSpinBox.value()
        config.data["datapanel"]["ui"]["window"] = self.windowDoubleSpinBox.value()
        # Extract step count and sizes from table
        steps = []
        for row in range(self.stepmodel.rowCount()):
            steps.append([
                int(self.stepmodel.data(self.stepmodel.index(row, 0)).split(" ")[0]),   # Count
                float(self.stepmodel.data(self.stepmodel.index(row, 2)).split(" ")[0])  # Step size
            ])
        config.data["datapanel"]["ui"]["steps"] = steps
        config.data["datapanel"]["ui"]["scancount"] = self.countSpinBox.value()
        config.data["datapanel"]["ui"]["method"] = self.methodComboBox.currentText()
        config.data["datapanel"]["ui"]["density"] = self.densitySpinBox.value()
        config.data["datapanel"]["ui"]["metadata"]["sample"] = self.sampleLineEdit.text()
        config.data["datapanel"]["ui"]["metadata"]["pump"] = self.pumpLineEdit.text()
        config.data["datapanel"]["ui"]["metadata"]["operator"] = self.operatorLineEdit.text()
        config.data["datapanel"]["ui"]["metadata"]["note"] = self.noteLineEdit.text()
    

    def _load_ui_config(self):
        """
        Load GUI control values from configuration file.
        """
        self.startDoubleSpinBox.setValue(config.data["datapanel"]["ui"]["start"])
        self.stepComboBox.setCurrentText(config.data["datapanel"]["ui"]["steptype"])
        self.fixedStepDoubleSpinBox.setValue(config.data["datapanel"]["ui"]["stepsize"])
        self.windowDoubleSpinBox.setValue(config.data["datapanel"]["ui"]["window"])
        for stepcount, stepsize in config.data["datapanel"]["ui"]["steps"]:
            self._add_step_table_row(stepcount*stepsize, stepsize)
        self.countSpinBox.setValue(config.data["datapanel"]["ui"]["scancount"])
        method = config.data["datapanel"]["ui"]["method"]
        if self.methodComboBox.findText(method) >= 0:
            self.methodComboBox.setCurrentText()
        else:
            self.methodComboBox.setCurrentIndex(0)
        self.densitySpinBox.setValue(config.data["datapanel"]["ui"]["density"])
        self.sampleLineEdit.setText(config.data["datapanel"]["ui"]["metadata"]["sample"])
        self.pumpLineEdit.setText(config.data["datapanel"]["ui"]["metadata"]["pump"])
        self.operatorLineEdit.setText(config.data["datapanel"]["ui"]["metadata"]["operator"])
        self.noteLineEdit.setText(config.data["datapanel"]["ui"]["metadata"]["note"])
        # Enable/disable some controls based on fixed/variable step
        if self.stepComboBox.currentIndex() == 0:
            # Fixed step
            self.fixedStepDoubleSpinBox.setEnabled(True)
            self.windowDoubleSpinBox.setEnabled(True)
            self.variableControls.setEnabled(False)
            self._update_fixedstep_totals()
        else:
            # Variable step
            self.fixedStepDoubleSpinBox.setEnabled(False)
            self.windowDoubleSpinBox.setEnabled(False)
            self.variableControls.setEnabled(True)
            self._update_table_totals()


    def _data_to_ui_config(self):
        """
        Adjust GUI controls to match the currently loaded data set.
        """
        t_unit = ds.d["raw/time"].attrs["units"]

        # Absolute start time should be stored in metadata
        try:
            self.startDoubleSpinBox.setValue(ds.d["raw"].attrs["start"])
        except:
            pass
        self.startDoubleSpinBox.setSuffix(f" {t_unit}")

        # Determine the step sizes for the time axis
        steplist = ds.find_stepsizes(ds.d["raw/time"])
        # Adjust some controls based on whether fixed or variable step sizes
        if len(steplist) == 0:
            # Empty data set, anything to do?
            pass
        elif len(steplist) == 1:
            # One step size, so fixed steps
            self.stepComboBox.setCurrentIndex(0)
            self.fixedStepDoubleSpinBox.setEnabled(True)
            self.fixedStepDoubleSpinBox.setValue(steplist[0][1])
            self.windowDoubleSpinBox.setEnabled(True)
            self.variableControls.setEnabled(False)
        else:
            # Variable step size
            self.stepComboBox.setCurrentIndex(1)
            self.fixedStepDoubleSpinBox.setEnabled(False)
            self.windowDoubleSpinBox.setEnabled(False)
            self.variableControls.setEnabled(True)
            # Update the step list table
            self._reset_step_table()
            for stepcount, stepsize in steplist:
                self._add_step_table_row(stepcount*stepsize, stepsize)
        self.fixedStepDoubleSpinBox.setSuffix(f" {t_unit}")

        self.stepmodel.setHorizontalHeaderLabels(["#", f"Window ({t_unit})", f"Step ({t_unit})"])
        
        # Window from time axis values
        self.windowDoubleSpinBox.setValue(ds.d["raw/time"][-1] - ds.d["raw/time"][0])
        self.windowDoubleSpinBox.setSuffix(f" {t_unit}")

        # If not an empty data set, use number of scans as scan count
        if ds.d["raw/data"].shape[0] > 0:
             self.countSpinBox.setValue(ds.d["raw/data"].shape[0])
    
        # Select acquisition method if available
        try:
            method = ds.d["raw"].attrs["acquisition_method"]
            if self.methodComboBox.findText(method) >= 0:
                self.methodComboBox.setCurrentText(method)
        except: pass

        # Metadata fields
        try:
            self.sampleLineEdit.setText(ds.d["raw"].attrs["sample"])
        except:
            self.sampleLineEdit.setText("")
        try:
            self.pumpLineEdit.setText(ds.d["raw"].attrs["pump"])
        except:
            self.pumpLineEdit.setText("")
        try:
            self.operatorLineEdit.setText(ds.d["raw"].attrs["operator"])
        except:
            self.operatorLineEdit.setText("")
        try:
            self.noteLineEdit.setText(ds.d["raw"].attrs["note"])
        except:
            self.noteLineEdit.setText("")


    def _data_updated(self, scans, times, wls):
        """
        Update plots with new changes or additions to the data set.

        The parameters ``scans``, ``times``, ``wls`` are lists of array indices where the data has
        been changed. These can be used to restrict what needs to be redrawn for efficiency. Setting
        these parameters to ``None`` indicates that potentially all elements should be redrawn.

        Handler for the :data:`datastorage.SignalStorage.data_updated` signal.

        :param scans: List of scan indices which have changed.
        :param times: List of time indices which have changed.
        :param wls: List of wavelength indices which have changed.
        """
        # Generate average
        ds.t["raw/data_avg"] = ds.raw_data_average()

        # Detect and handle the addition of scans
        if ds.d["raw/data"].shape[0] > len(self.xslice_scan_plots):
            # Ensure any excluded scans are invisible
            scan_enabled_list = np.ones((ds.d["raw/data"].shape[0],), dtype=bool)
            scan_enabled_list[ds.t["raw"].attrs["exclude_scans"]] = False
            for s_i in range(len(self.xslice_scan_plots), ds.d["raw/data"].shape[0]):
                scan_data = ds.d["raw/data"][s_i]
                # Temporary colour to use for the trace
                c = (1.0, 1.0, 1.0)
                nonzero_t_i = np.any(scan_data, axis=1)
                self.xslice_scan_plots.append(self.xslice.plot(ds.d["raw/time"][:][nonzero_t_i], scan_data[nonzero_t_i,self.selected_w_i], pen=c if scan_enabled_list[s_i] else None)) 
                self.yslice_scan_plots.append(self.yslice.plot(ds.d["raw/wavelength"], scan_data[self.selected_t_i,:], pen=c if scan_enabled_list[s_i] else None))
                # Connect to click events
                self.xslice_scan_plots[-1].sigClicked.connect(self.scansWidget.highlight_scan)
                self.xslice_scan_plots[-1].curve.setClickable(True)
                self.yslice_scan_plots[-1].sigClicked.connect(self.scansWidget.highlight_scan)
                self.yslice_scan_plots[-1].curve.setClickable(True)
            # Need to recompute colour gradient now
            c_start = np.array(config.data["datapanel"]["scangradient"]["start"])
            c_stop = np.array(config.data["datapanel"]["scangradient"]["stop"])
            for s_i, scan_data in enumerate(ds.d["raw/data"]):
                # Compute colour in the gradient to use
                c = tuple((c_start + ((s_i/(ds.d["raw/data"].shape[0] - 1)) if ds.d["raw/data"].shape[0] > 1 else 0)*(c_stop - c_start)).astype(np.int64))
                self.xslice_scan_plots[s_i].baseColor = c
                self.yslice_scan_plots[s_i].baseColor = c
                if scan_enabled_list[s_i]:
                    self.xslice_scan_plots[s_i].setPen(c)
                    self.yslice_scan_plots[s_i].setPen(c)
            # Update the scan selection checkboxes
            self.scansWidget.set_scans(list(zip(self.xslice_scan_plots, self.yslice_scan_plots)), checked=scan_enabled_list)

        for s_i, scan_data in enumerate(ds.d["raw/data"]):
            if scans is None or s_i in scans:
                self.xslice_scan_plots[s_i].setData(ds.d["raw/time"][:], scan_data[:,self.selected_w_i])
                self.yslice_scan_plots[s_i].setData(ds.d["raw/wavelength"], scan_data[self.selected_t_i,:])
        
        # Update the average traces
        self.xslice_plot.setData(ds.d["raw/time"][:], ds.t["raw/data_avg"][:][:,self.selected_w_i])
        self.yslice_plot.setData(ds.d["raw/wavelength"], ds.t["raw/data_avg"][self.selected_t_i,:])
        
        # Update colour bar (which links to the invisible composite image)
        # TODO: Can probably downsample this image data to get better performance
        self.overview_composite_image.setImage(ds.t["raw/data_avg"][:])

        for image in self.overview_images:
            # If the image slice doesn't contain any time indexes which were changed, we can skip it
            if not (times is None or any([x in range(image.tslice_start, image.tslice_end)] for x in times)):
                continue
            image.setImage(ds.t["raw/data_avg"][image.tslice_start:image.tslice_end if image.tslice_end < ds.d["raw/time"].shape[0] else None], levels=self.overview_composite_image.getLevels())
        
        
    def get_acquisition_params(self):
        """
        Get a tuple containing the acquisition parameters as configured in the user interface.

        The returned data is in the form of ``(scan_count, data_density, start_time, [[step_count, step_size]], metadata)``.

        The ``metadata`` is a dictionary containing the text in the metadata fields.

        :returns: Tuple containing acquisition parameters.
        """
        steps = []
        if self.stepComboBox.currentText() == "Variable":
            # Variable step size
            for row in range(self.stepmodel.rowCount()):
                steps.append([
                    int(self.stepmodel.data(self.stepmodel.index(row, 0)).split(" ")[0]),   # Count
                    float(self.stepmodel.data(self.stepmodel.index(row, 2)).split(" ")[0])  # Step size
                ])
        else:
            # Fixed step size
            steps.append([
                int(self.windowDoubleSpinBox.value()/self.fixedStepDoubleSpinBox.value()),  # Count
                float(self.fixedStepDoubleSpinBox.value())  # Step size
            ])
        metadata = {
            "start" : self.startDoubleSpinBox.value(),
            "sample" : self.sampleLineEdit.text(),
            "pump" : self.pumpLineEdit.text(),
            "operator" : self.operatorLineEdit.text(),
            "note" : self.noteLineEdit.text()
        }
        return self.countSpinBox.value(), self.densitySpinBox.value(), self.startDoubleSpinBox.value(), steps, metadata


    def _update_metadata(self):
        """
        Update the metadata in the temporary data storage with values from the text boxes.
        """
        ds.t["raw"].attrs.update({
            "start" : self.startDoubleSpinBox.value(),
            "sample" : self.sampleLineEdit.text(),
            "pump" : self.pumpLineEdit.text(),
            "operator" : self.operatorLineEdit.text(),
            "note" : self.noteLineEdit.text()
        })


    def closeEvent(self, event):
        """
        Handler for window close event.
        """
        # Check for acquisition in progress
        if self._acquisition:
            reply = QMessageBox.question(self, "TRSpectrometer", "Really stop the current data acquisition process?")
            if reply == QMessageBox.No:
                event.ignore()
            else:
                self._acquisition.stop()
        # Check for unsaved data                
        if not ds.prompt_unsaved(parent=self):
            # Unsaved data, user chose to cancel close
            event.ignore()
        else:
            event.accept()
        

class StepsSpinBoxDelegate(QtWidgets.QItemDelegate):
    """
    Delegate used to spawn spinbox controls for editing cells in the QTableView.
    """

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QDoubleSpinBox(parent)
        editor.setDecimals(2)
        editor.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)

        if index.column() == 1:
            # Step window
            editor.setRange(0.05, 10000)
        elif index.column() == 2:
            # Step size
            editor.setRange(0.05, 500)
        return editor

    def setEditorData(self, spinBox, index):
        value = float(index.model().data(index, QtCore.Qt.EditRole).split()[0])
        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, f"{value:f}".rstrip("0").rstrip(".") + (" @" if index.column() == 1 else ""), QtCore.Qt.EditRole)
        # Update the step count as well
        window = float(index.model().data(model.index(index.row(), 1), QtCore.Qt.EditRole).split()[0])
        step = float(index.model().data(model.index(index.row(), 2), QtCore.Qt.EditRole).split()[0])
        model.setData(model.index(index.row(), 0), f"{int(window/step)}")

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class DataPanelScansWidget(QtWidgets.QFrame, loadUiType(os.path.join(os.path.dirname(__file__), "datapanelscans.ui"))[0]):
    """
    The QWidget which will be inserted into the GraphicsLayout to display a
    list of checkboxes to disable or enable individiual scans. 
    """

    def __init__(self, parent=None, plotitems=[], label="Scan #{}"):
        super().__init__(parent)
        self.setupUi(self)
        self.scrollWidget.setLayout(FlowLayout())
        self.items = {}
        self.highlighted_item = None
        self.set_scans(plotitems, label=label)
    
    def set_scans(self, plotitems, checked=None, label="Scan #{}"):
        # Remove any existing checkboxes
        for checkbox in self.items.keys():
            self.scrollWidget.layout().removeWidget(checkbox)
            checkbox.setParent(None)
        self.items = {}
        # All checkboxes are checked if not specified
        if checked is None:
            checked = [True]*len(plotitems)
        # Create new checkboxes for given PlotItems
        for i, plotitem in enumerate(plotitems):
            # Ensure plotitem is a tuple
            try:
                plotitem = tuple(plotitem)
            except TypeError:
                plotitem = (plotitem,)
            checkbox = QtWidgets.QCheckBox(label.format(i + 1))
            checkbox.setChecked(bool(checked[i]))
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self._checkbox_clicked(state, checkbox))
            checkbox.installEventFilter(self)
            pen = plotitem[0].baseColor
            # Choose text colour depending on brightness of background
            c_text = "black" if (pen[0] + pen[1] + pen[2])*pen[3] > 97920 else "#d0d0d0"
            checkbox.setStyleSheet(f"QCheckBox {{ background: rgba({pen[0]},{pen[1]},{pen[2]},{pen[3]/255}); color: {c_text} }}")
            self.scrollWidget.layout().addWidget(checkbox)
            self.items[checkbox] = plotitem

    def _checkbox_clicked(self, state, checkbox):
        for plotitem in self.items[checkbox]:
            plotitem.setPen(plotitem.baseColor if state else None)
        # Update the list of excluded scans
        excluded_scans = []
        for i, checkbox in enumerate(self.items.keys()):
            if not checkbox.isChecked():
                excluded_scans.append(i)
        ds.t["raw"].attrs["exclude_scans"] = excluded_scans
        # Notify any listeners of the change to selection
        signals.raw_selection_changed.emit()

    def eventFilter(self, target, event):
        """Event filter to handle mouse movements over scan selection checkboxes and highlight matching scan trace."""
        if not type(target) == QtWidgets.QCheckBox: return False
        if target.isChecked() and (event.type() == QtCore.QEvent.HoverEnter or event.type() == QtCore.QEvent.HoverMove):
            self.highlight_scan(self.items[target][0])
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.highlight_scan(None)
        return False

    def highlight_scan(self, plotitem):
        # Check if item already highlighted
        if self.highlighted_item is not None and self.highlighted_item == plotitem: return
        # Don't respond if plotitem is hidden
        if plotitem is not None and type(plotitem.opts["pen"]) == QtGui.QPen and plotitem.opts["pen"].style() == QtCore.Qt.NoPen: return
        # Remove any existing highlight
        if self.highlighted_item in self.items:
            c = self.items[self.highlighted_item][0].baseColor
            c_text = "black" if (c[0] + c[1] + c[2])*c[3] > 97920 else "#d0d0d0"
            self.highlighted_item.setStyleSheet(f"QCheckBox {{ background: rgba({c[0]},{c[1]},{c[2]},{c[3]/255}); color: {c_text} }}")
            for p in self.items[self.highlighted_item]:
                p.setPen(p.baseColor if self.highlighted_item.isChecked() else None)
            self.highlighted_item = None
        # Allow None to remove highlight
        if plotitem is None: return
        # Loop through items looking for plotitem
        for checkbox, plotitems in self.items.items():
            if plotitem in plotitems:
                # Highlight the checkbox and both plotitems
                c = config.data["datapanel"]["scangradient"]["highlight"]
                checkbox.setStyleSheet(f"QCheckBox {{ background: rgba({c[0]},{c[1]},{c[2]},{c[3]/255}); }}")
                for p in plotitems:
                    p.setPen(c)
                self.highlighted_item = checkbox

