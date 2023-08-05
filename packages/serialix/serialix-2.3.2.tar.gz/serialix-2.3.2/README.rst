serialix
=======================================

About
--------------------------------------
``serialix`` is a powerful and easy-to-use tool that provides a unified interaction layer for various human-readable data serialization languages (like ``json``, ``yaml``, etc). Due to the how this tool designed, all the supported languages share the identical base between each other, meaning that process of working with those languages will be almost the same. This tool can also be extended for your purposes or even your own serialization language parser support.

Usage example
--------------------------------------
``serialix`` is very easy to use:

.. code:: python

    >>> from serialix import Serialix, JSON_Format                        # Import `Serialix` main class
    >>> default_settings = { 'version': '1.23.2' }                        # Specify the default values for our file
    >>> cfg = Serialix(JSON_Format, './settings.json', default_settings)  # Create serialix object for `json` format.
                                                                          # Local file will be automatically created.
    >>> cfg['version']                                                    # Read the `version` key
    '1.23.2'
    >>> cfg['version'] = '2.0.0'                                          # Change the `version` key value
    >>> cfg['version']                                                    # Read the values of `version` key again
    '2.0.0'
    >>> cfg.commit()                                                      # Commit the changes to local `settings.json` file

Supported Languages
--------------------------------------
List of currently supported languages parsers.

- Native Support
    - ``json``
- External Support
    - ``ujson`` *(replacement for python built-in json parser)*
    - ``yaml`` *(version <= 1.2)*
    - ``toml``

..

    Languages, listed in **Native Support** are supported by python without any external packages, while **External Support** requires external packages to be installed. For more detailed information go here: `Intallation Guide <https://maximilionus.github.io/serialix/guide_installation.html>`__

Documentation
--------------------------------------
All information about this package installation and usage is located in documentation `on this link <https://maximilionus.github.io/serialix/index.html>`__
