import click
import structlog

from opsduty_python.heartbeats import send_heartbeat_checkin as _send_heartbeat_checkin

logger = structlog.get_logger()


@click.command(help="Send a heartbeat checkin to OpsDuty.")
@click.argument("heartbeat", type=str, envvar="HEARTBEAT")
@click.option(
    "--environment",
    "-e",
    type=str,
    required=False,
    default=None,
    help="Specify the environment for the heartbeat (e.g., production, staging, development).",
    envvar="ENV",
    show_envvar=True,
)
@click.option(
    "--timeout",
    type=int,
    required=True,
    default=10,
    help="Specify the request timeout to OpsDuty.",
)
def checkin(*, heartbeat: str, environment: str | None, timeout: int) -> None:
    logger.debug(
        "Sending heartbeat checkin", heartbeat=heartbeat, environment=environment
    )

    success = _send_heartbeat_checkin(
        heartbeat=heartbeat, environment=environment, timeout=timeout
    )

    if not success:
        raise click.ClickException(
            message="Could not send heartbeat checkin to OpsDuty."
        )
