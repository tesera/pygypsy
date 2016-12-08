Master: |Codeship Status for tesera/gypsy master| Dev: |Codeship Status for tesera/gypsy dev|

|Coverage Status| |Documentation Status| |PyPI License| |DOI|

**Conda-forge**

|Anaconda-Server Version| |Anaconda-Server Downloads|

Linux: |Circle CI| OSX: |TravisCI| Windows: |AppVeyor|

**PyPI**

|PyPI version| |PyPI Downloads| |PyPI Python Versions| |PyPI Format|

pygypsy
=======

pygypsy is a python implementation of the forest **Growth and Yield Projection
SYstem** [HuangEtAl2009]_.

Its main usage mode is a command line interface; it also has a an API for
programmatic use.

.. [HuangEtAl2009] Huang, Meng, Yang (2009). A Growth and Yield Projection System for Natural and Post-Harvest Stands in Alberta. Retrieved from http://www1.agric.gov.ab.ca/$department/deptdocs.nsf/all/formain15784/$file/GYPSY-Natural-PostHarvestStands-Alberta-May21-2009.pdf?OpenElement

Installation
------------

pygypsy is available in the following package repositories

1. PyPI

::

    pip install pygypsy

2. conda-forge

::

    conda config --add channels conda-forge
    conda install pygypsy

Conda is the recommended environment for using gypsy. Installation from
PyPI currently requires compilation of cython extensions and C code; on
Linux and OSX this is generally not problematic.

It is recommended to install in a
`virtualenv <https://virtualenv.pypa.io/en/stable/userguide/>`__ or
`conda env <http://conda.pydata.org/docs/using/envs.html>`__ to avoid
clobbering system or other projects' python pacakges.

Usage
-----

pygypsy provides a command line interface for convenient usage

The complete documentation can be accessed with ``pygypsy -h``:

::

    Usage: pygypsy [OPTIONS] COMMAND [ARGS]...

      Growth and Yield Projection System

      Note: 'prep' subcommand must be run before 'simulate'

      Options:
        -v, --verbose
        -o, --output-dir PATH
        -h, --help             Show this message and exit.

      Commands:
        generate_config  Generate a configuration file Generates a...
        plot             Create charts for all files in pygypsy...
        prep             Prepare stand data for use in pygpysy...
        simulate         Run pygypsy simulation

Documentation for subcommands is available via
``pygypsy SUBCOMMAND -h``:

Getting help
------------

If you are interesting in using or developing pygypsy and would like
assistance:

1. Check the |pygypsy docs|
2. Check the |pygypsy issue tracker|
3. Open a |new pygypsy issue|

Contributing
------------

If you would like to contribute to pygypsy, start by reviewing the `contributing guide <https://github.com/tesera/pygypsy/blob/dev/docs/source/contributing.rst>`__. If you need help getting started, see `Getting help`_.


.. |pygypsy issue tracker| replace:: `pygypsy issue tracker <https://github.com/tesera/pygypsy/issues>`__
.. |new pygypsy issue| replace:: `new pygypsy issue <https://github.com/tesera/pygypsy/issues/new>`__
.. |pygypsy docs| replace:: `pygypsy docs <https://pygypsy.readthedocs.io/en/latest>`__

.. |Codeship Status for tesera/gypsy master| image:: https://app.codeship.com/projects/79989040-748f-0134-c8fb-56e5180c42b3/status?branch=master
   :target: https://app.codeship.com/projects/179242
.. |Codeship Status for tesera/gypsy dev| image:: https://app.codeship.com/projects/79989040-748f-0134-c8fb-56e5180c42b3/status?branch=dev
   :target: https://app.codeship.com/projects/179242
.. |Coverage Status| image:: https://coveralls.io/repos/github/tesera/pygypsy/badge.svg?branch=dev
   :target: https://coveralls.io/github/tesera/pygypsy?branch=dev
.. |Documentation Status| image:: https://readthedocs.org/projects/pygypsy/badge/?version=latest
   :target: http://pygypsy.readthedocs.io/en/latest/?badge=latest
.. |PyPI License| image:: https://img.shields.io/pypi/l/pygypsy.svg
   :target: https://img.shields.io/pypi/l/pygypsy.svg
.. |Anaconda-Server Version| image:: https://anaconda.org/conda-forge/pygypsy/badges/version.svg
   :target: https://anaconda.org/conda-forge/pygypsy
.. |Anaconda-Server Downloads| image:: https://anaconda.org/conda-forge/pygypsy/badges/downloads.svg
   :target: https://anaconda.org/conda-forge/pygypsy
.. |Circle CI| image:: https://circleci.com/gh/conda-forge/pygypsy-feedstock.svg?style=shield
   :target: https://circleci.com/gh/conda-forge/pygypsy-feedstock
.. |TravisCI| image:: https://travis-ci.org/conda-forge/pygypsy-feedstock.svg?branch=master
   :target: https://travis-ci.org/conda-forge/pygypsy-feedstock
.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/github/conda-forge/pygypsy-feedstock?svg=True
   :target: https://ci.appveyor.com/project/conda-forge/pygypsy-feedstock/branch/master
.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/pygypsy.svg
   :target: https://img.shields.io/pypi/dm/pygypsy.svg
.. |PyPI version| image:: https://badge.fury.io/py/pygypsy.svg
   :target: https://badge.fury.io/py/pygypsy
.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/pygypsy.svg
   :target: https://img.shields.io/pypi/pyversions/pygypsy.svg
.. |PyPI Format| image:: https://img.shields.io/pypi/format/pygypsy.svg
   :target: https://img.shields.io/pypi/format/pygypsy.svg
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.197110.svg
   :target: https://doi.org/10.5281/zenodo.197110
