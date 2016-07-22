#!/bin/bash
#
# An example hook script to verify what is about to be committed.
# Called by "git commit" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message if
# it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-commit".

if git rev-parse --verify HEAD >/dev/null 2>&1
then
	against=HEAD
else
	# Initial commit: diff against an empty tree object
	against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

FILES_PATTERN='\.py(\..+)?$'

FORBIDDEN_PATTERN='^[^#].*pdb\.set_trace.*$'

RESULTS=()

for FILE in $(git diff --cached --name-only $against | grep -E $FILES_PATTERN); do
    RESULT=$(grep --with-filename -n -e $FORBIDDEN_PATTERN $FILE)
    GREP_STATUS=$?
    if [[ $GREP_STATUS == 0 ]]; then
        RESULTS=("${RESULTS[@]}" "$RESULT")
    elif [[ $GREP_STATUS != 1 ]]; then
        echo "pre-commit hook failed. grep exited with code ${GREP_STATUS}."
    fi
done

if [[ $RESULTS ]]; then
    echo 'COMMIT REJECTED Found "pdb.set_trace()" references.'
    echo $RESULTS
    exit 1
fi

# Linting
git-pylint-commit-hook
