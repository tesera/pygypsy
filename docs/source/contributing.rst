Getting Started
~~~~~~~~~~~~~~~

Clone the repository

.. code:: bash

    git clone git@github.com:tesera/pygypsy.git
    cd pygypsy

Setup the commit hooks

.. code:: bash

    ln -s "$(pwd)/git-hooks/pre-commit.sh" .git/hooks/pre-commit

Development Process Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Fork the repository
-  Clone your fork to your development machine
-  Create a branch
-  Make a change: update code, update docs, update tests, and update README if
   appropriate)
-  Run the `tests <#tests>`__, `linter <#linting>`__, and
   `build <#cython-and-compiling-extensions>`__ the package
-  Submit a pull request against the dev branch of the upstream
   repository (the pull request will be against dev by default)
-  Select a peer reviewer and schedule a review
-  Conduct the review.
   - Please record as much as possible in the pull request using comments and review feature on github.
   - An outline of a good review procedure is given
   `here <http://blog.fogcreek.com/increase-defect-detection-with-our-code-review-checklist-example/>`__.
-  Revise pull request if necessary and continue reviewing-revising loop
   until reviewer(s) are satisfied.
-  Code is merged into dev branch

Releases will occur when enough new features or fixes have been merged
into the development branch. 'Enough' is at the discretion of the
mainters.

docker-compose
~~~~~~~~~~~~~~

Several development tasks are defined in ``docker-compose.yml``

Note - the base directory is mounted to a volume in the container -
/opt/pygypsy. This way you do not need to rebuild the image every time
you change a file or requirement.

Start the dev container and setup a venv

::

    docker-compose run dev
    virtualenv venv -p python2.7
    . venv/bin/activate
    pip install -e .[dev,test,lint,docs]

Then it is possible to use the docker-compose tasks

::

    docker-compose run test # run tests
    docker-compose run docs # build docs
    docker-compose run dev # run bash
    docker-compose run lint # run linter

Tests
~~~~~

Any functional changes or additions should be tested. Add a test for
your changes and update old tests, if required.

Run the tests as follows

::

    docker-compose run test

    # or, if set up with virtualenv outside of container
    py.test -s -v tests/

To save time, it is often convenient only to test the sections of the
code you are actively working. This can be done as follows

::

    docker-compose run test bash # only run this if you are using docker

    py.test -s -v tests/test_data_prep.py # test one file
    py.test -s -v tests/test_data_prep.py::test_prep_plottable # test one function

Linting
~~~~~~~

Linting checks the code for style and bugs.

Run the linter as follows

::

    docker-compose run lint

    # or, if set up with virtualenv outside of container
    bash bin/lint.sh

If you are familiar with pylint, you can use the ``pylint`` command
directly.

All new code should satisfy the linting standards!

Documentation
~~~~~~~~~~~~~

Documentation is built automatically from docstrings and hosted at |pygypsy docs| and administration is done at |read the docs|.

See http://www.sphinx-doc.org/en/stable/rest.html for the syntax

You can build the docs locally as follows:

::

    docker-compose run docs

    # or, if set up with virtualenv outside of container
    cd docs
    sphinx-apidoc -o ./source ../pygypsy
    make html
    make coverage

Commit hooks
~~~~~~~~~~~~

Commit hooks run automatically when committing to the repository for the
following quality control items:

-  debug breakpoints
-  linting

You have to symlink from the commit hooks provided to your local git
hooks directory as described in `Getting Started <#getting-started>`__:

You can override the commit hook by using the ``-n`` option when running
``git commit``. This is however discouraged!

Profiling
~~~~~~~~~

There are many strategies suitable for profiling.

A good initial strategy is to run ``cProfile`` on a script as follows:

::

    python -m cProfile -s cumtime  "$(which pygypsy)" simulate data/raw_plottable.csv.prepped > profile.txt

It is very easy to be misled by the profiler, cProfile has 2x overhead,
and there a multitude of possible solutions to performance issues from
internal optimizations to better use of library functions.

Do not attempt to optimize unless it is absolutely necessary, and
discuss your ideas with other developers before trying to implement
them.

Cython and Compiling Extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Cython <cython.readthedocs.io>`__ is used and aviable for use for
performance limiting areas of the code. Familiarize yourself with cython
before revising / adding code which uses cython.

The implication of cython use is that the modules written in cython must
be recompiled in order for changes in those modules to take effect (e.g.
before running tests). This can be done in either of the following ways:

::

    - `pip install -e .`
    - `python setup.py build_ext --inplace`

Ad-hoc analyses in ``notebooks/``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes it is useful to inlcude the results of ad-hoc analyses of
pygypsy's behaviour.

For this purpose, a directory called notebooks/ is available, where
jupyter notebooks can be saved.

If you would like to do an ad-hoc analyses, the procedure is as follows

1. File an issue describing the problem to be solved/reason for the
   analysis

2. Create a branch for your analysis using the following format

::

    <issue-number>-<desciption>

for example

::

    #32-address-testing-findings

2. Ensure the analysis ``extras`` are installed

``pip install -e .[analysis]``

If you are using docker remember to first enter the docker container
with ``docker-compose run dev``.

3. Start the jupyter notebook server

::

    docker-compose run --service-ports notebook # if using docker
    jupyter notebook --notebook-dir notebooks # if not using docker

4. Create a notebook using the same name as was used for the branch

5. Conduct the analysis & revise the source code as necessary

General guidelines
^^^^^^^^^^^^^^^^^^

Do not commit your data used in your analysis

Notebooks are /not/ a replacement for unit tests! It is required to make
suitable unit tests for the finding of an analysis before a pull request
associated with an analysis will be merged.

Environment variables in ``env/dev.env``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``env/dev.env`` file is not required for most developers. It is
required to deploy on PyPI, update coveralls, and to run the S3 tests.
PyPI and coveralls should never be used locall - they should only be
used from the continuous integration service. If you would like to run
the tests for data on S3, you can create a ``env/dev.env`` file in your
clone with the appropriate variables. Make sure not to commit it to the
repository!

::

    GYPSY_BUCKET=secrets
    AWS_ACCESS_KEY_ID=secrets
    AWS_SECRET_ACCESS_KEY=secrets
    AWS_REGION=secrets
    PYPI_USER=secrets
    PYPI_PASSWORD=secrets
    COVERALLS_REPO_TOKEN=secrets

Security Considerations
~~~~~~~~~~~~~~~~~~~~~~~

This repository is open - do not commit sensitive data if you do not
want it to become publicly accessible!

The project continuious integration service authenticates against AWS,
PyPI, and the coveralls service.

**Credentials for those services are limited to this project and they
are encrypted. However,they are available unencrypted in the continuous
integration environment; maintainers be warned!**

Release Process
~~~~~~~~~~~~~~~

-  Create a new branch - release-x.y.z from dev

   -  x.y.z is the version increment using `semantic
      versioning <http://semver.org/>`__, familiarize with semantic
      versioning before doing a release
   -  in short, x,y,z should be incrememnted for backwards incompatible
      public api changes, backwards compatible public api changes, and
      backwards compatible bug fixes

-  Make sure all issues tagged with the release's milestone are closed
   or moved to a future milestone
-  Make sure dependencies listed in setup.py are up to date, including
   their minimum versions
-  Make sure tests are passing
-  Update changelog with summary of changes since previous release

   -  the command below can be used to get a list of changes since the
      previous release; summarize and prepend
   - git log `git describe --tags --abbrev=0`..HEAD --oneline

-  Open pull request with target of master
-  When pull request is merged, create a release on github

   -  when this is done, a build will be released to PYPI via the CI
      service

-  Merge master back to dev
- In |read the docs|, activate and build the documentation for the release
- Publish the pygypsy release on `zenodo <https://zenodo.org/>`__ as described `here https://guides.github.com/activities/citable-code/>`__
- Once the new release is on PyPI, the `conda-forge feedstock
<https://github.com/conda-forge/pygypsy-feedstock>`__ conda-forge release
should be updated to build and deploy for conda. This can be done by bumping
the version in the `meta.yaml
<https://github.com/conda-forge/pygypsy-feedstock/blob/master/recipe/meta.yaml>`__
file. You will also need to update the sha256 for the package, which can be obtained from `pypi <https://pypi.org/project/pygypsy/#files>`__

.. |pygypsy docs| replace:: `pygypsy docs <https://pygypsy.readthedocs.io/en/latest>`__
.. |read the docs| replace:: `Read The Docs <http://readthedocs.org/>`__
