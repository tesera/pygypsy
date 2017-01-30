. venv/bin/activate

python setup.py sdist

twine upload -u "${PYPI_USER}" -p "${PYPI_PASSWORD}" dist/pygypsy-`git tag | tail -n 1`.tar.gz
