redlibssh
============

Bindings for libssh_ C library.

.. image:: https://coveralls.io/repos/github/Red-M/Redlibssh/badge.svg?branch=master
   :target: https://coveralls.io/github/Red-M/Redlibssh?branch=master
   :alt: Coverage
.. image:: https://readthedocs.org/projects/redlibssh/badge/?version=latest
   :target: http://redlibssh.readthedocs.org/en/latest/
   :alt: Latest documentation
.. image:: https://img.shields.io/pypi/v/redlibssh.svg
   :target: https://pypi.python.org/pypi/redlibssh
   :alt: Latest Version
.. image:: https://img.shields.io/pypi/wheel/redlibssh.svg
   :target: https://pypi.python.org/pypi/redlibssh
.. image:: https://img.shields.io/pypi/pyversions/redlibssh.svg
   :target: https://pypi.python.org/pypi/redlibssh
.. image:: https://img.shields.io/badge/License-LGPL%20v2-blue.svg
   :target: https://pypi.python.org/pypi/redlibssh
   :alt: License


Installation
_____________

Binary wheels are provided for Linux (manylinux 2010), OSX (10.14 and 10.15).

Wheels have *no dependencies*.

For building from source, see `documentation <https://redlibssh.readthedocs.io/en/latest/installation.html#building-from-source>`_.


.. code-block:: shell

   pip install redlibssh

Pip may need to be updated to be able to install binary wheels.

.. code-block:: shell

   pip install -U pip
   pip install redlibssh


Quick Start
_____________

See `command execution script <https://github.com/Red-M/redlibssh/blob/master/examples/exec.py>`_ for complete example.

Features
_________

The library uses `Cython`_ based native code extensions as wrappers to ``libssh``.

* Thread safe - GIL released as much as possible

  * libssh threading limitations apply - anything not supported in C is not supported in Python
* Very low overhead thin wrapper
* Object oriented

  * Memory freed automatically and safely as objects are garbage collected by Python
* Uses Python semantics where applicable

  * channel/file handle context manager support
  * channel/file handle iterator support
* Raises low level C errors as Python exceptions


.. _libssh: https://www.libssh.org
.. _Cython: https://www.cython.org
