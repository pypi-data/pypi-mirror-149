Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-tpa2016/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/tpa2016/en/latest/
    :alt: Documentation Status

.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_TPA2016/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_TPA2016/actions/
    :alt: Build Status

CircuitPython driver for TPA2016 Class D Amplifier.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
--------------------
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-tpa2016/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-tpa2016

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-tpa2016

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-tpa2016

Usage Example
=============

.. code-block:: python3

    import adafruit_tpa2016
    import busio
    import board

    i2c = busio.I2C(board.SCL, board.SDA)
    tpa = adafruit_tpa2016.TPA2016(i2c)

    tpa.fixed_gain = -16

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/tpa2016/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_TPA2016/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
