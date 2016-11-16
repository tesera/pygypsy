[![Codeship Status for tesera/gypsy](https://app.codeship.com/projects/79989040-748f-0134-c8fb-56e5180c42b3/status?branch=master)](https://app.codeship.com/projects/179242)

# GYPSY

GYPSY is a Growth and Yield Projection SYstem for trees.

## Usage

### Installation

There are two supported options for installation of GYPSY:

1. installation with pip inside of a [virtualenv](#virtualenv)
2. use of a GYPSY [docker](#docker) image

If an option you are familiar with is missing, please search for it in the
issue tracker; if it is not there add a new issue if your preferred option.

#### Quick Start

You can get started right away by installing GYPSY as follows:

```
pip install git+ssh://git@github.com/tesera/gypsy.git@dev # if you have ssh setup with github
pip install git+https://github.com/tesera/gypsy.git@dev # if you don't have ssh setup with github
```

However, maintainers may not be able to provide support for issues encountered
using this method of installation as it does not isolate GYPSY from other
python packages on the system.

#### Virtualenv

Virtual environments protect system-wide python packages from being clobbered
by user packages and their dependencies, and vice versa. They also enable
python projects on the same machine to easily use python2 **or** python3.

If you are not familiar with virtualenv, see the
[installation](https://virtualenv.pypa.io/en/stable/installation/) and
[user guide](https://virtualenv.pypa.io/en/stable/userguide/) to get started.

Once you have virtualenv installed on your system, create a project directory
and virtualenv for your work with GYPSY.

```
mkdir gypsy-project && cd gypsy-project
virtualenv venv
. venv/bin/activate
```

Now you can install gypsy. Note the `@dev` tag at the end - this installs the
latest development version. To install the latest stable release, leave `@dev`
out.

```
pip install git+ssh://git@github.com/tesera/gypsy.git@dev # if you have ssh setup with github
pip install git+https://github.com/tesera/gypsy.git@dev # if you don't have ssh setup with github
```

Once the installation is finished, test that GYPSY runs inside the virtualenv.

```
gypsy --help
```

The first run will be slow as matplotlib builds a font cache. Subsequent runs are faster.

#### Docker

Presently, GYPSY is not hosted on a docker image repository, so you will first
have to clone this repository

```
git clone git@github.com:tesera/gypsy.git
```

Then enter the cloned directory and build the GYPSY image as follows:

```
cd gypsy
docker build -t gypsy .
```

Start a container using the GYPSY image and activate the virtual environment
inside the container as follows:

```
docker run -t gypsy -v /path/to/your/data/dir:/data -i /bin/bash
. venv/bin/activate
```

That starts an isolated environment where GYPSY can be run. Note the `-v
path/to/your/data/dir:/data`, which makes the folder `/path/to/your/data/dir`
available in the docker image at the `/data` directory. This is required to run
gypsy in the container on data that you have on your local computer (the docker
host). The paths should be absolute, not relative.

Finally, test that GYPSY runs in the container:

```
root@de6cccb1a217:/opt/gypsy# gypsy --help
```

The first run will be slow as matplotlib builds a font cache. Subsequent runs are faster.

### CLI

Gypsy provides a command line interface for convenient usage

Prepared your stand data:

```
gyspy prep your_stand_data.csv
```

Run GYPSY on the prepped data from the `gypsy prep` command:

```
gyspy simulate your_stand_data.csv.prepped
```

The complete documentation can be accessed with `gypsy -h`, documentation for
subcommands is available via `gypsy SUBCOMMAND -h`:


```
Usage: gypsy [OPTIONS] COMMAND [ARGS]...

  Growth and Yield Projection System

  Data prep must be run before simulating

  Options:
    -v, --verbose
    -h, --help     Show this message and exit.

  Commands:
    prep      Prepare stand data for use in GYPSY...
    simulate  Run GYPSY simulation
```
## Development
### Getting Started

Clone the repository

``` bash
git clone git@github.com:tesera/gypsy.git
cd gypsy
```

Setup the commit hooks

``` bash
ln -s "$(pwd)/git-hooks/pre-commit.sh" .git/hooks/pre-commit
```
### Development Process Overview

- Fork the repository
- Create a branch in your fork
- Make a change: update code (and docs, tests, and README if appropriate)
  - or update tests
  - or update and build docs
  - or update README
- Submit a pull request against the dev branch of the upstream repository
- Select a peer reviewer and schedule a review
- Conduct the review. Please keep comments in the pull request. An outline of a good review procedure is given [here](http://blog.fogcreek.com/increase-defect-detection-with-our-code-review-checklist-example/).
- Revise pull request if necessary and continue reviewing-revising loop until
  reviewer(s) are satisfied.
- Code is merged into dev branch

Releases will occur when enough new features or fixes have been merged into the
development branch. 'Enough' is at the discretion of the mainters.

### docker-compose

Several development tasks are defined in `docker-compose.yml`

Note - the base directory is mounted to a volume in the container -
/opt/gypsy. This way you do not need to rebuild the image every time you
change a file or requirement.

Start the dev container and setup a venv; the venv will be persisted to your
local storage but will probably not run on your system!

```
docker-compose run dev
virtualenv venv -p python2.7
. venv/bin/activate
pip install -e .[dev,test,lint,docs]
```

Then it is possible to use the docker-compose tasks

```
docker-compose run test # run tests
docker-compose run docs # build docs
docker-compose run dev # run bash
docker-compose run lint # run linter
```

### Tests

Any functional changes or additions should be tested. Add a test for your
changes and update old tests, if required.

Run the tests as follows

```
docker-compose run test

# or, if set up with virtualenv outside of container
py.test -s -v tests/
```

To save time, it is often convenient only to test the sections of the code you
are actively working. This can be done as follows

```
docker-compose run test bash # only run this if you are using docker

py.test -s -v tests/test_data_prep.py # test one file
py.test -s -v tests/test_data_prep.py::test_prep_standtable # test one function
```

### Linting

Linting checks the code for style and bugs.

Run the linter as follows

```
docker-compose run lint

# or, if set up with virtualenv outside of container
bash bin/lint.sh
```

If you are familiar with pylint, you can use the `pylint` command directly.

All new code must satisfy the linting standards.

### Documentation

Documentation is built automatically from docstrings

See http://www.sphinx-doc.org/en/stable/rest.html for the syntax

If you change function arguments, or the docstrings are otherwise updated, you
should rebuild the docs as follows:

```
docker-compose run docs

# or, if set up with virtualenv outside of container
cd docs
sphinx-apidoc -o ./source ../gypsy
make html
make coverage
```

### Commit hooks

Commit hooks run automatically when committing to the repository for the following quality control items:

- debug breakpoints
- linting

Once the test suite has been sped it, it will also be run as a pre-commit hook.

You have to symlink from the commit hooks provided to your local git hooks directory as described in [Getting Started](#getting-started):

You can override the commit hook by using the `-n` option when running `git commit`. This is however discouraged!

### Profiling

There are many strategies suitable for profiling.

A good initial strategy is to run `cProfile` on a script as follows:

    python -m cProfile -s cumtime  "$(which gypsy)" simulate data/raw_standtable.csv.prepped > profile.txt

It is very easy to be misled by the profiler, cProfile has 2x overhead, and
there a multitude of possible solutions to performance issues from internal
optimizations to better use of library functions.

Do not attempt to optimize unless it is absolutely necessary, and discuss your
ideas with other developers before trying to implement them.

### Cython

[Cython](cython.readthedocs.io) is used and aviable for use for performance
limiting areas of the code. Familiarize yourself with cython before revising /
adding code which uses cython.

The implication of cython use is that the modules written in cython must be
recompiled in order for changes in those modules to take effect (e.g. before
running tests). This can be done in either of the following ways:

    - `pip install -e .`
    - `python setup.py build_ext --inplace`

### Ad-hoc analyses in `notebooks/`

Sometimes it is useful to inlcude the results of ad-hoc analyses of gypsy's
behaviour.

For this purpose, a directory called notebooks/ is available, where jupyter
notebooks can be saved.

If you would like to do an ad-hoc analyses, the procedure is as follows

1. File an issue describing the problem to be solved/reason for the analysis

2. Create a branch for your analysis using the following format

```
<issue-number>-<desciption>
```

for example

```
#32-address-testing-findings
```

2. Ensure the analysis `extras` are installed

`pip install -e .[analysis]`

If you are using docker remember to first enter the docker container with
`docker-compose run dev`.

3. Start the jupyter notebook server

```
docker-compose run --service-ports notebook # if using docker
jupyter notebook --notebook-dir notebooks # if not using docker
```

4. Create a notebook using the same name as was used for the branch


5. Conduct the analysis & revise the source code as necessary


#### General guidelines

Do note commit your data used in your analysis

Notebooks are /not/ a replacement for unit tests! It is required to make suitable unit tests for the finding of an analysis before a pull request associated with an analysis will be merged.
