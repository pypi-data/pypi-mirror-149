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

"""
This module is used to store references to Qt Signals for use by various other components of the
application.

Since Qt Signals can only be sent by QObjects, an instance of the :data:`SignalStorage` class is
used to store and emit the various Signals. Do not create new instances of the :data:`SignalStorage`
class, instead access the shared instance as the :data:`signals` attribute of this module.

An example usage is:

.. code-block:: python

    from signalstorage import signals
    signals.data_changed.emit(True)

This :data:`signals` instance may be used to store custom signals created dynamically. Do not try to
assign to new attributes to it, it won't work! Instead, use the
:meth:`~trspectrometer.signalstorage.SignalStorage.create_signal` method:

.. code-block:: python

    from signalstorage import signals
    signals.create_signal("custom_signal", str, int, object)
    signals.custom_signal.connect(lambda s, i, o: print(f"Received: {s}, {i}, {o}"))
    signals.emit("one", 2, bytearray([0x33, 0x34]))
"""

from PySide6 import QtCore
from PySide6.QtCore import Signal


class SignalStorage(QtCore.QObject):
    """
    A class to store and emit Qt Signals from.

    Do not create new instances of this class, instead access the shared instance as the
    :data:`~trspectrometer.signalstorage.signals` attribute of the
    :data:`~trspectrometer.signalstorage` module.

    The built-in signals are:

    - ``data_changed``: Signal that new data has been loaded. If the parameter is ``True```, it
      indicates that a complete data set was loaded from a file, and thus user interface controls
      should be updated to match. If ``False``, it indicates that the new data is from an
      acquisition process, and UI updates should not be performed.
    
    - ``raw_data_updated``: Signal that raw data has been updated. The parameters are lists of scan,
      time, wavelength indices which may have changed. ``None`` indicates that all elements have
      potentially changed.
    
    - ``raw_selection_changed``: Signal that the selection of raw data traces has changed.

    - ``acquisition_started``: Signal that data acquisition has started. Components may want to
      connect to this in order to disable functionality while acquisition is in progress.

    - ``acquisition_stopped``: Signal that data acquisition has stopped. An Exception will be
      included if an error occurred. Components may want to connect to this to re-enable functions
      which were disabled during acquisition. An Exception instance may be passed to provide
      information about any errors which occurred.

    - ``laser_reprate_changed``: Signal that the laser repetition rate has changed in the
      configuration. Components may want to respond to this by restarting or re-configuring
      themselves for the new reprate.

    """
    # For some reason sphinx isn't generating documentation for these signals properly,
    # so we'll instead describe them above in the class documentation string.
    data_changed = Signal(bool)
    raw_data_updated = Signal(list, list, list)
    raw_selection_changed = Signal()
    acquisition_started = Signal()
    acquisition_stopped = Signal(object)
    laser_reprate_changed = Signal()

    def create_signal(self, signal_name:str, *args):
        """
        Create a new signal and store it in this class.

        Note, Qt Signals must be created during class definition and can't normally be created
        dynamically. We actually make a new class definition and swap this instance's class type to
        the newly created class. It's some arcane python magic.

        :param signal_name: Name for the new Signal.
        :param args: Type arguments for the new Signal.
        """
        # Make a copy of this class, but add the new signal
        old_cls = self.__class__
        new_cls = type(old_cls.__name__, old_cls.__bases__, {**old_cls.__dict__, signal_name: Signal(*args)})
        # Set this instance's class type to our newly defined one
        self.__class__ = new_cls


# An instance of the SignalStorage class for general use.
signals = SignalStorage()
signals.__doc__ = "A shared instance of :data:`SignalStorage` for use by any components of the application."