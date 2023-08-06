============
Installation
============

GBprocesS runs under Linux operating systems. Installation of GBprocesS requires a working version of Python 3.7 or older.

Via Git
-------
Currently, there are two supported ways to download GBprocesS from Gitlab.  
The first and easiest way is to clone the git repository::

    git clone git@gitlab.com:dschaumont/gbprocess.git

The second is to download an archive::

    wget https://gitlab.com/dschaumont/GBprocesS/-/archive/2.3/GBprocesS-2.3.tar.gz
    tar -xvf GBprocesS-2.3.tar.gz
    mv GBprocesS-2.3 gbprocess

Afterwards, the package can be installed using the latest version of ``pip``::
    
    cd gbprocess
    pip install --upgrade pip
    pip install --user .

This will install the GBprocesS in ``$HOME/.local/bin``. 
If an already exisiting installation is present, add the ``--upgrade`` parameter
to install a newer version.

To install at another location, a virtual environment can be used::

    python3 -m venv .venv
    source .venv/bin/activate
    cd gbprocess
    pip install --upgrade pip
    pip install .

A new folder ``.venv`` will be created in the current working directory,
and GBprocesS will be installed at that location. Please note that you 
will need to activate the virtual environment again when you start a new 
session using the ``source .venv/bin/activate`` command in the gbprocess directory.

After the installation, test if the program is correctly installed by using::

    gbprocess --help

Exit the virtual environment with::

    deactivate
