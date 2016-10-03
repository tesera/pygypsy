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

### Linting

Linting checks the code for style and bugs.

Run the linter as follows

```
docker-compose run lint

# or, if set up with virtualenv outside of container
bash bin/lint.sh
```

If you are familiar with pylint, you can use the `pylint` command directly.

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

### Commit hooks

Commit hooks run automatically when committing to the repository.

You have to symlink from the commit hooks provided to your local git hooks directory as follows:

You can override the commit hook by using the `-n` option when running `git commit`. This is however discouraged!

```
# from the root gypsy directory
ln -s "$(pwd)/git-hooks/pre-commit.sh" .git/hooks/pre-commit
```
