import os
import shutil

import pytest
from click.testing import CliRunner
import botocore

from gypsy.scripts.cli import cli
from conftest import DATA_DIR


def assert_s3_obj_exists(bucket_conn, key):
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


@pytest.mark.skipif(os.getenv('GYPSY_BUCKET') is None,
                    reason="S3 tests are not configured locally")
def test_generate_config(s3_config_output_dir, s3_bucket_conn):
    runner = CliRunner()
    expected_output_path = '%s/%s' % (s3_config_output_dir, 'gypsy-config.json')

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', s3_config_output_dir, 'generate_config'
        ])

        assert result.exit_code == 0
        assert_s3_obj_exists(s3_bucket_conn, expected_output_path)


@pytest.mark.skipif(os.getenv('GYPSY_BUCKET') is None,
                    reason="S3 tests are not configured locally")
def test_prep(s3_prep_output_dir, s3_bucket_conn):
    expected_output_path = os.path.join(s3_prep_output_dir['out-dir'],
                                        'plot_table_prepped.csv')
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', s3_prep_output_dir['out-dir'],
            'prep', s3_prep_output_dir['data-path']
        ])
        import ipdb; ipdb.set_trace()

        assert result.exit_code == 0
        assert_s3_obj_exists(s3_bucket_conn, expected_output_path)


@pytest.mark.skipif(os.getenv('GYPSY_BUCKET') is None,
                    reason="S3 tests are not configured locally")
def test_simulate(s3_simulate_output_dir, s3_bucket_conn):
    output_dir = 'gypsy-output'
    input_data_path = './data.csv'
    expected_files = [
        os.path.join('simulation-data', '1614424.csv'),
        os.path.join('simulation-data', '1008174.csv'),
        'gypsy.log'
    ]
    expected_output_paths = [
        os.path.join(output_dir, item) \
        for item in expected_files
    ]

    runner = CliRunner()

    with runner.isolated_filesystem():
        shutil.copy(
            os.path.join(DATA_DIR, 'raw_standtable_prepped.csv'),
            input_data_path
        )

        result = runner.invoke(cli, [
            '--output-dir', output_dir,
            'simulate', input_data_path
        ])

        assert result.exit_code == 0
        assert all([os.path.exists(i) for i in expected_output_paths])
