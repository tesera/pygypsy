import re
import pytest
from click.testing import CliRunner
import botocore

from pygypsy.scripts.cli import cli
from conftest import BUCKET

S3_BKT_PREFIX = 's3://%s/' % BUCKET
SKIP_IF_NO_S3 = pytest.mark.skipif(BUCKET is None,
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
    prefix = re.sub(r'^%s' % S3_BKT_PREFIX, '', s3_config_output_dir)
    expected_output_paths = [
        '%s/%s' % (prefix, f) \
        for f in ['pygypsy-config.json', 'generate-config.log']
    ]

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', s3_config_output_dir, 'generate_config'
        ])

        assert result.exit_code == 0
        assert all([
            s3_obj_exists(s3_bucket_conn, path) \
            for path in expected_output_paths
        ])


@SKIP_IF_NO_S3
def test_prep(s3_prep_output_dir, s3_bucket_conn):
    runner = CliRunner()
    prefix = re.sub(r'^%s' % S3_BKT_PREFIX, '', s3_prep_output_dir['out-dir'])
    expected_output_paths = [
        '%s/%s' % (prefix, f) \
        for f in ['plot_table_prepped.csv', 'prep.log']
    ]

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', s3_prep_output_dir['out-dir'],
            'prep', s3_prep_output_dir['data-path']
        ])

        assert result.exit_code == 0
        assert all([
            s3_obj_exists(s3_bucket_conn, path) \
            for path in expected_output_paths
        ])


@SKIP_IF_NO_S3
def test_simulate(s3_simulate_output_dir, s3_bucket_conn):
    runner = CliRunner()
    input_data_path = s3_simulate_output_dir['data-path']
    output_dir = s3_simulate_output_dir['out-dir']
    prefix = re.sub(r'^%s' % S3_BKT_PREFIX, '', output_dir)
    expected_files = [
        'simulation-data/1614424.csv',
        'simulation-data/1008174.csv',
        'simulate.log',
    ]
    expected_output_paths = [
        '%s/%s' %  (prefix, f) for f in expected_files
    ]

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', output_dir,
            'simulate', input_data_path
        ])

        assert result.exit_code == 0
        assert all([s3_obj_exists(s3_bucket_conn, i) for i in expected_output_paths])

@SKIP_IF_NO_S3
def test_simulate_log_present_if_err(s3_simulate_output_dir, s3_bucket_conn):
    input_data_path = s3_simulate_output_dir['prepped-data-path']
    output_dir = s3_simulate_output_dir['out-dir']
    prefix = re.sub(r'^%s' % S3_BKT_PREFIX, '', output_dir)
    expected_files = [
        'simulate.log',
    ]
    expected_output_paths = [
        '%s/%s' % (prefix, f) for f in expected_files
    ]

    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            '--output-dir', output_dir,
            'simulate', input_data_path
        ])

        assert result.exit_code != 0
        assert all([s3_obj_exists(s3_bucket_conn, i) for i in expected_output_paths])
