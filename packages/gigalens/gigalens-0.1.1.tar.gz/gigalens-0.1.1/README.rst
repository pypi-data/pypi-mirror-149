GIGA-Lens
========================

.. image:: https://img.shields.io/pypi/v/gigalens.svg
    :target: https://pypi.python.org/pypi/gigalens
    :alt: Latest PyPI version

Gradient Informed, GPU Accelerated Lens modelling (GIGA-Lens) is a package for fast Bayesian inference on strong
gravitational lenses. For details, please see `our paper <https://arxiv.org/abs/2202.07663>`__.

Usage
-----

Installation
------------
``GIGA-Lens`` can be installed via pip: ::

    pip install gigalens

Tests can be run simply by running ``tox`` in the root directory.

Requirements
^^^^^^^^^^^^
::

    tensorflow>=2.6.0
    tensorflow-probability>=0.15.0
    lenstronomy==1.9.3
    scikit-image==0.18.2
    tqdm==4.62.0

The following dependencies are required by ``lenstronomy``:

::

    cosmohammer==0.6.1
    schwimmbad==0.3.2
    dynesty==1.1
    corner==2.2.1
    mpmath==1.2.1

Authors
-------

`GIGALens` was written by `Andi Gu <andi.gu@berkeley.edu>`_.
