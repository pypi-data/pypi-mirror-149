========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/Plotting_funcs/badge/?style=flat
    :target: https://Plotting_funcs.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/nnanos/Plotting_funcs.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/nnanos/Plotting_funcs

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/nnanos/Plotting_funcs?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/nnanos/Plotting_funcs

.. |requires| image:: https://requires.io/github/nnanos/Plotting_funcs/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/nnanos/Plotting_funcs/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/nnanos/Plotting_funcs/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/nnanos/Plotting_funcs

.. |version| image:: https://img.shields.io/pypi/v/Plotting-funcs.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/Plotting-funcs

.. |wheel| image:: https://img.shields.io/pypi/wheel/Plotting-funcs.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/Plotting-funcs

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/Plotting-funcs.svg
    :alt: Supported versions
    :target: https://pypi.org/project/Plotting-funcs

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/Plotting-funcs.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/Plotting-funcs

.. |commits-since| image:: https://img.shields.io/github/commits-since/nnanos/Plotting_funcs/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/nnanos/Plotting_funcs/compare/v0.0.0...master



.. end-badges

Auxiliary functions for plotting purposes mainly.

* Free software: MIT license

Installation
============

::

    pip install Plotting-funcs

You can also install the in-development version with::

    pip install https://github.com/nnanos/Plotting_funcs/archive/master.zip


Documentation
=============


https://Plotting_funcs.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
