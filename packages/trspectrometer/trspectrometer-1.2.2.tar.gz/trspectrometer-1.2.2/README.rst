TRSpectrometer
==============

TRSpectrometer is a platform for time-resolved spectroscopy, encompassing both software and hardware
designs. It can be used for both data acquisition, as well as viewing data and basic analysis.

Features:

- Completely open source hardware and software designs. Don't get stuck with inflexible and buggy
  proprietary software!

- Plugin architecture to ease modifications and integration of new hardware devices or experimental methods.
 
- Supports the latest rapid-acquisition techniques.

- Cross platform python - Linux, Windows, MacOS.

The aim of the software is to be as open and flexible as possible, using a plugin system for the
addition and customisation of features and functionality. For example, the same software that runs
on a Windows machine acquiring data can be installed on a Linux or Mac OS computer and used for data
viewing and analysis without restriction. The majority of the code base is written in Python, making
development and modifications (hopefully!) more accessible to students and researchers who lack
specific programming backgrounds.

The initial 1.0 version includes a reference hardware design for a transient absorption
(pump--probe) spectrometer and a cross-platform software application for data acquisition and basic
data exploration and analysis. In time, it is hoped that the platform will support a wider variety
of hardware and additional time-resolved experimental techniques, as well as adding more advanced
data exploration, analysis, and plotting tools. This will only truly be possible through
contributions by users and other interested parties. See the Contributing page in the documentation
for more information.

Installation
------------

The latest release can be downloaded and installed using the Package Installer for Python (pip):

.. code-block:: sh

    pip install --upgrade trspectrometer

On Linux, a launcher icon should be installed in your menus (this feature is not yet implemented on Windows or MacOS).
On all operating systems, the application can be launched from the command line:

.. code-block:: sh

    trspectrometer

Further details can be found in the `Getting Started <https://trspectrometer.readthedocs.io/en/latest/gettingstarted.html>`__ section of the documentation.


Support
-------

Documentation can be read online at `Read the Docs <https://trspectrometer.readthedocs.io/>`__.

Bug reports, feature requests and suggestions can be submitted to the `issue tracker <https://gitlab.com/ptapping/trspectrometer/-/issues>`__.


License
-------

All original work is free and open source, licensed under the GNU Public License.
See the `LICENSE.txt <https://gitlab.com/ptapping/trspectrometer/-/blob/main/LICENSE.txt>`__ for details.
