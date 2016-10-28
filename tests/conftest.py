import os
import pytest


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


@pytest.fixture(scope='module')
def cli_config_file():
    path = os.path.join(DATA_DIR, 'cli_config.txt')

    with open(path, 'w') as f:
        f.write('key=value')

    yield path

    os.remove(path)
