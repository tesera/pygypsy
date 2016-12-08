run_lint(){
    PYLINT_RC_PATH="../.pylintrc"
    LINT_FILE='lint-output.txt'
    LINT_LIMIT=7.5
    echo "Running lint check using pylintrc ${PYLINT_RC_PATH}"
    git-pylint-commit-hook \
        --pylintrc "${PYLINT_RC_PATH}" \
        >"${LINT_FILE}" 2>&1
    success=$?

    if [ $success -ne 0 ]
    then
        echo "The linting pre-commit hook failed"
        echo "Linting scored less than ${LINT_LIMIT}/10 or an error occurred"
        echo
        echo "$(tail -n 5 "${LINT_FILE}")"
        echo
        echo "See ${LINT_FILE} for full report"
        echo
        exit 1
    fi
}

check_breakpoint(){
    FILES_PATTERN='\.py(\..+)?$'
    FORBIDDEN_PATTERN='^[^#].*pdb\.set_trace.*$'
    RESULTS=()
    echo "Checking for debugger breakpoints"

    if git rev-parse --verify HEAD >/dev/null 2>&1
    then
        against=HEAD
    else
        # Initial commit: diff against an empty tree object
        against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
    fi
    for FILE in $(git diff --cached --name-only $against |\
                         grep -E $FILES_PATTERN); do
        RESULT=$(grep --with-filename -n -e $FORBIDDEN_PATTERN $FILE)
        GREP_STATUS=$?
        if [[ $GREP_STATUS == 0 ]]; then
            RESULTS=("${RESULTS[@]}" "$RESULT")
        elif [[ $GREP_STATUS != 1 ]]; then
            echo "grep exited with code ${GREP_STATUS}."
        fi
    done

    if [[ $RESULTS ]]; then
        echo 'COMMIT REJECTED Found "pdb.set_trace()" references.'
        echo "${RESULTS}"
        exit 1
    fi
}
