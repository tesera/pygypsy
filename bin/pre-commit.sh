#!/usr/bin/env sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "${DIR}/pre-commit-functions.sh"

[ -z "$VIRTUAL_ENV" ] && [ hash docker-compose 2>/dev/null ]
USING_DOCKER=$?
if [ $USING_DOCKER ]
then
    . venv/bin/activate
fi

run_lint
check_breakpoint
