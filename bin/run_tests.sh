#!/usr/bin/env sh

. venv/bin/activate
py.test -v --cov pygypsy --durations 5 --cache-clear tests/

