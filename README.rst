xrviz
=====

Visualization of xarray data using PyQt5.


*Note, that the repository is under current development!*

Installation
------------
If you use `anaconda`, you may first create an environment:

     conda create -n xrviz python=3.8
     conda activate xrviz

Navigate to the repository directory.

For development:

.. code-block:: bash
    pip install -e ".[complete]"

otherwise

.. code-block:: bash
    pip install ".[complete]"

To only install special functionality, e.g. only vtk support in addition to core dependencies, run:

.. code-block:: bash
    pip install (-e) ".[docs]"

Usage
-----
From the console:

.. code-block:: bash
        xrviz -f <path-to-netcdf-file>



