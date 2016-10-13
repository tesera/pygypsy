#!/usr/bin/env sh

PYLINT_RC_PATH="../.pylintrc"
[ -z "$VIRTUAL_ENV" ] && [ hash docker-compose 2>/dev/null ]
USING_DOCKER=$?

if [ $USING_DOCKER ]
then
    . venv/bin/activate
fi

git-pylint-commit-hook --pylintrc ${PYLINT_RC_PATH}
