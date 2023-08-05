from click.testing import CliRunner

from facilyst.__main__ import cli


def test_print_cli_cmd():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
