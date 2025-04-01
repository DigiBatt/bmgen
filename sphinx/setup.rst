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