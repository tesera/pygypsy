#!/usr/bin/env bash

[ -z "$VIRTUAL_ENV" ] && hash docker-compose 2>/dev/null
USING_DOCKER=$?

echo "Running pre-commit hook using ${PYLINT_RC_PATH}"
echo "Using docker test had exit code ${USING_DOCKER}"


if [ $USING_DOCKER -eq 0 ]; then
    docker-compose run pre-commit
else
    bash bin/pre-commit.sh
fi
