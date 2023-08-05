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
Handle loading, storing, saving, and default values for program settings.
"""

import os
import io
import logging
import atexit
import re

import tomlkit
import appdirs


def set_defaults():
    update(tomlkit.parse(
"""
[rawdata]

[rawdata.units]
# Default units for wavelength axis
wavelength = "nm"
# Default units for time axis
time = "ps"
# Default units for samples
data = "ΔA"

[directories]
# Default directory to find data files
data = ""
# List of directories containing user plugin modules
plugins = []

[plugins]
# List of plugin modules to load
load = ["aligncam", "delay", "chopper", "detector", "interface", "acquisition", "scope"]

[hardware]

# Whether to search for and initialise hardware devices.
# If set to false, no hardware detection will take place.
# The software will still be usable for data visualisation and analysis.
init_hardware = true

# In the future we may be able to detect laser rep rate.
# For the meantime a temporary config option will do.
# Rate in Hz.
laser_reprate = 1000
"""
    ))
    # Set default directories
    if not data["directories"]["data"]:
        data["directories"]["data"] = os.path.expanduser("~")


def read(reset=False):
    """
    Read and update configuration from the configuration file.

    If ``reset=True`` the current configuration will be reset prior to reading the file, otherwise
    the configuration will be preserved and only be updated with any values stored in the file.

    :param reset: Reset current configuration before reading file.
    """
    global data
    newconfig = tomlkit.toml_document.TOMLDocument() if reset else data.copy()
    try:
        with io.open(configfile, encoding="utf-8") as f:
            _update_dict(newconfig, tomlkit.loads(f.read()))
    except:
        _log.exception(f"Error reading configuration from file {configfile}")
        return
    data = newconfig


def write():
    """
    Write the current configuration out the the configuration file.
    """
    # The tomlkit library seems to have a bug where it keeps adding newlines after tables.
    # So after a few load-save cycles the newline start to get out of hand.
    # The regex is a dodgy hack to remove any triple+ newlines.
    try:
        with io.open(configfile, "w", encoding="utf-8", newline="\n") as f:
            f.write(re.sub("\n\n\n*", "\n\n", data.as_string()))
    except:
        _log.exception(f"Error writing configuration to file {configfile}")


def update(newdict):
    """
    Update the current configuration using the provided dictionary.

    Any existing configuration entries will be overwritten by the new values.

    :param newdict: Dictionary of updated configuration values.
    """
    _update_dict(data, newdict)


def _update_dict(olddict, newdict):
    """Recursively update dicts."""
    for k, _ in newdict.items():
        if k in olddict and isinstance(olddict[k], dict) and isinstance(newdict[k], dict):
            # Recurse into sub-dicts
            _update_dict(olddict[k], newdict[k])
        else:
            # Overwrite existing values from newdict
            olddict[k] = newdict[k]


def add_defaults(defaultsdict):
    """
    Update the current configuration using the provided dictionary of default values.

    Existing entries in the current configuration will not be overwritten. This allows adding any
    missing default values to the configuration without overwriting values which may already exist.

    :param defaultsdict: Dictionary of default configuration values.
    """
    _add_defaults(data, defaultsdict)


def _add_defaults(olddict, defaultsdict):
    """Recursively add values to a dictionary if the value does not already exist."""
    for k, _ in defaultsdict.items():
        if k in olddict and isinstance(olddict[k], dict) and isinstance(defaultsdict[k], dict):
            # Recurse into sub-dicts
            _add_defaults(olddict[k], defaultsdict[k])
        elif not k in olddict:
            # Add missing values from defaults dict
            olddict[k] = defaultsdict[k]


def plugin_dirs():
    """
    Return the list of plugin directories from configuration file, but also append the built-in
    plugin directory.

    :returns: List of configured plugin directories.
    """
    plugin_dirs = data["directories"]["plugins"].copy()
    builtin_dir = os.path.join(os.path.dirname(__file__), "plugins")
    if not builtin_dir in plugin_dirs:
        plugin_dirs.append(builtin_dir)
    return plugin_dirs


# Module init ##################################################################

_log = logging.getLogger(__name__)

#: Reference to the main window class instance.
mainwindow = None

#: Path to the configuration file.
configfile = os.path.join(appdirs.user_config_dir("trspectrometer", False), "trspectrometer.toml")
_log.info(f"Configuration file location is {configfile}")

# Start with empty TOMLDocument, add defaults, then load/overwrite from file
#: Data structure holding the configuration as a TOMLDocument.
data = tomlkit.toml_document.TOMLDocument()
set_defaults()
if not os.access(configfile, os.F_OK):
    # Create new file
    _log.info("Configuration file doesn't exist, creating default")
    try:
        os.mkdir(os.path.dirname(configfile))
    except FileExistsError:
        pass
    except:
        _log.exception(f"Unable to create directory for configuration at {os.path.dirname(configfile)}")
        pass
    write()
read(reset=False)

# Save back out to disk when application shuts down
atexit.register(write)
