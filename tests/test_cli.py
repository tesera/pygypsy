import os
import shutil
from click.testing import CliRunner

from gypsy.scripts.cli import cli
from gypsy.scripts import DEFAULT_CONF_FILE

from conftest import DATA_DIR


def test_generate_config():
    runner = CliRunner()
    output_dir = 'gypsy-output'

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['--output-dir', output_dir, 'generate_config'])

        assert result.exit_code == 0
        assert os.path.exists('./gypsy-output/gypsy-config.json')


def test_prep():
    output_dir = 'gypsy-output'
    input_data_path = './raw_standtable.csv'
    expected_output_path = os.path.join(output_dir,
                                        'plot_table_prepped.csv')
    runner = CliRunner()

    with runner.isolated_filesystem():
        shutil.copy(
            os.path.join(DATA_DIR, 'raw_standtable.csv'),
            input_data_path
        )

        result = runner.invoke(cli, [
            '--output-dir', output_dir,
            'prep', input_data_path
        ])

        assert result.exit_code == 0
        assert os.path.exists(expected_output_path)

def test_valid_config():
    input_data_path = './raw_standtable.csv'
    runner = CliRunner()

    with runner.isolated_filesystem():
        shutil.copy(
            os.path.join(DATA_DIR, 'raw_standtable.csv'),
            input_data_path
        )

        result = runner.invoke(cli, [
            'prep',
            '--config-file', DEFAULT_CONF_FILE,
            input_data_path
        ])

        assert result.exit_code == 0


def test_invalid_config(invalid_cli_config_file):
    input_data_path = './raw_standtable.csv'
    runner = CliRunner()

    with runner.isolated_filesystem():
        shutil.copy(
            os.path.join(DATA_DIR, 'raw_standtable.csv'),
            input_data_path
        )

        result = runner.invoke(cli, [
            'prep',
            '--config-file', invalid_cli_config_file,
            input_data_path
        ])

        assert result.exit_code != 0

def test_schema_violating_config():
    input_data_path = './raw_standtable.csv'
    runner = CliRunner()

    with runner.isolated_filesystem():
        shutil.copy(os.path.join(DATA_DIR, 'raw_standtable.csv'),
                    input_data_path)
        shutil.copy(os.path.join(DATA_DIR, 'invalid-config.json'),
                    'config.json')

        result = runner.invoke(cli, [
            'prep',
            '--config-file', 'config.json',
            input_data_path
        ])

        assert result.exit_code != 0
        assert 'Invalid value for "--config-file"' in result.output


def test_simulate():
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
