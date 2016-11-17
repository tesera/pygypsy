#!/usr/bin/env sh

. venv/bin/activate
pylint -r y gypsy/ setup.py
