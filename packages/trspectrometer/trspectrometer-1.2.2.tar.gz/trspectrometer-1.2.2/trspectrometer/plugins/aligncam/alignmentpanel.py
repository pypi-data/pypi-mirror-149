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

import sys
import logging
from threading import Lock

from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Signal
import numpy as np
import cv2

import pyqtgraph as pg
import configuration as config
import hardware as hw


class AlignmentPanel(QtWidgets.QWidget, loadUiType(__file__.split(".py")[0] + ".ui")[0]):

    """
    UI panel to facilitate the alignment of a laser beam through a translating
    retroreflector delay stage.

    When the beam is properly aligned into the input of the delay stage,
    translating the retroreflector should not cause any change in the beam
    position on a target after the output of the delay.

    To align the beam, the laser spot is observed on a target screen at some
    location after the delay stage.
    This is performed with a video camera device focussed on the target screen.
    An interative process is then used to correctly align the beam input in to
    the delay stage:

        1. The delay stage is moved to the start of its track.

        2. The position of the laser spot is marked.

        3. The delay stage is moved to the end of its track.

        4. The new position of the laser spot is marked.

        5. If the two markers are overlapped well, the alignment is complete.
           Otherwise, vertical and/or horizontal deflection adjustments are made
           on the input steering mirror and the process is repeated.

    :param parent: Parent of the QWidget.
    """

    # Signal to indicate device list has been refreshed
    _devices_changed = Signal()
    # Signal to indicate there is new image data to display
    _frame_acquired = Signal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.log = logging.getLogger(__name__)

        # Configure plot area
        pg.setConfigOptions(imageAxisOrder='row-major', antialias=True)
        [ self.plotWidget.getAxis(ax).setZValue(10) for ax in self.plotWidget.getPlotItem().axes ] # Draw axes and ticks above image/data
        self.image = pg.ImageItem()
        self.plotWidget.addItem(self.image)
        # Spot alignment markers
        self.rois = [
            pg.EllipseROI((100, 100), (75, 75), pen=(0, 0, 255)),
            pg.EllipseROI((200, 200), (75, 75), pen=(255, 0, 0), movable=False)
        ]
        for i, roi in enumerate(self.rois):
            try:
                # Load position, size, angle of ROIs from config
                geom = config.data["alignment"]["ui"]["rois"][i]
                roi.setPos(geom["pos"], update=False)
                roi.setSize(geom["size"], update=False)
                roi.setAngle(float(geom["angle"]))
            except:
                self.log.warning(f"Couldn't restore ROI #{i} state from config.")
        for roi in self.rois:
            roi.sigRegionChanged.connect(self._roi_changed)
            self.plotWidget.addItem(roi)
        self.roiline = self.plotWidget.plot(pen=(0, 192, 0), symbol="+")
        self._roi_changed()

        self.plotWidget.setAspectLocked(True, ratio=1.0)

        # Restore UI settings
        try:
            self.auto_checkBox.setChecked(config.data["alignment"]["ui"]["auto"])
        except:
            self.auto_checkBox.setChecked(False)
            config.data["alignment"]["ui"]["auto"] = False

        # Handle signal that camera device list refreshed
        hw.modules["aligncam"].add_change_callback(self._change_callback)
        self._devices_changed.connect(self.reset)

        # Handle signal that new frame data is available
        self._frame_acquired.connect(self._process_frame)

        # Connect UI signals
        self.camera_comboBox.currentIndexChanged.connect(self._camera_changed)
        self.reset_pushButton.clicked.connect(hw.modules["aligncam"].init)
        self.delay_horizontalSlider.valueChanged.connect(self._delay_changed)
        self.auto_checkBox.clicked.connect(self._auto_changed)

        # Populate the camera list box and start acquisition
        self.reset()

    def _change_callback(self):
        """
        Notify of a change in the camera devices.

        This may be called from outside the Qt event loop, so don't touch anything!
        Instead emit a signal and let the handler inside the Qt thread handle
        the updating of the UI.
        """
        self._devices_changed.emit()

    def reset(self):
        """
        Reset the panel, showing any new camera devices.

        The actual hardware detection is handled by ``aligncam``, this
        will only synchronise the UI to the cameras in the hardware module.
        """
        # Populate and configure camera selection box
        self.camera_comboBox.blockSignals(True)
        self.camera_comboBox.clear()
        for cam in hw.modules["aligncam"].devices:
            self.camera_comboBox.addItem(f"{cam.name}{' (missing)' if cam.vidcap is None else ''}")
        try:
            index = config.data["alignment"]["ui"]["cameraindex"]
            self.camera_comboBox.setCurrentIndex(index)
            self.camera_comboBox.blockSignals(False)
        except:
            self.log.warning("Can't select default camera index")
        if self.camera_comboBox.currentIndex() >= 0:
            # Cameras listed
            self.plotWidget.setEnabled(True)
            # Trigger first selection of camera device
            self._camera_changed(self.camera_comboBox.currentIndex())
        else:
            # No cameras in list
            self.plotWidget.setEnabled(False)
        self.camera_comboBox.blockSignals(False)

    def showEvent(self, event):
        """
        Handle the Qt event when widget is shown.

        :param event: QEvent describing the event.
        """
        # Register for new frame events from selected camera
        try:
            hw.modules["aligncam"].devices[self.camera_comboBox.currentIndex()].add_frame_callback(self._frame_callback)
        except:
            # Probably no cameras configured
            pass

    def hideEvent(self, event):
        """
        Handle the Qt event when widget is hidden.

        :param event: ``QEvent`` describing the event.
        """
        # Don't need to receive frames anymore
        try:
            hw.modules["aligncam"].devices[self.camera_comboBox.currentIndex()].remove_frame_callback(self._frame_callback)
        except:
            # Probably no cameras configured
            pass

    def _frame_callback(self, frame):
        """
        Notify that a new image frame from the camera is available.

        This may be called from outside the Qt event loop, so don't touch anything!
        Instead emit a signal and let the handler inside the Qt thread handle
        the updating of the UI.

        :param frame: Numpy ``ndarray`` containing image data.
        """
        self._frame_acquired.emit(frame)

    def _process_frame(self, frame):
        """
        Handle the Qt signal that a new image frame from the camera is available.

        This handler is called by the Qt event loop on when the signal is
        emitted, and thus is able to update the UI safely.

        :param frame: Numpy ``ndarray`` containing image data.
        """

        # Flip image vertically to match y-axis direction
        self.image.setImage(frame[::-1])
        if self.auto_checkBox.isChecked(): self._do_fit()

    def _camera_changed(self, index):
        """
        Handle changing of the selected camera device.

        :param index: Numerical index of the new device.
        """
        # Don't need to receive frames from old device(s)
        for cam in hw.modules["aligncam"].devices:
            cam.remove_frame_callback(self._frame_callback)
        cam_i = self.camera_comboBox.currentIndex()
        if cam_i >= 0:
            cam = hw.modules["aligncam"].devices[cam_i]
            if not self.isHidden() and self.isVisible():
                # On creation, widget will be not hidden *and* not visible!
                # We don't need to process frames until first viewed.
                cam.add_frame_callback(self._frame_callback)
            self.image.setImage(np.zeros((cam.height, cam.width)))
            self.image.setPos(-0.5, -0.5)
            self.plotWidget.setLimits(xMin=0, xMax=cam.width + 0.5,
                                      yMin=-0.5, yMax=cam.height + 0.5)
            # Adjust roi bounds and move into view if needed
            # TODO Bug in pyqtgraph with rotated ROIs and maxBounds.
            #for i, roi in enumerate(self.rois):
            #    roi.maxBounds = QtCore.QRectF(0, 0, cam.width, cam.height)
            #    roi.translate(0, 0)
            self.plotWidget.enableAutoRange()
            config.data["alignment"]["ui"]["cameraindex"] = cam_i

    def _roi_changed(self, changed_roi=None):
        """
        Handle changes to the marker ROI position, size, or angle.
        """
        # Finding the centre of the markers is a bit annoying since they may
        # have a rotation transform applied. Coordinates returned from pos()
        # and size() need transforming back to plot coordinates etc.
        x, y = [], []
        for roi in self.rois:
            x.append(roi.pos()[0] + np.cos(np.radians(roi.angle()))*roi.size()[0]/2 - np.sin(np.radians(roi.angle()))*roi.size()[1]/2)
            y.append(roi.pos()[1] + np.sin(np.radians(roi.angle()))*roi.size()[0]/2 + np.cos(np.radians(roi.angle()))*roi.size()[1]/2)
        self.roiline.setData(x, y)
        # Radial distance
        #d_r = np.hypot(x[0] - x[1], y[0] - y[1])
        self.translationLabel.setText(f"{x[1] - x[0]:0.0f}, {y[1] - y[0]:0.0f}")
        # Change in angle
        d_a = (self.rois[0].angle() - self.rois[1].angle())%180
        if d_a > 90: d_a = 180 - d_a
        self.rotationLabel.setText(f"{d_a:0.0f}°")
        # Change in aspect ratio
        d_asp = (np.max(tuple(self.rois[0].size()))/np.min(tuple(self.rois[0].size())))/(np.max(tuple(self.rois[1].size()))/np.min(tuple(self.rois[1].size())))
        #if d_asp < 1.0: d_asp = 1/d_asp
        self.aspectLabel.setText(f"{d_asp:0.2f}")
        # Divergence, as ratio of area of markers
        d_s = np.prod(self.rois[1].size())/np.prod(self.rois[0].size())
        self.divergenceLabel.setText(f"{d_s:0.2f}")
        # Store updated ROI shape in config
        geom = []
        for roi in self.rois:
            geom.append({
                "pos" : list(roi.pos()),
                "size" : list(roi.size()),
                "angle" : roi.angle()
            })
        config.data["alignment"]["ui"]["rois"] = geom

    def _delay_changed(self, value):
        """
        Handle changes to the delay position slider.
        """
        self.rois[bool(value)].translatable = True
        self.rois[not bool(value)].translatable = False
        try:
            # Move delay
            delay = hw.modules["delay"].devices[0]
            delay.set_velocity(2e-9)
            delay.set_acceleration(2e-8)
            delay.set_delay((delay.min_delay(), delay.max_delay())[bool(value)])
        except Exception as ex:
            # TODO: narrow exception types, IndexError etc
            #print("NoDelay: ", ex)
            pass
        

    def _auto_changed(self, value):
        config.data["alignment"]["ui"]["auto"] = value

    def _do_fit(self):
        # Noise reduction with blur
        image = image = cv2.GaussianBlur(self.image.image, (25, 25), 0)
        # Convert to binary image with simple threshold
        _, image = cv2.threshold(image, 3*image.max()//4, 255, cv2.THRESH_BINARY)
        # Extract contours from inage
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Fit ellipses to contours
        ellipses = []
        for c in contours:
            if c.shape[0] > 5:
                ellipses.append(cv2.fitEllipse(c))
        # Abort update if no ellipses detected
        if len(ellipses) == 0: return
        # Select largest ellipse
        area = 0
        for e in ellipses:
            a = e[1][0] * e[1][1]
            if a > area:
                area = a
                pos, size, angle = e

        # Transform to ROI position coordinates
        roi = self.rois[bool(self.delay_horizontalSlider.value())]
        roi.setAngle(angle)
        roi.setSize(size)
        x_prime = pos[0] - np.cos(np.radians(roi.angle()))*roi.size()[0]/2 + np.sin(np.radians(roi.angle()))*roi.size()[1]/2
        y_prime = pos[1] - np.sin(np.radians(roi.angle()))*roi.size()[0]/2 - np.cos(np.radians(roi.angle()))*roi.size()[1]/2
        roi.setPos(x_prime, y_prime)
