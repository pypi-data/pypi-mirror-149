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

import os
import sys
import logging
import warnings
from time import sleep, monotonic, strftime, localtime
from threading import Thread, Event


from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Signal
import numpy as np

import pyqtgraph as pg
import configuration as config
from signalstorage import signals
import hardware as hw
import datastorage as ds
from utils import AcquisitionError, AcquisitionAbortedWarning, no_infs, status_message, si_unit_factor


class ScopePanel(QtWidgets.QWidget, loadUiType(__file__.split(".py")[0] + ".ui")[0]):

    """
    UI panel to view realtime data from the detector device.

    Currently only uses the first delay, chopper, interface, and detector devices. Data can be
    viewed as raw signal from the detector, or as a change in absorbance (ΔA) signal.

    :param parent: Parent of the QWidget.
    """

    _data_received = Signal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._log = logging.getLogger(__name__)

        # Configure plot area
        self.plot = self.glw.addPlot(enableMenu=False)
        self.plot.showGrid(x=True, y=True)
        self.plot.addLegend()
        self.zeroline = pg.InfiniteLine(pos=0.0, angle=0, pen=(64, 64, 64), movable=False)
        self.plot.addItem(self.zeroline)
        self.reference_raw = pg.PlotDataItem(pen=(96, 96, 96), name="Loaded")
        self.reference_deltaA = pg.PlotDataItem(pen=(96, 96, 96), name="Loaded")
        self.reference_pinned = pg.PlotDataItem(pen=(192, 0, 0), name="Pinned")
        self.spectrum = self.plot.plot(pen=(255, 255, 0), name="Signal")
        self.plot.setLabels(left="Intensity (a.u.)", bottom="Wavelength (nm)")
        # Cursor labels
        self.cursor_label = pg.LabelItem(justify="right")
        self.glw.addItem(self.cursor_label, row=1, col=0)
        # Cursor crosshair
        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=config.data["scope"]["crosshair"]["colour"])
        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=config.data["scope"]["crosshair"]["colour"])
        self.plot.addItem(self.vline, ignoreBounds=True)
        self.plot.addItem(self.hline, ignoreBounds=True)
        # Install signalproxy to filter mouse move events
        self.sigproxy = pg.SignalProxy(self.plot.scene().sigMouseMoved, rateLimit=60, slot=self._mouse_moved)
        # Catch mouse exit plot events
        self.glw.installEventFilter(self)

        # Restore UI settings
        self._load_ui_config()

        # Connect signals
        self.rawRadioButton.toggled.connect(self._mode_changed)
        self.delayDoubleSpinBox.valueChanged.connect(self._delay_changed)
        self.beginPushButton.clicked.connect(self._begin_pressed)
        self.decPushButton.clicked.connect(self._dec_pressed)
        self.incPushButton.clicked.connect(self._inc_pressed)
        self.endPushButton.clicked.connect(self._end_pressed)
        self.enablePushButton.clicked.connect(self._enable_pressed)
        self.savePushButton.clicked.connect(self._save_pressed)
        self.pinPushButton.clicked.connect(self._pin_pressed)
        self.loadPushButton.clicked.connect(self._load_pressed)
        self._data_received.connect(self._set_spectrum_data)

        # Background acquisition thread and stop signal event
        self._acq_thread = None
        self._acq_stop = Event()

        # Reference to detector and interface currently in use
        self._detector = None
        self._interface = None

        # Used to limit frame rate
        self._last_update_time = monotonic()
        self._update_interval = 0.033


    def showEvent(self, event):
        """
        Handle the Qt event when widget is shown.

        :param event: ``QEvent`` describing the event.
        """
        # Subscribe to delay device changes if delay module loaded
        if "delay" in hw.modules and not hw.modules["delay"].devices[0] is None:
            hw.modules["delay"].add_change_callback(self._delay_devices_changed)
        self._delay_devices_changed()
        # Subscribe to chopper device changes if chopper module loaded
        if "chopper" in hw.modules and not hw.modules["chopper"].devices[0] is None:
            hw.modules["chopper"].add_change_callback(self._chopper_devices_changed)
        self._chopper_devices_changed()
        self.start()
        # Be aware of laser reprate changes
        signals.laser_reprate_changed.connect(self._reprate_changed)


    def hideEvent(self, event):
        """
        Handle the Qt event when widget is hidden.

        :param event: ``QEvent`` describing the event.
        """
        # Don't care about laser reprate changes any more
        signals.laser_reprate_changed.disconnect(self._reprate_changed)
        self.stop()
        # Unsubscribe from delay device changes if delay module loaded
        if "delay" in hw.modules and not hw.modules["delay"].devices[0] is None:
            hw.modules["delay"].remove_change_callback(self._delay_devices_changed)
        # Unsubscribe from chopper device changes if chopper module loaded
        if "chopper" in hw.modules and not hw.modules["chopper"].devices[0] is None:
            hw.modules["chopper"].remove_change_callback(self._chopper_devices_changed)
        self._save_ui_config()


    def _mouse_moved(self, event):
        """
        Handle mouse movements over plot, update cursor position and labels.
        """
        pos = event[0]
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.getViewBox().mapSceneToView(pos)
            #index = int(mousePoint.x())
            #if index > 0 and index < len(data1):
            #    label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            self.vline.setPen(config.data["scope"]["crosshair"]["colour"])
            self.vline.setPos(mousePoint.x())
            self.hline.setPen(config.data["scope"]["crosshair"]["colour"])
            self.hline.setPos(mousePoint.y())
            self.cursor_label.setText(f"Cursor at {mousePoint.x():0.1f} nm = {mousePoint.y():g}")
        else:
            self.vline.setPen([0, 0, 0, 0])
            self.hline.setPen([0, 0, 0, 0])
            self.cursor_label.setText("")


    def eventFilter(self, obj, event):
        if obj == self.glw:
            if event.type() == QtCore.QEvent.Type.Leave:
                # Hide crosshair when mouse leaves the plot window
                self.vline.setPen([0, 0, 0, 0])
                self.hline.setPen([0, 0, 0, 0])
                self.cursor_label.setText("")
        return False


    def _delay_devices_changed(self):
        """Notify that delay devices have changed state."""
        if "delay" in hw.modules and not hw.modules["delay"].devices[0] is None and hw.modules["delay"].devices[0].is_initialised():
            try:
                # Update delay display to match current delay setting
                self.delayDoubleSpinBox.blockSignals(True)
                si_f = si_unit_factor(ds.d["raw/time"].attrs["units"])
                self.delayDoubleSpinBox.setMinimum(hw.modules["delay"].devices[0].min_delay()/si_f)
                self.delayDoubleSpinBox.setMaximum(hw.modules["delay"].devices[0].max_delay()/si_f)
                self.delayDoubleSpinBox.setValue(hw.modules["delay"].devices[0].get_target()/si_f)
                self.delayDoubleSpinBox.setSuffix(f" {ds.d['raw/time'].attrs['units']}")
                self.delayDoubleSpinBox.blockSignals(False)
                self.delayGroupBox.setEnabled(True)
                # Set a sensible delay movement speed
                hw.modules["delay"].devices[0].set_velocity(2e-9)      # 2ns/s
                hw.modules["delay"].devices[0].set_acceleration(2e-8)  # 20ns/s/s
            except: 
                self._log.error("Unable to update GUI with delay status.")
                self.delayGroupBox.setEnabled(False)
        else:
            self.delayGroupBox.setEnabled(False)


    def _chopper_devices_changed(self):
        """Notify that chopper devices have changed state."""
        if "chopper" in hw.modules and not hw.modules["chopper"].devices[0] is None and hw.modules["chopper"].devices[0].is_initialised():
            try:
                # Update chopper display to match current settings
                if hw.modules["chopper"].devices[0].get_enabled():
                    self.enablePushButton.setChecked(True)
                    self.enablePushButton.setText("Disable")
                else:
                    self.enablePushButton.setChecked(False)
                    self.enablePushButton.setText("Enable")
                self.chopperGroupBox.setEnabled(True)
            except: 
                self._log.error("Unable to update GUI with chopper status.")
                self.chopperGroupBox.setEnabled(False)
        else:
            self.chopperGroupBox.setEnabled(False)


    def _mode_changed(self):
        """
        Handle acquisition mode changes.
        """
        self.stop()
        self._update_reference_spectrum()
        self.plot.removeItem(self.reference_pinned)
        self.pinPushButton.setChecked(False)
        self.samplesSpinBox.setEnabled(not self.rawRadioButton.isChecked())
        self.start()


    def _update_reference_spectrum(self):
        """
        Show/hide appropriate reference spectrum and update UI control state depending on
        the currently selected mode.
        """
        if self.rawRadioButton.isChecked():
            self.plot.removeItem(self.reference_deltaA)
            if self.reference_raw.getData()[0] is None:
                # No saved spectrum data loaded
                self.loadPushButton.setChecked(False)
                self.loadPushButton.setText("Load")
                self.plot.removeItem(self.reference_raw)
            else:
                # Saved spectrum data loaded
                self.loadPushButton.setChecked(True)
                self.loadPushButton.setText("Unload")
                self.plot.addItem(self.reference_raw)
                self.reference_raw.setZValue(-5)
        else:
            self.plot.removeItem(self.reference_raw)
            if self.reference_deltaA.getData()[0] is None:
                # No saved spectrum data loaded
                self.loadPushButton.setChecked(False)
                self.loadPushButton.setText("Load")
                self.plot.removeItem(self.reference_deltaA)
            else:
                # Saved spectrum data loaded
                self.loadPushButton.setChecked(True)
                self.loadPushButton.setText("Unload")
                self.plot.addItem(self.reference_deltaA)
                self.reference_deltaA.setZValue(-5)


    def _reprate_changed(self):
        """
        Handle changes to laser reprate if currently acquiring.
        """
        self.stop()
        self.start()
        

    def start(self):
        """
        Start acquiring spectra.
        """
        # Check if required devices are available and ready
        if not ("interface" in hw.modules and not hw.modules["interface"].devices[0] is None and hw.modules["interface"].devices[0].is_initialised() and
                "detector" in hw.modules and not hw.modules["detector"].devices[0] is None and hw.modules["detector"].devices[0].is_initialised()):
            msg = "Unable to start scope acquisition due to missing hardware."
            self._log.info(msg)
            status_message(msg)
            return
        self._detector = hw.modules["detector"].devices[0]
        self._interface = hw.modules["interface"].devices[0]
        
        # Detector configuration
        self._detector.set_triggermode("External")
        self._detector.set_exposure(0.00005)
        
        if self.rawRadioButton.isChecked():
            # Start streaming raw spectra from the camera
            msg = "Starting scope in raw spectrum mode."
            self._log.info(msg)
            status_message(msg)
            # Configure the plot area
            self.plot.setLimits(
                xMin=self._detector.get_pixel_wavelengths()[0],
                xMax=self._detector.get_pixel_wavelengths()[-1],
                yMin=0, yMax=self._detector.get_max_value())
            self.spectrum.setData()
            self.plot.setLabel("left", "Intensity (a.u.)")
            self.plot.setRange(
                xRange=(self._detector.get_pixel_wavelengths()[0], self._detector.get_pixel_wavelengths()[-1]),
                yRange=(0, self._detector.get_max_value())
            )
            # Start acquisition
            self._interface.stop()
            self._detector.stop()
            self._detector.register_spectrum_callback(self._raw_spectrum_acquired)
            self._detector.start()
            # Start triggering camera using interface, but don't collect chopper or delay information
            self._interface.trigger()
        elif self.deltaARadioButton.isChecked():
            # Start background thread to collect and compute DeltaA
            msg = f"Starting scope in ΔA mode using {self.samplesSpinBox.value()} samples."
            self._log.info(msg)
            status_message(msg)
            # Press the button to start the chopper
            self.enablePushButton.setChecked(True)
            self._enable_pressed()
            # Configure plot
            self.plot.setLimits(
                xMin=self._detector.get_pixel_wavelengths()[0],
                xMax=self._detector.get_pixel_wavelengths()[-1],
                yMin=-1, yMax=1)
            self.spectrum.setData()
            self.plot.setLabel("left", "ΔA")
            self.plot.setRange(
                xRange=(self._detector.get_pixel_wavelengths()[0], self._detector.get_pixel_wavelengths()[-1]),
                yRange=(-0.02, +0.02)
            )
            # Start the acquisition thread
            self._acq_thread = Thread(name="Scope", daemon=True, target=self._start_acq)
            self._acq_stop.clear()
            self._acq_thread.start()
        else:
            msg = "Unable to start scope acquisition, no mode was selected."
            self._log.warning(msg)
            status_message(msg)
            return
        self.spectrum.setData()


    def stop(self):
        """
        Stop acquiring spectra.
        """
        msg = "Stopping scope."
        self._log.info(msg)
        status_message(msg)
        try:
            self._acq_stop.set()
            if self._acq_thread is not None:
                self._acq_thread.join()
        except:
            self._log.debug("Error stopping acquisition thread.")
        try:
            self._interface.stop()
        except:
            self._log.debug("Error stopping interface.")
        try:
            self._detector.stop()
            self._detector.unregister_spectrum_callback(self._raw_spectrum_acquired)
        except:
            self._log.debug("Error stopping detector.")
        try:
            hw.modules["chopper"].devices[0].set_enabled(False)
            self.enablePushButton.setText("Enable")
        except:
            self._log.debug("Error stopping chopper.")
        self._interface = None
        self._detector = None
        self._acq_thread = None


    def _start_acq(self, averaging_method="mean of DeltaA"):
        """
        Background thread to acquire spectra and compute DeltaA.
        """
        # We should try to handle any error that may occur in this background thread
        try:
            # Storage and event for chopper state data received from the interface
            interface_done = Event()
            global chopper_state
            chopper_state = np.zeros((0,), dtype=bool)

            # Handle the interface acquisition completion callback
            def _got_chopper_state(delay_pos, chop_state):
                global chopper_state
                chopper_state = chop_state
                interface_done.set()
            self._interface.register_data_callback(_got_chopper_state)

            # Storage and event for signal spectra obtained from the detector
            detector_done = Event()
            global spectra
            spectra = np.zeros((0, 0))

            # Handle the detector data acquisition callback
            def _got_spectra(data):
                global spectra
                spectra = data
                detector_done.set()
            self._detector.register_acquisition_callback(_got_spectra)

            # Acquire spectra until stopped manually
            acquisition_attempt_count = 0
            while not self._acq_stop.is_set():

                # Acquire spectra and chopper state
                interface_done.clear()
                detector_done.clear()
                chopper_state = np.zeros((0,), dtype=bool)
                spectra = np.zeros((0, 0))
                # Should be safe to read UI status from this from background thread
                n_samples = self.samplesSpinBox.value()
                # Start detector
                self._detector.start(2*n_samples)
                # Manually trigger the interface which will then trigger the detector shutter
                self._interface.start(2*n_samples)

                # Wait for acquisition to finish
                acq_start_time = monotonic()
                acq_expected_duration = 2*n_samples/config.data["hardware"]["laser_reprate"] + 1.0
                acquisition_failure = False
                while not (interface_done.is_set() and detector_done.is_set()):
                    if self._acq_stop.is_set():
                        raise AcquisitionAbortedWarning()
                    if monotonic() > (acq_start_time + acq_expected_duration):
                        # TODO: Could decide on timeout value depending on number of samples and laser rep rate
                        acquisition_failure = True
                        break
                    sleep(0.01)
                if acquisition_failure:
                    # Count acquisition attempts
                    acquisition_attempt_count += 1
                    if acquisition_attempt_count >= 50:
                        # Too many retries have occurred
                        raise AcquisitionError(f"Failed to receive detector data after {acquisition_attempt_count} acquisition attempts.")
                    else:
                        # Retry acquisition at this time point
                        bad_devices = "detector" if not detector_done.is_set() else ""
                        bad_devices += " and " if (not detector_done.is_set()) and (not interface_done.is_set()) else ""
                        bad_devices += "interface" if not interface_done.is_set() else ""
                        msg = f"Timeout waiting for {bad_devices} data, will retry."
                        self._log.warning(msg)
                        status_message(msg)
                        self._interface.stop()
                        self._detector.stop()
                        # Interface will return (possibly zero length) data once stopped, wait to receive that before continuing
                        sleep(0.25)
                        continue
                else:
                    # Successful acquisition
                    acquisition_attempt_count = 0

                if chopper_state.shape[0] > 0 and chopper_state.shape[0] == spectra.shape[0]:
                    # Acquired same number of chopper states and spectra... good
                    # Split into "chopper on" and "chopper off" sets
                    ons = spectra[chopper_state]
                    offs = spectra[~chopper_state]
                    # Ideally, they should alternate between on and off, but not always true
                    n = min(ons.shape[0], offs.shape[0])
                    if n == 0:
                        # Something wrong with chopper, all on or all off
                        msg = "Interface didn't detect chopper movement (start chopper, check connections?)."
                        self._log.warning(msg)
                        status_message(msg)
                        self._data_received.emit(None)
                        sleep(0.5)
                        continue
                    
                    # Compute DeltaA using selected method
                    with warnings.catch_warnings():
                        # Ignore divide-by zero when computing deltaA
                        warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="divide by zero encountered in true_divide")
                        warnings.filterwarnings(action="ignore", category=RuntimeWarning, message="invalid value encountered in true_divide")
                        if averaging_method == "mean of samples":
                            # Average all "on" and all "off" samples, then compute DeltaA
                            data = no_infs(-np.log10(no_infs(np.nanmean(ons, axis=0, dtype=np.float32)/np.nanmean(offs, axis=0, dtype=np.float32))))
                        elif averaging_method == "mean of ratios":
                            # Compute ratio of adjacent "on" and "off" samples, then average the ratios
                            ons = ons[:n]
                            offs = offs[:n]
                            data = no_infs(-np.log10(np.nanmean(no_infs(ons/offs), axis=0, dtype=np.float32)))
                        else:
                            # Average DeltaA computed using adjacent "on" and "off" samples
                            ons = ons[:n]
                            offs = offs[:n]
                            data = np.nanmean(no_infs(-np.log10(no_infs(ons/offs))), axis=0, dtype=np.float32)
                else:
                    # We can't match up the chopper state to the spectra
                    # TODO: Implement time stamps on spectra and try to sort them out
                    msg = f"Requested {2*n_samples} spectra, received {chopper_state.shape[0]} chopper values and {spectra.shape[0]} spectra, retrying acquisition."
                    self._log.warning(msg)
                    status_message(msg)
                    continue

                # Emit the signal that data has been updated
                self._data_received.emit(data)

        except AcquisitionAbortedWarning:
            # Stopping manually is perfectly normal
            pass
        except Exception as ex:
            # Notify of any errors which occurred during acquisition
            self._log.error(f"{ex}")
 
        # Be careful cleaning up, as we don't want to raise any exceptions within this thread
        self._acq_stop.set()    
        # It's possible that these callback functions haven't been defined if an error occurs early
        try:
            self._detector.unregister_acquisition_callback(_got_spectra)
        except: pass
        try:
            self._interface.unregister_data_callback(_got_chopper_state)
        except: pass
        try:
            self._detector.stop()
        except:
            self._log.debug("Error stopping Detector.")
        try:
            self._interface.stop()
        except:
            self._log.debug("Error stopping Interface.")
        self._log.info("Acquisition stopped.")


    def _raw_spectrum_acquired(self, data, force=False):
        """
        Receive a new raw spectrum and emit the data update signal.

        Since this will get called from a background thread (outside of the Qt event loop thread),
        then we need to wrap the signal emit() so that the plot update happens inside the Qt thread.

        :param data: Spectral data.
        :param force: Force an update, even if maximum frame rate would be exceeded.
        """
        this_update_time = monotonic()
        if force or (this_update_time > self._last_update_time + self._update_interval):
            self._data_received.emit(data)
            self._last_update_time = this_update_time


    def _set_spectrum_data(self, data):
        """
        Update the plot with the provided spectrum data.

        This should only be called from inside the Qt event loop. Emit the :data:`_data_received`
        signal or call :meth:`_raw_spectrum_acquired` if the plot needs to be updated from
        alternative background threads.

        :param data: Spectral data.
        """
        if data is None:
            self.spectrum.setData()
        else:
            try:
                self.spectrum.setData(hw.modules["detector"].devices[0].get_pixel_wavelengths(), data)
            except (AttributeError, ValueError):
                self.spectrum.setData()
            

    def _delay_changed(self, value):
        """Move the delay to selected time."""
        try:
            si_f = si_unit_factor(self.delayDoubleSpinBox.suffix())
            hw.modules["delay"].devices[0].set_delay(value*si_f)
        except:
            msg = "Error changing delay value."
            self._log.warn(msg)
            status_message(msg)

    def _begin_pressed(self):
        """Move to beginning of delay."""
        self.delayDoubleSpinBox.setValue(self.delayDoubleSpinBox.minimum())

    def _inc_pressed(self):
        """Increment delay."""
        self.delayDoubleSpinBox.setValue(self.delayDoubleSpinBox.value() + 100)

    def _dec_pressed(self):
        """Decrement delay."""
        self.delayDoubleSpinBox.setValue(self.delayDoubleSpinBox.value() - 100)

    def _end_pressed(self):
        """Move to end of delay."""
        self.delayDoubleSpinBox.setValue(self.delayDoubleSpinBox.maximum())


    def _enable_pressed(self):
        """Handle starting/stopping chopper."""
        try:
            if self.enablePushButton.isChecked():
                hw.modules["chopper"].devices[0].set_enabled(True)
                self.enablePushButton.setText("Disable")
            else:
                hw.modules["chopper"].devices[0].set_enabled(False)
                self.enablePushButton.setText("Enable")
        except:
            msg = "Error changing chopper state."
            self._log.warning(msg)
            status_message(msg)


    def _save_pressed(self):
        """Save the current spectrum out to a file."""
        self.stop()
        try:
            data = np.array(self.spectrum.getData())
        except:
            status_message("No current spectrum to save!")
            self.start()
            return
        # Suggested filename based on date code
        suffix = ".raw_spectrum.csv" if self.rawRadioButton.isChecked() else ".deltaA_spectrum.csv"
        initial_filename = strftime("%y%m%d_%H%M%S", localtime()) + suffix
        initial_filename = os.path.join(config.data["directories"]["data"], initial_filename)
        filename, _ = QFileDialog.getSaveFileName(self, "Save Spectrum", initial_filename, f"Spectra (*{suffix})")
        if filename:
            # Ensure name has appropriate suffix
            filename = filename.partition(suffix)[0] + suffix
            np.savetxt(filename, data, fmt="%g", delimiter=",")
        self.start()


    def _load_pressed(self):
        """Load a saved spectrum up for display as a reference."""
        if self.loadPushButton.isChecked():
            # Act as load button
            self.stop()
            if self.rawRadioButton.isChecked():
                suffix = ".raw_spectrum.csv"
                plot_trace = self.reference_raw
                config_entry = "reference_raw"
            else:
                suffix = ".deltaA_spectrum.csv"
                plot_trace = self.reference_deltaA
                config_entry = "reference_deltaA"
            filename, _ = QFileDialog.getOpenFileName(self, "Load Spectrum", config.data["directories"]["data"], f"Spectra (*{suffix})")
            if not filename:
                self.loadPushButton.setChecked(False)
                self.start()
                return
            try:
                spec = np.loadtxt(filename, delimiter=",")
                plot_trace.setData(spec[0], spec[1])
            except:
                status_message(f"Error loading spectrum data from {filename}")
                self.loadPushButton.setChecked(False)
                self.start()
                return
            self.plot.addItem(plot_trace)
            plot_trace.setZValue(-5)
            config.data["scope"]["ui"][config_entry] = filename
            self.loadPushButton.setText("Unload")
            self.start()
        else:
            # Act as clear button
            self.loadPushButton.setText("Load")
            if self.rawRadioButton.isChecked():
                self.plot.removeItem(self.reference_raw)
                self.reference_raw.setData()
                config.data["scope"]["ui"]["reference_raw"] = ""
            else:
                self.plot.removeItem(self.reference_deltaA)
                self.reference_deltaA.setData()
                config.data["scope"]["ui"]["reference_deltaA"] = ""
  

    def _pin_pressed(self):
        """Pin or un-pin a temporary reference spectrum to the plot."""
        if self.pinPushButton.isChecked():
            try:
                self.reference_pinned.setData(*self.spectrum.getData())
                self.reference_pinned.setZValue(-4)
                self.plot.addItem(self.reference_pinned)
            except:
                # No spectra yet to pin?
                self.pinPushButton.setChecked(False)
        else:
            self.plot.removeItem(self.reference_pinned)


    def _save_ui_config(self):
        """Save GUI control values out to configuration file."""
        config.data["scope"]["ui"]["mode"] = "raw" if self.rawRadioButton.isChecked() else "deltaA"
        config.data["scope"]["ui"]["samples"] = self.samplesSpinBox.value()
    

    def _load_ui_config(self):
        """Load GUI control values from configuration file."""
        try:
            rawmode = (config.data["scope"]["ui"]["mode"] == "raw")
            self.rawRadioButton.setChecked(rawmode)
            self.deltaARadioButton.setChecked(not rawmode)
        except:
            self.rawRadioButton.setChecked(True)
            self.deltaARadioButton.setChecked(False)
            config.data["scope"]["ui"]["mode"] = "raw"
        try:
            self.samplesSpinBox.setValue(config.data["scope"]["ui"]["samples"])
        except:
            self.samplesSpinBox.setValue(50)
            config.data["scope"]["ui"]["samples"] = 50
        self.samplesSpinBox.setEnabled(not self.rawRadioButton.isChecked())
        # Attempt to load saved spectra from disk
        try:
            filename = config.data["scope"]["ui"]["reference_raw"]
            if filename:
                spec = np.loadtxt(filename, delimiter=",")
                self.reference_raw.setData(spec[0], spec[1])
            else:
                self.reference_raw.setData()
        except:
            self._log.debug(f"Unable to load the saved raw spectrum.")
            self.reference_raw.setData()
        try:
            filename = config.data["scope"]["ui"]["reference_deltaA"]
            if filename:
                spec = np.loadtxt(filename, delimiter=",")
                self.reference_deltaA.setData(spec[0], spec[1])

            else:
                self.reference_deltaA.setData()
        except:
            self._log.debug("Unable to load the saved deltaA spectrum.")
            self.reference_deltaA.setData()
        self._update_reference_spectrum()
