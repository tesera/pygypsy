#!/usr/bin/env bash


PYLINT_RC_PATH="../.pylintrc"

echo "Running pre-commit hook using ${PYLINT_RC_PATH}"

if [ -z "$VIRTUAL_ENV" ]; then
    CMD="docker-compose run pre-commit"
else
    CMD="git-pylint-commit-hook --pylintrc ${PYLINT_RC_PATH}"
fi
