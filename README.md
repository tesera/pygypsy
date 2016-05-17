# gypsy

TODO!

## Installation

Docker and (host machine) virtualenv installation are incompatible!

### Virtualenv
```
git clone git@github.com:tesera/gypsy.git
cd gypsy
virtualenv venv
. venv/bin/activate
pip install . # regular users
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
### dev.env

A file, `dev.env` is required for some tasks

It should have the following

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
GITHUB_TOKEN=
```

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
py.test tests/
```

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
