Setup
=====

The Python package is available on [PyPI](https://pypi.org/project/bm-generator/) and can be installed using pip:

    pip install bm-generator

The web version of the program can be started using the command:

    bmgen-server

Installation from sources
-------------------------

The required dependencies and the package itself can also be installed from the sources using pip:

    pip install -r requirements.txt
    pip install -e .

A working installation of Python >= 3.10 and pip is required. The web version also requires npm.
To build the modules for the web version and the documentation, the provided build script can be used:

    ./build.sh