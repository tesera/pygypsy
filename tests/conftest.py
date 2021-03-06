#pylint: disable=redefined-outer-name,missing-docstring
import os
import pytest
import boto3

from pygypsy.scripts import DEFAULT_CONF_FILE
from pygypsy.utils import _copy_file


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
BUCKET = os.getenv('GYPSY_BUCKET')

@pytest.yield_fixture(scope='module')
def invalid_cli_config_file():
    path = os.path.join(DATA_DIR, 'invalid_cli_config.txt')

    with open(path, 'w') as f:
        f.write('\n\n\n\nnodata\n')

    yield path

    os.remove(path)

@pytest.fixture(scope='session')
def s3_bucket_path():
    if BUCKET is None:
        return

    return 's3://' + BUCKET

@pytest.fixture(scope='function')
def s3_bucket_conn():
    if BUCKET is None:
        return

    s3 = boto3.resource('s3')
    bucket_conn = s3.Bucket(BUCKET)

    return bucket_conn

@pytest.yield_fixture(scope='function')
def s3_config_output_dir(s3_bucket_path, s3_bucket_conn):
    if BUCKET is None:
        return

    prefix = 'test/generate-config/pygypsy-output'
    out_dir = '%s/%s' % (s3_bucket_path, prefix)

    yield out_dir

    for key in s3_bucket_conn.objects.filter(Prefix=prefix):
        key.delete()

@pytest.yield_fixture(scope='function')
def s3_prep_output_dir(s3_bucket_path, s3_bucket_conn):
    if BUCKET is None:
        val = None
    else:
        prefix = 'test/prep/pygypsy-output'
        out_dir = '%s/%s' % (s3_bucket_path, prefix)
        files = [
            (os.path.join(DATA_DIR, 'raw_standtable.csv'),
             '/'.join([prefix, 'raw-data.csv'])),
            (DEFAULT_CONF_FILE,
             '/'.join([prefix, 'config.json'])),
        ]

        for item in files:
            _copy_file(item[0], item[1], bucket_conn=s3_bucket_conn)
            data_path = '/'.join([s3_bucket_path, files[0][1]])

            val = {
                'out-dir': out_dir,
                'data-path': data_path
            }

    yield val

    for key in s3_bucket_conn.objects.filter(Prefix=prefix):
        key.delete()

@pytest.yield_fixture(scope='function')
def s3_simulate_output_dir(s3_bucket_path, s3_bucket_conn):
    if BUCKET is None:
        yield
        return

    prefix = 'test/simulate/pygypsy-output'
    out_dir = '%s/%s' % (s3_bucket_path, prefix)
    files = [
        (os.path.join(DATA_DIR, 'raw_standtable_prepped.csv'),
         '/'.join([prefix, 'raw-data-prepped.csv'])),
        (os.path.join(DATA_DIR, 'raw_standtable.csv'),
         '/'.join([prefix, 'raw-data.csv'])),
        (DEFAULT_CONF_FILE,
         '/'.join([prefix, 'config.json'])),
    ]

    for item in files:
        _copy_file(item[0], item[1], bucket_conn=s3_bucket_conn)

    data_path = '/'.join([s3_bucket_path, files[0][1]])
    prepped_data_path = '/'.join([s3_bucket_path, files[1][1]])

    yield {
        'out-dir': out_dir,
        'data-path': data_path,
        'prepped-data-path': prepped_data_path,
    }

    for key in s3_bucket_conn.objects.filter(Prefix=prefix):
        key.delete()

@pytest.yield_fixture(scope='function')
def config_on_s3(s3_bucket_path, s3_bucket_conn):
    if BUCKET is None:
        yield
        return

    prefix = 'test/_load_and_validate_config/pygypsy-ouptput'
    files = [
        (DEFAULT_CONF_FILE,
         '/'.join([prefix, 'config.json'])),
    ]

    for item in files:
        _copy_file(item[0], item[1], bucket_conn=s3_bucket_conn)

    config_path = '/'.join([s3_bucket_path, files[0][1]])

    yield config_path

    for key in s3_bucket_conn.objects.filter(Prefix=prefix):
        key.delete()
