# gypsy

TODO! - JS

## Installation

The package should be installed using docker or virtualenv.

If you will be contributing to the code, please carefully review the
"Development" further below in this README.

Docker and (host machine) virtualenv installation are incompatible! Packages
installed in a docker virtualenvironment will probably not be compatible with
your local system, and vice versa.

### Virtualenv
```
git clone git@github.com:tesera/gypsy.git
cd gypsy
virtualenv venv
. venv/bin/activate
pip install -e . # regular users
```

### Docker

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

## Development
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

### Code Linting

A linter [linter](https://en.wikipedia.org/wiki/Lint_%28software%29) is a
program that checks code for errors. They have many [benefits](https://raygun.com/blog/2015/07/using-linters-for-faster-safer-coding-with-less-javascript-errors/).

Linting is an effective way to improve code quality with little expenditure of
effort on behalf of the developer.

Make sure your contributions to gypsy meet common python conventions. This is
enforced with a 'pre-commit hook'. When you commit, pylint will run and check
that style is followed before you commit. If it does not pass linting, the
commit will be rejected. Familiarize with pylint
[here](https://www.pylint.org/).

For the pylint commit hook to run successfully, you will have to make sure some
packages are installed and that the hook is in the git hooks directory as shown
below:

Install pylint and git-pylint-commit hooks globally

    pip install pylint
    pip install git-pylint-commit-hook==2.0.7

Link the commit hook to where git expects it

    ln -s "${PWD}/hooks/pre-commit.sh .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit


### Documentation

Documentation is build automatically from docstrings

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
