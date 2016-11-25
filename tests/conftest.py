import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


@pytest.yield_fixture(scope='module')
def invalid_cli_config_file():
    path = os.path.join(DATA_DIR, 'invalid_cli_config.txt')

    with open(path, 'w') as f:
        f.write('\n\n\n\nnodata\n')

    yield path

    os.remove(path)
