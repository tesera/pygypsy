from click.testing import CliRunner

from gypsy.scripts.cli import cli
from gypsy.scripts import DEFAULT_CONF_FILE

def test_cli_config_file(): #pylint: disable=missing-docstring
    runner = CliRunner()
    result = runner.invoke(cli, ['--config-file', DEFAULT_CONF_FILE,
                                 'prep', '-h'])

    assert result.exit_code == 0
    # TODO: check that config is on ctx.obj, or do it with a callback and test
    # the callback and mock the ctx

def test_cli_invalid_config_file(invalid_cli_config_file): #pylint: disable=missing-docstring
    runner = CliRunner()
    result = runner.invoke(cli, ['--config-file', invalid_cli_config_file,
                                 'prep', '-h'])
    assert result.exit_code != 0
    assert 'error reading the config file' in result.output

def test_cli_missing_config_file(): #pylint: disable=missing-docstring
    runner = CliRunner()
    result = runner.invoke(cli, ['--config-file', 'no/such/file.cfg',
                                 'prep', '-h'])

    assert result.exit_code != 0
    assert 'Invalid value for "--config-file"' in result.output
