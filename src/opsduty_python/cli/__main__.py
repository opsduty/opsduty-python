import click

from opsduty_python.cli.cli_groups import LazyGroup
from opsduty_python.utils import logging

# Give us nice and short help parameters, too
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.version_option()
@click.group(
    context_settings=CONTEXT_SETTINGS,
    epilog="""
Command-line utility for interfacing with OpsDuty.
           """,
)
@click.option(
    "--log-format",
    type=click.Choice(logging.LOG_FORMATS, case_sensitive=False),
    default=str(logging.LogFormat.CONSOLE.value),
    show_default=True,
)
@click.option(
    "--log-level",
    type=click.Choice(logging.LOG_LEVELS, case_sensitive=False),
    default=str(logging.LogLevel.INFO.value),
    show_default=True,
)
@click.option(
    "--access-token",
    default=None,
    required=False,
    help="Set the bearer token used to communicate with OpsDuty.",
)
@click.pass_context
def opsduty(
    ctx: click.Context, log_format: str, log_level: str, access_token: str
) -> None:
    logging.configure_structlog(
        log_level=logging.LogLevel(log_level), log_format=logging.LogFormat(log_format)
    )


@click.group(
    cls=LazyGroup,
    lazy_subcommands={
        "checkin": "opsduty_python.cli.heartbeats.checkin",
    },
    help="Commands for managing and monitoring heartbeats.",
)
def heartbeats() -> None:
    pass


# Add CLI groups.
opsduty.add_command(heartbeats)


if __name__ == "__main__":
    opsduty()
