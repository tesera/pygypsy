from click.testing import CliRunner

from gypsy.scripts.cli import cli

def test_cli_config_file(cli_config_file): #pylint: disable=missing-docstring
    runner = CliRunner()
    result = runner.invoke(cli, ['--config-file', cli_config_file,
                                 'prep', '-h'])
    assert result.exit_code == 0

def test_cli_invalid_config_file(invalid_cli_config_file): #pylint: disable=missing-docstring
    runner = CliRunner()
    result = runner.invoke(cli, ['--config-file', invalid_cli_config_file,
                                 'prep', '-h'])
    assert result.exit_code != 0
