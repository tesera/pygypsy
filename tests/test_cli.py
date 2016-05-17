import os
from click.testing import CliRunner

from gypsy.scripts.cli import cli


def test_cli_count():
    log_file_path = os.path.join(os.getcwd(), 'gypsy.log')

    runner = CliRunner()
    result = runner.invoke(cli, ['run', '3'])

    assert result.exit_code == 0
    assert result.output == "False\nFalse\nFalse\n"
    assert os.path.exists(log_file_path)
