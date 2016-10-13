#!/usr/bin/env sh

. venv/bin/activate
py.test -v --cov gypsy --durations 5 --cache-clear tests/

