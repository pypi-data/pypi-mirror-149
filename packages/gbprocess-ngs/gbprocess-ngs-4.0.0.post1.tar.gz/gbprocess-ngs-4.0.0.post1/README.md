# Gbprocess

## Description

GBprocesS allows for the extraction of genomic inserts from NGS data for GBS experiments. 
Preprocessing is performed in different stages that are part of a linear pipeline where the steps are performed in order. 
GBprocesS provides a flexible way to adjust the functionality to your needs, as the operations required and the execution order vary depending on the GBS protocol used.

## Documentation

An extensive manual of the GBprocesS package can be found on [Read the Docs](https://gbprocess.readthedocs.io/en/latest/) including detailed explanations and illustrations.

## Citation

If you use GBprocesS, please cite 
"Schaumont, D. (2020) GBprocesS: Genotyping-by-Sequencing Data Processing Toolkit [Online]. Available online at https://gitlab.com/dschaumont/GBprocesS"

## Installation

GBprocesS is being developed and tested on Linux. 
Additionally, some dependencies are only developped on Linux. 


### From pypi
The package can be installed using the latest version of ``pip3``:
    
    pip install --user gbprocess-ngs

This will install GBprocesS in ``$HOME/.local/bin``. 
To install at another location, a virtual environment can be used::

    python3 -m venv .venv
    source .venv/bin/activate
    pip install gbprocess-ngs

### Via Git

Currently, there are two supported ways to download GBprocesS from Git. 
The first and easiest way is to clone the git repository:

    git clone git@gitlab.com:dschaumont/gbprocess.git

The second is to download an archive:

    wget https://gitlab.com/ilvo/GBprocesS/-/archive/2.0.2/GBprocesS-2.0.2.tar.gz
    tar -xvf GBprocesS-2.0.2.tar.gz
    mv GBprocesS-2.0.2 gbprocess

Afterwards, the package can be installed using the latest version of ``pip3``::
    
    cd gbprocess
    pip3 install --user .

This will install GBprocesS in ``$HOME/.local/bin``. 
If an already existing installation is present, add the ``--upgrade`` parameter to install a newer version.

To install at another location, a virtual environment can be used::

    python3 -m venv .venv
    source .venv/bin/activate
    cd gbprocess
    pip install .

A new folder ``.venv`` will be created in the current working directory,
and GBprocesS will be installed at that location. Please note that you will need to activate the virtual environment again when you start a new session using the ``source`` command above.

After the installation, test if the program is correctly installed by using::

    gbprocess --help
