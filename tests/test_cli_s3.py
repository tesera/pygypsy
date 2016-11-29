import os

import pytest
from click.testing import CliRunner
import botocore

from gypsy.scripts.cli import cli


SKIP_IF_NO_S3 = pytest.mark.skipif(os.getenv('GYPSY_BUCKET') is None,
                                   reason="S3 tests are not configured locally")


def s3_obj_exists(bucket_conn, key):
    try:
        bucket_conn.Object(key).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            raise
    else:
        exists = True

    return exists


@SKIP_IF_NO_S3
def test_generate_config(s3_config_output_dir, s3_bucket_conn):
    runner = CliRunner()
    expected_output_path = '%s/%s' % (s3_config_output_dir, 'gypsy-config.json')
    expected_output_path = expected_output_path.lstrip('s3://hris-gypsy/')

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', s3_config_output_dir, 'generate_config'
        ])

        assert result.exit_code == 0
        assert s3_obj_exists(s3_bucket_conn, expected_output_path)

@SKIP_IF_NO_S3
def test_prep(s3_prep_output_dir, s3_bucket_conn):
    runner = CliRunner()
    expected_output_path = os.path.join(s3_prep_output_dir['out-dir'],
                                        'plot_table_prepped.csv')
    expected_output_path = expected_output_path.lstrip('s3://hris-gypsy/')

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', s3_prep_output_dir['out-dir'],
            'prep', s3_prep_output_dir['data-path']
        ])

        assert result.exit_code == 0
        assert s3_obj_exists(s3_bucket_conn, expected_output_path)


@SKIP_IF_NO_S3
def test_simulate(s3_simulate_output_dir, s3_bucket_conn):
    input_data_path = s3_simulate_output_dir['data-path']
    output_dir = s3_simulate_output_dir['out-dir']
    expected_files = [
        'simulation-data/1614424.csv',
        'simulation-data/1008174.csv',
    ]
    expected_output_paths = [
        '%s/%s' %(output_dir.lstrip('s3://hris-gypsy/'), f) \
        for f in expected_files
    ]

    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', output_dir,
            'simulate', input_data_path
        ])

        assert result.exit_code == 0
        assert all([s3_obj_exists(s3_bucket_conn, i) for i in expected_output_paths])
