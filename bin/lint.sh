#!/usr/bin/env sh

. venv/bin/activate
pylint -r y gypsy/ tests/ setup.py
