"""
Plugins
=======

The plugins package is a directory tree containing python modules which may be dynamically loaded by
the TRSpectrometer application.

The modules are loaded automatically if the module name is included in the ``load`` list within the
``[plugins]`` section of the configuration file. For example

.. code-block:: toml

    [plugins]
    # List of plugin modules to load
    load = ["aligncam", "acquisition"]

will act similar to an ``from plugins import aligncam, acquisition`` statement.

Note that module-level code is executed on import, allowing the module to perform arbitrary actions.
This may be used to extend the functionality of the application, such as adding additional menu
items or user interface elements. By default, the application does no further actions on the module
other than the import.

Hardware Plugins
================

A "hardware plugin" is a normal plugin module, but must also:

  - Implement a ``init()`` method to connect to and initialise the device(s).
  - Implement a ``close()`` method to disconnect from devices and free any used resources.
  - Implement a ``statuspanel`` property to return a QWidget class type
    (not an instance of the class!) to display device status information in the
    hardware status panel. This may be ``None`` if no panel is required.
  - Add a reference to itself to the :data:`hardware.modules` dictionary, for example using
    ``hardware.modules[__name__] = sys.modules[__name__]``.

Calling of the plugin's ``init()`` and ``close()`` methods will be handled automatically,
as will creation and display of the ``statuspanel`` if provided.
"""