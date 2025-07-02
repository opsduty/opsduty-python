from click.testing import CliRunner

from opsduty_python.cli.__main__ import opsduty


def test_invoke_cli_without_args_or_commands() -> None:
    runner = CliRunner()
    result = runner.invoke(opsduty)
    assert result.exit_code == 0

    assert "Usage: opsduty" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output

    commands = opsduty.commands.keys()
    assert commands, "No commands found"

    for command in commands:
        assert command in result.output


def test_invoke_subcommands_with_help() -> None:
    runner = CliRunner()

    commands = opsduty.commands.keys()

    for command in commands:
        result = runner.invoke(opsduty, [command, "--help"])
        assert result.exit_code == 0

        assert f"Usage: opsduty {command}" in result.output
        assert "Options:" in result.output
        assert "Commands:" in result.output


def test_invoke_cli_with_help_flag() -> None:
    runner = CliRunner()
    result = runner.invoke(opsduty, ["--help"])
    assert result.exit_code == 0

    assert "Usage: opsduty" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
