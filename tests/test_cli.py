import os
import shutil
from click.testing import CliRunner

from gypsy.scripts.cli import cli

from conftest import DATA_DIR


def remove_path_if_exists(*paths): #pylint: disable=missing-docstring
    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except OSError:
            pass


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

def test_simulate():
    output_dir = 'gypsy-output'
    input_data_path = './data.csv'
    expected_files = ['1614424.csv', '1008174.csv']
    expected_output_paths = [
        os.path.join(output_dir, 'simulation-data', item) \
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
