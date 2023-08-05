#!/usr/bin/env python3
import os
import sys
import shutil
import setuptools

# Workaround issue in pip with "pip install -e --user ."
import site
site.ENABLE_USER_SITE = True

with open("README.rst", "r") as fh:
    long_description = fh.read()

"""
Implements the distutils 'install' command to install service startup files.
"""
from setuptools.command.install import install
class CustomInstallCommand(install):

    def initialize_options(self):
        install.initialize_options(self)
        # Enable recording of installed files
        self.record = "installed_files.txt"
        self.file_list = []

    def run(self):
        if sys.platform.startswith("linux"):
            # xdg-icon-resource doesn't support svg, so do it manually
            if os.access("/usr/share/icons/hicolor/scalable/apps/", os.W_OK):
                try:
                    shutil.copy("trspectrometer/resources/trspectrometer.svg", "/usr/share/icons/hicolor/scalable/apps/")
                    self.file_list.append("/usr/share/icons/hicolor/scalable/apps/trspectrometer.svg")
                except:
                    print("Error installing trspectrometer.svg icon to system directory.")
                else:
                    print("Installed trspectrometer.svg icon to system directory.")
            else:
                try:
                    shutil.copy("trspectrometer/resources/trspectrometer.svg", os.path.join(os.path.expanduser("~"), ".local/share/icons/hicolor/scalable/apps/"))
                    self.file_list.append(os.path.join(os.path.expanduser("~"), ".local/share/icons/hicolor/scalable/apps/trspectrometer.svg"))
                except Exception as ex:
                    print("Error installing trspectrometer.svg icon to user directory.")
                    print(ex)
                else:
                    print("Installed trspectrometer.svg icon to user directory.")
            # Install png icon
            try:
                os.system("xdg-icon-resource install --novendor --size 48 trspectrometer/resources/trspectrometer-48.png")
                os.system("xdg-icon-resource install --novendor --size 48 trspectrometer/resources/trspectrometer-96.png")
                os.system("xdg-icon-resource install --novendor --size 256 trspectrometer/resources/trspectrometer-256.png")
            except:
                print("Error installing trspectrometer.png icons.")
            else:
                print("Installed trspectrometer.png icons.")
            # Install .desktop file
            try:
                os.system("xdg-desktop-menu install --novendor trspectrometer/resources/trspectrometer.desktop")
            except:
                print("Error installing trspectrometer.desktop launcher.")
            else:
                print("Installed trspectrometer.desktop launcher.")

        elif sys.platform.startswith("win32"):
            # TODO
            print("Windows OS detected. Installation of launcher shortcuts is not yet implemented.")

        install.run(self)


    def get_outputs(self):
        """
        Append any custom install files to the file record list.
        """
        outputs = install.get_outputs(self)
        outputs.extend(self.file_list)
        return outputs


"""
Implements the distutils 'develop' command to install service startup files.
"""
from setuptools.command.develop import develop
class CustomDevelopCommand(develop):
    pass


"""
Implements a custom distutils 'uninstall' command.
"""
from distutils.core import Command
class CustomUninstallCommand(Command):

    description = "Uninstall trspectrometer, including launcher and icon files."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if sys.platform.startswith("linux"):
            try:
                os.system("xdg-desktop-menu uninstall trspectrometer.desktop")
            except:
                print("Error uninstalling trspectrometer.desktop launcher.")
            else:
                print("Uninstalled trspectrometer.desktop launcher.")
            try:
                os.system("xdg-icon-resource uninstall --size 48 trspectrometer.png")
            except:
                print("Error uninstalling trspectrometer.png icon.")
            else:
                print("Uninstalled trspectrometer.png icon.")

        with open("installed_files.txt") as fd: filelist = fd.readlines()
        for f in filelist:
            try:
                os.remove(f.strip())
                print(f"Removed file: {f.strip()}")
            except Exception as ex:
                pass
            dirname = os.path.dirname(f.strip())
            if "trspectrometer" in dirname:
                try:
                    os.removedirs(dirname)
                    print(f"Removed directory: {dirname}")
                except Exception as ex:
                    pass


setuptools.setup(
    name="trspectrometer",
    version="1.2.2",
    author="Patrick Tapping",
    author_email="mail@patricktapping.com",
    description="Software for running a time-resolved spectrometer.",
    long_description=long_description,
    url="https://gitlab.com/ptapping/trspectrometer",
    project_urls={
        "Documentation": "https://trspectrometer.readthedocs.io/",
        "Source": "https://gitlab.com/ptapping/trspectrometer",
        "Tracker": "https://gitlab.com/ptapping/trspectrometer/-/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PySide6==6.2.1",
        "pyqtgraph",
        "numpy",
        "scipy",
        "opencv-python-headless",
        "tomlkit",
        "appdirs",
        "zarr",
        "pyreadline",
        "pluginlib",
        "thorlabs_apt_device",
        "thorlabs_mc2000b",
        "andor3",
        "trs-interface"
    ],
    package_data={
        "": [ "*.ui" ],
        #"": [ "pyqtgraph/icons/*.png" ]
    },
    entry_points={
        "console_scripts": [
            "trspectrometer = trspectrometer:main",
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'uninstall' : CustomUninstallCommand,
    },
)
