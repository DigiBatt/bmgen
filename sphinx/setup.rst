Setup
=====

Installation
------------

A working installation of Python >= 3.10 and pip is required. The web version also requires npm.
The source code of the project can be found in its `GitLab repository <https://git.isea.rwth-aachen.de/ESS/testing/bmgen>`__.
The required dependencies and the package itself can be installed using pip:

.. code-block:: bash

    git clone git@git.isea.rwth-aachen.de:ESS/testing/bmgen.git
    cd bmgen
    pip install -r requirements.txt
    pip install -e .
    
To build the necessary node modules for the web version, the provided install script can be used:

.. code-block:: bash

    ./install.sh

Configuration
-------------

Configuration parameters can be provided in a JSON file.
Bdat will try to read the configuration from the following locations, from top to bottom:

- The path that is passed using the -c / --config option, if it is specified.
- ./config.json
- ~/.config/bdat/config.json

The config file contains information about the database(s) that bdat interacts with.
An example config looks like this:

.. code-block:: json

    {
        "databases": {
            "kadi": {
                "type": "kadi",
                "url": "https://cadi.isea.rwth-aachen.de",
                "token": "pat_xxxxxxxxxxxxx"
            }
        }
    }
