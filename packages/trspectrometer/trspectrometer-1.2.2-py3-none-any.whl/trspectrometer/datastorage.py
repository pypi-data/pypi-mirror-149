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
Utilities for handling the creation, manipulation, and storage of transient
absorption data.

The native storage format uses `zarr <https://zarr.readthedocs.io/>`_, which has
many friendly methods for handling data.
These utilities therefore are mainly for the import and export of different file
formats.
"""

import os
import shutil
import warnings
import logging
import time

import numpy as np
import zarr
from scipy.stats import norm
from scipy.ndimage import median_filter
from PySide6.QtWidgets import QFileDialog, QMessageBox

import configuration as config
from signalstorage import signals
from ufsfile import UFSData
from utils import clean_filename, now_string

# Logger for this module. 
_log = logging.getLogger(__name__)

#: Reference to the currently loaded data as a zarr group.
d = zarr.group()

#: Path to the currently loaded zarr data array in :attr:`d`.
d_path = ""

# Suffix to indicate temporary data stored on disk
_temp_suffix = "-temporary.tr.zarr"

#: Flag to indicate the currently loaded data is not saved to disk. It might be exclusively in RAM
#: or on disk as a temporary data set. It's possible to have data in RAM that doesn't need saving
#: though.
d_unsaved = False

#: Reference to temporary data which doesn't need to be saved to disk or can be rebuilt from :attr:`d`.
t = zarr.group()

#: Attributes to include in the root of the zarr array.
root_attrs = {
    "description"       : "Time-resolved spectroscopy data",
    "format"            : "trdata",
    "version"           : "1.0.0",
    "creation_software" : "trspectrometer",
}


def new_zarr(location=""):
    """
    Generate a new empty data set.

    The directory location for the data files can be specified with the ``location`` parameter. If
    ``location`` is an empty string (``""``), then an attempt at creating an automatically named
    directory will be made. If the directory is unable to be created, or ``location=None``, then the
    new data set will be stored in RAM instead and will be lost if not saved to disk at some later
    stage.

    Note that if the creation of the new data set succeeds, any existing unsaved data will be lost
    without warnings.

    The function will return the absolute path of the created data set, or an empty string if the
    data set was created in RAM only.

    :param location: Directory to use as storage for the new data set files.
    :returns: Location on disk of the data set, or ``""`` if in RAM.
    """
    
    global d, d_path, d_unsaved, t, _temp_suffix
    
    if location == "":
        # Use auto generated name
        location = os.path.abspath(os.path.join(config.data["directories"]["data"], f"{time.strftime('%y%m%d-%H%M%S', time.localtime())}{_temp_suffix}"))
    elif location is not None:
        # Some location was specified
        if not os.path.isabs(location):
            # Relative path, convert to absolute path from configured data directory
            location = os.path.abspath(os.path.join(os.path.join(config.data["directories"]["data"], location)))
        if not location.endswith(".tr.zarr"):
            # Append suffix if needed
            location = location + ".tr.zarr"
    
    if location:
        # Create the data set on disk
        if os.path.exists(location):
            # Don't overwrite existing data
            raise FileExistsError(f"Data location already exists: {location}")
        if not os.access(os.path.dirname(location), os.W_OK):
            # Can't write to location
            raise PermissionError(f"Data location not writable: {location}")
        data = zarr.group(store=location)
    else:
        # Location was specified as None, create in RAM
        data = zarr.group()
        location = ""
    data.attrs.update(root_attrs)
    data.attrs.update({"creation_time" : now_string()})

    # Creation successful, start using the new data set
    d = data
    d_path = location
    d_unsaved = False  # Nothing useful yet, no need to save
    t = zarr.group()
    _log.info("New data set created" + (f" at {location}" if location else "."))
    return location


def new_raw_zarr(location=""):
    """
    Generate a new data set containing some blank raw data.

    The directory location for the data files can be specified with the ``location`` parameter. If
    ``location`` is an empty string (``""``), then an attempt at creating an automatically named
    directory will be made. If the directory is unable to be created, or ``location=None``, then the
    new data set will be stored in RAM instead and will be lost if not saved to disk at some later
    stage.

    :param location: Directory to use as storage for the new data set files.
    :returns: Location on disk of the data set, or ``""`` if in RAM.
    """
    global d, d_path, d_unsaved, t
    new_zarr(location)
    d.create_group("raw")
    d["raw"].array("wavelength", data=np.array([500.0], dtype=np.float32))
    d["raw"].array("time", data=np.array([0.0], dtype=np.float32))
    d["raw"].full("data", np.nan, shape=(0, 1, 1), dtype=np.float32)
    d["raw/wavelength"].attrs["units"] = config.data["rawdata"]["units"]["wavelength"]
    d["raw/time"].attrs["units"] = config.data["rawdata"]["units"]["time"]
    d["raw/data"].attrs["units"] = config.data["rawdata"]["units"]["data"]
    return d_path


def open_zarr(parent=None, initial_dir=None):
    """
    Show a dialog for selecting a time-resolved data directory, and load the data.

    The native format for data is a Zarr data directory.
    If the selected directory does not appear to contain time-resolved data,
    a RuntimeError will be raised.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    :returns: Name of selected data directory, or ``None`` if no directory selected.
    """
    global d, t, d_path, d_unsaved
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    # Was hoping that using a filter and directory options would limit to 
    # selection of dirname.zarr, but it doesn't quite work that way...
    qfd = QFileDialog(parent, "Open Time-resolved Data", initial_dir, "Zarr data directory (*)")
    qfd.setAcceptMode(QFileDialog.AcceptOpen)
    qfd.setFileMode(QFileDialog.Directory)
    qfd.setOption(QFileDialog.ShowDirsOnly)
    if qfd.exec_():
        dirname = qfd.selectedFiles()[0]
        try:
            # Open read-only to prevent inadvertent modifications to data
            data = zarr.open(dirname, mode="r")
        except:
            raise RuntimeError(f"Unable to read {dirname}:\nNot a Zarr data directory.")
        if not "format" in data.attrs or not data.attrs["format"] == "trdata":
            # Originally had capitalised "Format" field, keep compatible with that
            if not "Format" in data.attrs or not data.attrs["Format"] == "trdata":
                raise RuntimeError(f"Unable to read {dirname}:\nNot time-resolved data.")
        # Looks OK, switch in the loaded data
        d = data
        t = zarr.group()
        # Copy data and which may be modified to temporary storage
        if ("raw" in d) and ("exclude_scans" in d["raw"].attrs):
            t.create_group("raw")
            t["raw"].attrs["exclude_scans"] = d["raw"].attrs["exclude_scans"]
        d_path = dirname
        d_unsaved = False
        return dirname
    return None


def save_zarr(parent=None, initial_dir=None, data=None):
    """
    Show a dialog for selecting the save directory location for time-resolved data.

    The native format for data is a Zarr data directory.
    If the Zarr `data` is not provided, the currently loaded data will be saved.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    :param data: Zarr data to save.
    :returns: Directory where data was saved, or ``None`` if no directory selected.
    """
    # If data not given, default to currently loaded data
    global d, t, d_path, d_unsaved, _temp_suffix
    if data is None:
        if d is None: return None
        data = d
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    qfd = QFileDialog(parent, "Save Time-resolved Data", initial_dir, "Zarr data directory (*)")
    qfd.setAcceptMode(QFileDialog.AcceptSave)
    qfd.setFileMode(QFileDialog.Directory)
    qfd.setOption(QFileDialog.ShowDirsOnly)
    # Suggest a file name based on stored metadata fields
    datecode = time.strftime("%y%m%d_%H%M%S", time.localtime())
    # Use updated metadata fields stored in temporary data storage if they exist
    try:
        if "sample" in t["raw"].attrs:
            samplename = t["raw"].attrs["sample"]
        else:
            samplename = data["raw"].attrs["sample"]
        if samplename: samplename = "-" + samplename
    except:
        samplename = ""
    try:
        if "pump" in t["raw"].attrs:
            pumpname = t["raw"].attrs["pump"]
        else:
            pumpname = data["raw"].attrs["pump"]
        if pumpname: pumpname = "-" + pumpname
    except:
        pumpname = ""
    qfd.selectFile(clean_filename(f"{datecode}{samplename}{pumpname}.tr.zarr"))
    dirname = None
    while qfd.exec_():
        dirname = qfd.selectedFiles()[0]
        if dirname == d_path:
            # Selected data dir is the one currently open
            reply = QMessageBox.question(parent, "TRSpectrometer", "Selected data directory is the one currently open. Do you want to overwrite its contents?")
            if reply == QMessageBox.No:
                # Show selection dialog again
                dirname = None
                continue
            else:
                # Just need to update currently open data directory, enable write
                dest = zarr.open(dirname, mode="r+")
        else:
            # Selected data dir is not the one currently open
            # QFileDialog creates the directory before the suffix is appended, delete it if empty
            try:
                os.rmdir(dirname)
            except Exception as ex:
                pass
            # Ensure name has a .tr.zarr suffix
            dirname = dirname.partition(".tr.zarr")[0] + ".tr.zarr"
            # Check if currently using a temporary storage location
            if d_path.endswith(_temp_suffix):
                # Can just move the whole directory
                try:
                    shutil.move(d_path, dirname)
                except:
                    # Failed to move for whatever reason, directory could exist etc
                    reply = QMessageBox.information(parent, "TRSpectrometer", "Unable to create data directory in the selected location. Please choose another location or name.")
                    initial_dir = dirname
                    dirname = None
                    continue
                # Open the new location for writing
                dest = zarr.open(dirname, mode="r+")
            else:
                # Data in RAM or non-temporary location on disk
                try:
                    dest = zarr.open(dirname, mode="w-")
                except Exception as ex:
                    # Failed with "w-" mode as directory already exists
                    reply = QMessageBox.question(parent, "TRSpectrometer", "Selected data directory already exists. Do you want to overwrite its contents?")
                    if reply == QMessageBox.No:
                        # Show selection dialog again
                        initial_dir = dirname
                        dirname = None
                        continue
                    else:
                        # Force overwrite of directory
                        dest = zarr.open(dirname, mode="w")
                # Copy the data over to new destination
                try:
                    zarr.copy_all(data, dest)
                    # Root attributes don't get copied. Bug in zarr 2.5.0
                    dest.attrs.update(data.attrs)
                except Exception as ex:
                    raise RuntimeError(f"Unable to write {dirname}:\n{ex}")
        # Save out data modifications from temporary storage
        def update_attr(attr_name):
            if ("raw" in t) and (attr_name in t["raw"].attrs):
                if "raw" not in dest:
                    dest.create_group("raw")
                dest["raw"].attrs[attr_name] = t["raw"].attrs[attr_name]
        for attr in ["exclude_scans", "sample", "pump", "operator", "note"]:
            update_attr(attr)
        # Done. Start using new data directory in read-only mode
        d_path = dirname
        d_unsaved = False
        d = zarr.open(dirname, "r")
        break
    return dirname


def prompt_unsaved(parent=None, initial_dir=None):
    """
    Check if the current data set is unsaved and prompt to save or discard it.

    The function will return ``True`` if the data was handled OK, or ``False`` if the user cancelled
    the operation or something went wrong.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
    :returns: ``True`` if data was handled successfully.
    """
    global d, d_path, d_unsaved, t, _temp_suffix
    if not d_path:
        # Data in RAM
        if not d_unsaved:
            # Unsaved flag not set, nothing to do
            return True
        # Save needed
        reply = QMessageBox.question(parent, "TRSpectrometer",
                        "The current data set has not been saved.\nWould you like to save the existing data, or discard it?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Save:
            if save_zarr(parent, initial_dir):
                # Saved OK, job done
                return True
        elif reply == QMessageBox.Discard:
            # Allow data in RAM to be lost
            return True
        # Cancelled, or not saved properly
        return False
    elif d_path.endswith(_temp_suffix):
        # Data in temporary disk storage, prompt for save (regardless of unsaved flag)
        reply = QMessageBox.question(parent, "TRSpectrometer",
                        f"The current data set is in temporary storage on disk at:\n\n{os.path.dirname(d_path)}{os.sep}\n{os.path.basename(d_path)}\n\n"
                        "Would you like to save it elsewhere, discard it, or ignore it and leave the temporary files on disk?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Ignore | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Save:
            if save_zarr(parent, initial_dir):
                # Saved OK, job done
                return True
        elif reply == QMessageBox.Discard:
            # Delete the temporary files
            d_path_old = d_path
            # We'll make new data, in case there's issues deleting open files (on Windows...)
            new_raw_zarr(location=None)
            signals.data_changed.emit(False)
            try:
                shutil.rmtree(d_path_old)
            except:
                _log.warning(f"Unable to delete temporary data at {d_path_old}")
                QMessageBox.warning(parent, "TRSpectrometer", f"An error occurred while removing temporary files at:\n{d_path_old}\nYou may wish to try deleting these files manually later.")
            return True
        elif reply == QMessageBox.Ignore:
            # Ignore and leave data on disk, nothing to do
            return True
        # Cancelled, or not saved properly
        return False
    else:
        # Data on disk, not in temporary storage
        if not d_unsaved:
            # Unsaved flag not set, nothing to do
            return True
        # Data modified, save needed
        reply = QMessageBox.question(parent, "TRSpectrometer",
                        "The current data set has been modifed but not yet saved.\nWould you like to apply the changes to the existing data, save a new data set, or discard the modifications?",
                        QMessageBox.Apply | QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Save:
            if save_zarr(parent, initial_dir):
                # Saved OK, job done
                return True
        elif reply == QMessageBox.Discard:
            # Allow changes to be lost
            return True
        elif reply == QMessageBox.Apply:
            # Save temporary structures to disk
            try:
                # Enable write
                d = zarr.open(d_path, mode="r+")
                if ("raw" in t) and ("exclude_scans" in t["raw"].attrs):
                    if "raw" not in d:
                        d.create_group("raw")
                    d["raw"].attrs["exclude_scans"] = t["raw"].attrs["exclude_scans"]
                d_unsaved = False
                d = zarr.open(d_path, "r")
            except:
                _log.warning(f"Unable to update data at {d_path}")
                QMessageBox.warning(parent, "TRSpectrometer", f"An error occurred while updating the data at:\n{d_path}")
        # Cancelled, or not saved properly
        return False

        

def import_raw(parent=None, initial_dir=None):
    """
    Show a dialog for selecting non-native time-resolved data file(s), and return the data.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    :returns: Tuple of selected file name(s) and zarr data.
    """
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    # File type definitions
    type_csv = "CSV Files (*.csv *.csv? *.csv??)"
    type_ufs = "UFS Files (*.ufs)"
    filenames, filetype = QFileDialog.getOpenFileNames(parent, "Import Time-resolved Data", initial_dir, f"{type_csv};;{type_ufs}")
    if not filenames: return None, None
    if filetype == type_csv:
        data_matrix, warning_msgs = load_csv_matrix(filenames)
        if data_matrix.shape < (1, 2, 2):
            raise RuntimeError(f"Unable to interpret valid data from selected files.")
        # Transpose from (scan, wavelength, time) to (scan, time, wavelength)
        data_matrix = np.swapaxes(data_matrix, 1, 2)
        # Build the zarr data array
        data = zarr.group()
        data.attrs.update(root_attrs)
        data.create_group("raw")
        data["raw"].array("wavelength", data=np.mean(data_matrix[:,0,1:], axis=0))
        data["raw"].array("time", data=np.mean(data_matrix[:,1:,0], axis=0))
        data["raw"].array("data", data=data_matrix[:,1:,1:])
        data["raw/wavelength"].attrs["units"] = config.data['rawdata']['units']['wavelength']
        data["raw/time"].attrs["units"] = config.data['rawdata']['units']['time']
        data["raw/data"].attrs["units"] = config.data['rawdata']['units']['data']
    elif filetype == type_ufs:
        ufs = [ UFSData(ufsfile=f) for f in filenames ]
        # UFS files can potentially contain multiple scans.
        # Use the wavelength and time axes from the first file and if the
        # shape of subsequent file data matches, include it as additional scans.
        warning_msgs = ""
        data_matrices = []
        for i, u in enumerate(ufs):
            if not u.data_matrix.shape == ufs[0].data_matrix.shape:
                warning_msgs += f"Matrix shape of {os.path.basename(filenames[i])} does not match other files, skipping.\n"
                ufs.remove(u)
            else:
                data_matrices.append(np.swapaxes(u.data_matrix, 1, 2))
        data_matrices = np.concatenate(data_matrices, axis=0)
        # Build the zarr data array
        data = zarr.group()
        data.attrs.update(root_attrs)
        data.create_group("raw")
        data["raw"].array("wavelength", data=ufs[0].axis1_data)
        data["raw"].array("time", data=ufs[0].axis2_data)
        data["raw"].array("data", data=data_matrices)
        data["raw/wavelength"].attrs["units"] = ufs[0].axis1_units
        data["raw/time"].attrs["units"] = ufs[0].axis2_units
        data["raw/data"].attrs["units"] = "DeltaA" if ufs[0].data_units == "DA" else ufs[0].data_units
        data["raw"].attrs["ufs_metadata"] = ufs[0].metadata
    # Alert if any warnings for invalid files etc
    if warning_msgs:
        QMessageBox.warning(parent, "Warnings during import", warning_msgs)
    # Abbreviate filename list if needed
    if len(filenames) > 1:
        filename = f"{os.path.basename(filenames[0])} and {len(filenames) - 1} other{'s' if len(filenames) > 2 else ''}"
    else:
        filename = os.path.basename(filenames[0])
    return filename, data


def load_csv_matrix(filenames, cleanrows=95, cleancols=95):
    """
    Load a list of CSV files containing data matrices.

    The CSV data in each file must have identical shapes (number of rows and columns).
    Any file where the shape does not match the first loaded file will be ignored.

    :param filenames: List of CSV file names to load data from.
    :returns: Numpy array containing file data.
    """
    warning_messages = ""
    data_matrices = []
    for filename in filenames:
        try:
            warnings.simplefilter('ignore') # ignore any mismatched line lengths (text/metadata at end of file)
            data_matrices.append(np.genfromtxt(filename, delimiter=',', dtype=np.float32, invalid_raise=False))
            warnings.simplefilter('default')
        except OSError:
            warning_messages += f"Error opening {os.path.basename(filename)}, skipping.\n"
            continue
        # Ensure shape of each matrix matches the first file
        if not data_matrices[len(data_matrices)-1].shape == data_matrices[0].shape:
            warning_messages += f"Matrix shape of {os.path.basename(filename)} does not match other files, skipping.\n"
    # Ignore files if matrix shapes don't match
    data_matrices = np.stack([ x for x in data_matrices if x.shape == data_matrices[0].shape ], 0)
    
    # Convert any infs to nans
    data_matrices[np.logical_not(np.isfinite(data_matrices))] = np.nan

    # Remove wavelengths/rows with too many nan values
    if cleanrows < 100:
        cleanrows = max(0, cleanrows)
        mask = np.sum(np.isfinite(data_matrices[:,:,1:]), axis=2) >= (1.0 - cleanrows/100.0)*(data_matrices.shape[2] - 1)
        # Remove rows from all scans so dimensions still match
        mask = np.all(mask, axis=0) 
        data_matrices = data_matrices[:,mask]
        #print('Removed rows with more than {}% invalid data. New matrix shape: {}'.format(cleanrows, data_matrices[0].shape))
    
    # Remove times/columns with too many nan values
    if cleancols < 100:
        cleancols = max(0, cleancols)
        mask = np.sum(np.isfinite(data_matrices[:,1:,:]), axis=1) >= (1.0 - cleancols/100.0)*(data_matrices.shape[1] - 1)
        # Remove columns from all scans so dimensions still match
        mask = np.all(mask, axis=0)
        data_matrices = data_matrices[:,:,mask]
        #print('Removed columns with more than {}% invalid data. New matrix shape: {}'.format(cleancols, data_matrices[0].shape))

    return data_matrices, warning_messages


def export_raw_average(parent=None, initial_dir=None):
    """
    Show a dialog for saving out the average of the selected raw data traces to a non-native data file.

    :param parent: The parent QWidget for the dialog box.
    :param initial_dir: Initial directory for the dialog box.
        If `None`, then the data directory specified in the configuration will be used.
    """
    if initial_dir is None:
        initial_dir = config.data["directories"]["data"]
    # Suggest a file name based on stored metadata fields
    datecode = time.strftime("%y%m%d_%H%M%S", time.localtime())
    # Use updated metadata fields stored in temporary data storage if they exist
    try:
        if "sample" in t["raw"].attrs:
            samplename = t["raw"].attrs["sample"]
        else:
            samplename = d["raw"].attrs["sample"]
        if samplename: samplename = "-" + samplename
    except:
        samplename = ""
    try:
        if "pump" in t["raw"].attrs:
            pumpname = t["raw"].attrs["pump"]
        else:
            pumpname = d["raw"].attrs["pump"]
        if pumpname: pumpname = "-" + pumpname
    except:
        pumpname = ""
    initial_filename = os.path.join(initial_dir, clean_filename(f"{datecode}{samplename}{pumpname}"))
    # File type definitions
    type_csv = "CSV Files (*.csv)"
    type_ufs = "UFS Files (*.ufs)"
    filename, filetype = QFileDialog.getSaveFileName(parent, "Export Raw Data Average", initial_filename, f"{type_csv};;{type_ufs}")
    if not filename: return None
    if filetype == type_csv:
        # Ensure name has a .csv suffix
        filename = filename.partition(".csv")[0] + ".csv"
        # Attach wavelength and time axis to data matrix
        data_average = raw_data_average()
        data = np.zeros((data_average.shape[1] + 1, data_average.shape[0] + 1))
        data[1:,1:] = data_average.T
        data[1:,0] = d["raw/wavelength"]
        data[0,1:] = d["raw/time"]
        np.savetxt(filename, data, fmt="%g", delimiter=",")
    elif filetype == type_ufs:
        # Ensure name has a .ufs suffix
        filename = filename.partition(".ufs")[0] + ".ufs"
        # Build a UFSData object
        ufs = UFSData()
        ufs.version = "Version2".encode("utf-8")
        ufs.axis1_label = "Wavelength".encode("utf-8")
        ufs.axis1_units = d["raw/wavelength"].attrs["units"].encode("utf-8")
        ufs.axis1_data = d["raw/wavelength"]
        ufs.axis2_label = "Time".encode("utf-8")
        ufs.axis2_units = d["raw/time"].attrs["units"].encode("utf-8")
        ufs.axis2_data = d["raw/time"]
        ufs.data_units = ("DA" if d["raw/data"].attrs["units"] == "DeltaA" else d["raw/data"].attrs["units"]).encode("utf-8")
        ufs.data_matrix = np.swapaxes(raw_data_average(), 0, 1)[np.newaxis,:,:]
        # TODO: Could actually put something useful in here...
        ufs.metadata = "".encode("utf-8")
        ufs.write_file(filename)
    return filename


def raw_data_average():
    """
    Compute and return the average of the raw data set.

    This routine will use the "exclude_scans" attribute of raw to exclude scans from the average.
    The attribute should contain a list of scan indices to exclude.

    :returns: Array containing the averaged data.
    """
    if (not "raw" in d) or (not "raw/data" in d): return None
    if not "raw" in t:
        t.create_group("raw")
    if not "exclude_scans" in t["raw"].attrs:
        # Include all scans if not specified yet
        t["raw"].attrs["exclude_scans"] = []
    if  0 < len(t["raw"].attrs["exclude_scans"]) < d["raw/data"].shape[0]:
        # Multiple scans included, average them
        selection_mask = np.ones((d["raw/data"].shape[0]), dtype=bool)
        selection_mask[t["raw"].attrs["exclude_scans"]] = False
        # Ignore warning if all NaNs in slice
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = np.nanmean(d["raw/data"].get_orthogonal_selection((selection_mask, slice(None), slice(None))), axis=0)
    else:
        # Zero or all scans selected
        # Ignore warning if all NaNs in slice
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = np.nanmean(d["raw/data"], axis=0)
    return result


def find_stepsizes(time_axis, filter_window=35, snap=0.05):
    """
    Generate a list of time step sizes from a given time axis label array.

    :param time_axis: Array of time axis values.
    :param filter_window: Width of filtering window to apply, in array indices.
    :param snap: Minimum step size permitted. Step sizes will be snapped to multiples of this value.
    :returns: List of [count, step_size] pairs.
    """
    if time_axis.shape[0] < 2: return []
    steps = np.round(snap*np.round(median_filter(np.diff(time_axis.astype(np.float64)), size=filter_window)/snap), 6)
    steplist = [ [0, steps[0]] ]
    for x in steps:
        if x == steplist[-1][1]:
            # Repeated step size
            steplist[-1][0] += 1
        else:
            # New step size
            steplist.append([1, x])
    return steplist
