import os
import shutil
from click.testing import CliRunner

from gypsy.scripts.cli import cli
from gypsy import DATA_DIR

def remove_path_if_exists(*paths):
    for path in paths:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except OSError:
            pass

def test_prep():
    input_data_path = os.path.join(DATA_DIR, 'raw_standtable.csv')
    expected_output_path = '%s.prepped' %input_data_path

    remove_path_if_exists(expected_output_path)

    runner = CliRunner()
    result = runner.invoke(cli, ['prep', input_data_path])

    assert result.exit_code == 0
    assert result.output == ""
    assert os.path.exists(expected_output_path)

def test_simulate():
    data_path = os.path.join(DATA_DIR, 'raw_standtable.csv.prepped')
    expected_output_path = os.path.join(os.getcwd(), 'gypsy-output')

    remove_path_if_exists(expected_output_path)

    runner = CliRunner()
    result = runner.invoke(cli, ['simulate', data_path])

    assert result.exit_code == 0
    assert result.output == ""
    assert os.path.exists(expected_output_path)
