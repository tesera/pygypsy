#!/usr/bin/env sh

. venv/bin/activate
pylint -r y pygypsy/ setup.py > report.txt
cat report.txt
