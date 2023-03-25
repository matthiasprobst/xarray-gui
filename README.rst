xrgviz
======

XArray gui visualization is a visualization tool for xarray objects using PyQt5.


*Note, that the repository is under current development!*

Installation
------------
If you use `anaconda`, you may first create an environment:

::

     conda create -n xrgviz python=3.8
     conda activate xrgviz

Navigate to the repository directory.

For development:

::

    pip install -e ".[complete]"

otherwise

::

    pip install ".[complete]"

To only install special functionality, e.g. only vtk support in addition to core dependencies, run:

::

    pip install (-e) ".[docs]"

Usage
-----
From the console:

::

        xrgviz -f <path-to-netcdf-file>



