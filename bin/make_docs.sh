#!/usr/bin/env sh

. venv/bin/activate
cd docs
sphinx-apidoc -o ./source ../pygypsy
make html
