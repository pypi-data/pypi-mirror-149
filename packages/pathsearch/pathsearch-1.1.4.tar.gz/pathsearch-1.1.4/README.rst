.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/
    :alt: isort

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

.. image:: https://img.shields.io/pypi/v/pathsearch
    :target: https://pypi.org/project/pathsearch/
    :alt: pypi version

.. image:: https://img.shields.io/pypi/dm/pathsearch
    :target: https://pypi.org/project/pathsearch/
    :alt: downloads/monthly

.. image:: https://static.pepy.tech/badge/pathsearch
    :target: https://pypi.org/project/pathsearch/
    :alt: total downloads

.. image:: https://img.shields.io/pypi/pyversions/pathsearch
    :target: https://pypi.org/project/pathsearch/
    :alt: python versions

.. image:: https://img.shields.io/pypi/l/pathsearch
    :target: https://github.com/mrlegohead0x45/pathsearch/blob/main/LICENSE
    :alt: license

pathsearch
----------

A script to search for a file in a list of directories.

Install
=======

You can install this script from PyPi with your favorite package manager.
For example:
::
    
    pip install pathsearch
    poetry add pathsearch


Or you can install it from source:

.. code:: bash

    # clone the repository
    git clone https://github.com/mrlegohead0x45/pathsearch/
    # or if you have github cli
    gh repo clone mrlegohead0x45/pathsearch

    cd pathsearch
    
    # install the package
    pip install -e .
    # or you can just run it directly
    python pathsearch.py

Usage
=====

::

    $ pathsearch -h
    usage: pathsearch [-h] [-V] [-pe] [-v | -q] (-p PATH | -e VAR) file

    Search for a file in a list of directories

    positional arguments:
    file                  File to search for on the specified path

    options:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    -pe, --pathext        Look for file with extensions in environment variable PATHEXT (normally only set on Windows) (default: False)
    -v, --verbose         Be verbose
    -q, --quiet           Be quiet (only print found files)
    -p PATH, --path PATH  Literal path to look in (e.g. /usr/bin:/bin:/usr/sbin:/sbin)
    -e VAR, --env VAR     Environment variable to take path to search from (e.g. PATH or LD_LIBRARY_PATH)

    Copyright (c) 2022 mrlegohead0x45. Licensed under the MIT License, which can be found in the source code of this program, or online at https://opensource.org/licenses/MIT. This program can be found online at
    https://github.com/mrlegohead0x45/pathsearch and https://pypi.org/project/pathsearch/

You can specify a literal path to look in with the ``-p`` or ``--path`` option.
Or, you can specify an environment variable to take the path from with the ``-e`` or ``--env`` option.
The ``-pe`` or ``--pathext`` option is generally only useful on Windows,
and will look for files with extensions in the PATHEXT environment variable, for example,
``pathsearch -pe -e PATH cmd`` will look for ``cmd.exe``, ``cmd.bat``, ``cmd.com`` etc. in the path.
See `<https://superuser.com/questions/1027078/what-is-the-default-value-of-the-pathext-environment-variable-for-windows>`_ for more information.

License
=======

This project is licensed under the MIT license,
the text of which is available at https://opensource.org/licenses/MIT and in the `LICENSE file <LICENSE>`_.
