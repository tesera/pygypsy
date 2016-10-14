# gypsy

TODO!

## Usage

Docker and (host machine) virtualenv installation are incompatible!

### Installation
#### Virtualenv
```
git clone git@github.com:tesera/gypsy.git
cd gypsy
virtualenv venv
. venv/bin/activate
pip install . # regular users
```

#### Docker

Build the gypsy image as follows

```
docker build -t gypsy .
```

That creates an isolated environment where gypsy can be run

Start a container using the gypsy image

```
docker run -t -i gypsy /bin/bash
. venv/bin/activate
```

Run gypsy in the container

```
root@de6cccb1a217:/opt/gypsy# gypsy 10
False
False
False
False
False
False
False
False
False
False
```

### CLI

Gypsy provides a command line interface for convenient usage

Prepared your standtable

```
gyspy prep your_stand_table.csv
```

Run the gypsy simulation

```
gyspy simulate your_stand_table.csv
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
    prep      Prepare stand table for use in GYPSY...
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
- Conduct the review. Please keep comments in the pull request.
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
pip install -e .[dev]
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
