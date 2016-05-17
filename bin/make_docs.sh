#!/usr/bin/env sh

. venv/bin/activate
cd docs
sphinx-apidoc -o ./source ../gypsy
make html
