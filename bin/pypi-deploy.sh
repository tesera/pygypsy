# TODO: in future, instead of ignoring failures in pypi upload
# only build and upload if the latest tag is at HEAD
. venv/bin/activate

python setup.py sdist
# upload to pypi, ignoring failures
twine upload -u "${PYPI_USER}" -p "${PYPI_PASSWORD}" dist/*

