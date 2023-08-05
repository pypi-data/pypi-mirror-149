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
Module for storing miscellaneous utility functions etc.
"""

import re
from datetime import datetime

import numpy as np

import configuration as config


def no_infs(x, copy=True):
    """
    Convenience function to convert all ``+inf`` and ``-inf`` in a numpy array to ``nan``.

    :param x: Numpy array.
    :param copy: Create a copy of ``x`` (default, ``True``), or convert in-place (``False``).
    :returns: The array ``x``, with all infinite values converted to ``nan``.
    """
    return np.nan_to_num(x, copy=copy, nan=np.nan, posinf=np.nan, neginf=np.nan)


def mask_outliers(data, axis:int=0, sensitivity:float=0.1, copy:bool=True):
    """
    Convert outlying points in a numpy array to NaNs.
    
    The ``axis`` parameter determines the array axis in which to compute the median values and
    detect the outliers. The ``sensitivity`` parameter would typically range between 0.0 and 1.0,
    where 0.0 will return the original data unmodified, and larger values will remove a greater
    number of outliers. Values greater than 1.0 are permitted. By default the operation is performed
    on a copy of the original data. To modify the original data in-place, the ``copy`` parameter can
    be set to ``False``.
    
    :param data: Numpy array containing data to process.
    :param axis: Index of array axis in which to detect outliers.
    :param sensitivity: Sensitivity of outlier detection.
    :param copy: Operate on a copy of the input data.

    :returns: Numpy array containing the processed data.
    """
    if sensitivity > 0.0:
        data_delta = np.abs(data - np.nanmedian(data, axis=axis))
        med_dev = np.nanmedian(data_delta, axis=axis)
        if copy:
            data = data.copy()
        data[(data_delta/med_dev)>(1.0/sensitivity)] = np.nan
    return data


class AcquisitionError(RuntimeError):
    """
    An exception to identify some error which occurred during the acquisition process.

    :param message: String describing the error.
    """
    def __init__(self, message="Unknown acquisition error."):
        super().__init__(message)


class AcquisitionAbortedWarning(UserWarning):
    """
    An exception to indicate the acquisition process was stopped manually.

    Since the stop was manually triggered, this is a warning rather than an error, but may still
    want to be acted upon by the listeners to the completion callback.

    :param message: String describing the warning.
    """
    def __init__(self, message="Acquisition interrupted by user."):
        super().__init__(message)


def status_message(message: str) -> None:
    """
    Display a message on the main window's status bar.

    This may be called from outside the Qt UI thread.

    :param message: String to display on the status bar.
    """
    try:
        config.mainwindow.show_message.emit(message)
    except: pass


def clean_filename(filename, allowed_symbols=["-", "_", "+", "."]):
    """
    Clean up a filename by removing symbols and replacing spaces with underscores.
    
    The list of ``allowed_symbols`` will not be removed.
    
    :param filename: Input filename to clean up.
    :returns: The cleaned filename.
    """
    # Perform a few substitutions first
    filename = filename.rstrip()
    filename = re.subn("(?<=[0-9]) nm", "nm", filename)[0]
    filename = re.subn("(?<=[0-9]) mW", "mW", filename)[0]
    filename = filename.replace(" ", "_")
    filename = filename.replace("&", "+")
    return "".join(c for c in filename if c.isalnum() or c in allowed_symbols)


def si_unit_factor(unit: str):
    """
    Get the scaling factor for a given SI unit prefix.

    The current implementation works for time-based units (in seconds, s), and wavelength units (in
    metres, m) for ranges applicable for this application. For example, the scaling factor for
    ``"ps"`` is 1e-12.

    :param unit: String of the SI unit.
    :returns: Scaling factor of the SI prefix.
    """
    return {
        # Time units
        "hours": 3600.0,
        "hr": 3600.0,
        "minutes": 60.0,
        "min": 60.0,
        "s" : 1.0,
        "ms": 1e-3,
        "us": 1e-6,
        "µs": 1e-6,  # micro sign UxB5
        "μs": 1e-6,  # greek small letter mu Ux3BC
        "ns": 1e-9,
        "ps": 1e-12,
        "fs": 1e-15,
        "as": 1e-18,
        # Wavelength units
        "m" : 1.0,
        "mm": 1e-3,
        "um": 1e-6,
        "µm": 1e-6,  # micro sign UxB5
        "μm": 1e-6,  # greek small letter mu Ux3BC
        "nm": 1e-9,
        "pm": 1e-12,
        "Å" : 1e-10,  # Angstrom sign Ux212B
        "Å" : 1e-10,  # capital letter A with ring above UxC5
        "A" : 1e-10,
        "fm": 1e-15,
        "am": 1e-18,
    }[unit.strip()]


def now_string():
    """
    Get the current local time as an ISO8601 formatted string.

    This format is useful for embedding into the metadata of data files. To convert the string back
    into a python ``datetime`` object, use :meth:`datetime.fromisoformat`.

    :returns: String representation of current time.
    """
    return datetime.now().astimezone().isoformat()
