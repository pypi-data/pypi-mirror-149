#!/usr/bin/env python3

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

# TODO: Signals don't always get triggered, so a setProgress maximum can get lost
#       Perhaps make a separate maxchanged signal and trigger that? Then also include
#       a method to trigger that signal.
# TODO: Make an "incrementProgress" method?
# TODO: Get icon from parent if possible

import os
from threading import Thread, Event
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout
from PySide6.QtCore import QObject, Signal


class BusyThread(QObject):
    """Runs a task in a background thread, and makes callback when complete.

    :param task: Reference to function which performs the desired task.
        In addition to the given *args* and *kwargs*, the task will be passed a
        reference to the instance of this BusyThread instance. Care should be
        taken if manipulating the BusyThread from the separate (new task) thread,
        but it is provided in case it is useful (e.g. to update the GUI of the
        :class:`BusyDialog` subclass).
        If the specified *task* function does not expect being passed this additional
        reference, then it can be ignored by wrapping with a lambda expression, e.g.
        ``task=lambda _: time.sleep(5)``.
    :param args: Tuple of positional arguments to pass to the task function.
    :param kwargs: Dictionary of keyword arguments to pass to the task function.
    :param callback: Reference to function to call once task is complete. It will
        be passed whatever is returned from the *task* function.
    """

    _task_finished_signal = Signal(object)
    """``pyqtSignal`` to emit when task is complete."""

    def __init__(self, task=None, args=(), kwargs={}, callback=None):
        super().__init__()

        # Thread to run given method in background
        self.task = task if task else lambda : None
        if callable(callback): self._task_finished_signal.connect(callback)
        self._task_thread = Thread(target=self._start_task, args=(args, kwargs), name="BusyTask")
        self._task_thread.start()

    def _start_task(self, args, kwargs):
        # Task will be passed a reference to this BusyThread, so it can tweak internals if desired
        result = self.task(self, *args, *kwargs)
        self._task_finished_signal.emit(result)


class BusyDialog(QDialog):
    """Runs a task in a background thread, and makes callback when complete.
    A dialog is displayed, with a progress bar and label. These may be updated
    by the background task to communicate progress to the user.

    :param parent: QWidget parent (for example, a QMainWindow instance) to which this dialog box belongs.
    :param modal: Set the modal window flag on the dialog.
    :param title: String to display in the dialog title bar.
    :param label: String to display in the dialog label.
    :param progress: Tuple of initial current and maximum progress values.
    :param task: Reference to function which performs the desired task.
        See :class:`BusyThread` for more information.
    :param args: Tuple of positional arguments to pass to the task function.
    :param kwargs: Dictionary of keyword arguments to pass to the task function.
    :param callback: Reference to function to call once task is complete. It will
        be passed whatever is returned from the *task* function.
    """

    _task_finished_signal = Signal(object)
    """``Signal`` to emit when task is complete."""

    _update_label_signal = Signal(str)
    """``Signal`` used to trigger a label update."""

    _update_progress_signal = Signal(int, int)
    """``Signal`` used to trigger a progress bar update."""

    _increment_progress_signal = Signal(int)
    """``Signal`` used to trigger an increment of the progress bar."""

    # Note we need to prevent the spawned thread from directly modifying things
    # in the Qt GUI thread, so need to trigger label, progress updates through
    # emitting and responding to Qt signals.

    def __init__(self, parent=None, modal=False, title=None, label="Please wait...", progress=(0, 0), task=None, args=(), kwargs={}, callback=None):
        super().__init__(parent=parent)
        
        self.resize(400, 100)
        self.setModal(modal)
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(label, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(progress[1])
        self.progressBar.setValue(progress[0])
        self.verticalLayout.addWidget(self.progressBar)
        self.setWindowTitle(title if title is not None else parent.windowTitle() if parent is not None else "One moment...")
        self.setFixedSize(self.size())

        self._task_finished_signal.connect(lambda x: self.close())
        self._update_label_signal.connect(self._update_label)
        self._update_progress_signal.connect(self._update_progress)
        self._increment_progress_signal.connect(self._increment_progress)

        # Thread to run given method in background
        self.task = task if task else lambda : None
        if callable(callback): self._task_finished_signal.connect(callback)
        self._task_thread = Thread(target=self._start_task, args=(args, kwargs), name="BusyTask")
        self._task_complete = Event()
        self._task_thread.start()

        # TODO: It would be nice to wait ~1 s before showing
        # so if the task finishes before then, the dialog doesn't get shown
        self.show()

    def _start_task(self, args, kwargs):
        # Task will be passed a reference to this BusyThread, so it can tweak internals if desired
        result = self.task(self, *args, *kwargs)
        self._task_complete.set()
        self._task_finished_signal.emit(result)

    def closeEvent(self, event):
        """Handler for window close event. If the background task is still running,
        the window close event will be ignored."""
        if not self._task_complete.is_set():
            event.ignore()
        else:
            event.accept()

    def setLabel(self, label):
        """Update the text of the dialog label. This method is thread safe and
        may be called by the running background task. Do not attempt to
        manipulate the label directly from outside the main Qt application thread!

        :param label: String to display in the dialog label.
        """
        self._update_label_signal.emit(label)

    def _update_label(self, label):
        self.label.setText(label)

    def setProgress(self, progress_current, progress_maximum=-1):
        """Update the progress bar of the dialog. This method is thread safe and
        may be called by the running background task. Do not attempt to
        manipulate the progress bar directly from outside the main Qt application thread!

        :param progress_current: Number representing current progress.
        :param progress_maximum: Number representing maximum (complete) progress.
        """
        if progress_current < 0: progress_current = progress_maximum = 0
        self._update_progress_signal.emit(progress_current, progress_maximum)

    def _update_progress(self, progress_current, progress_maximum):
        if progress_maximum >= progress_current: self.progressBar.setMaximum(progress_maximum)
        self.progressBar.setValue(progress_current)

    def incrementProgress(self, increment=1):
        self._increment_progress_signal.emit(increment)

    def _increment_progress(self, increment):
        self.progressBar.setValue(self.progressBar.value() + increment)

def main():
    """Run a demo of the BusyDialog."""
    import sys
    import time
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = BusyDialog(title="Timewaster 2000", label="Sleeping for 5 seconds...", task=lambda dialog, t: time.sleep(t), args=(5,))
    sys.exit(mainwindow.exec())

if __name__ == '__main__':
    main()
