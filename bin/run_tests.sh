#!/usr/bin/env sh

. venv/bin/activate
py.test -v --durations 5 --cache-clear tests/

