#!/usr/bin/env bash

[ -z "$VIRTUAL_ENV" ] && hash docker-compose 2>/dev/null
USING_DOCKER=$?

echo "Running pre-commit hook"

if [ $USING_DOCKER -eq 0 ]; then
    echo "Assuming you are using docker"
    docker-compose run pre-commit
else
    bash bin/pre-commit.sh
fi
