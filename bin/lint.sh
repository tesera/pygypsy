#!/usr/bin/env sh

. venv/bin/activate
pylint -r y gypsy/ setup.py > report.txt
cat report.txt
