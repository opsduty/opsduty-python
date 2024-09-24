import logging
from typing import Any

import pytest
from opsduty_python.heartbeats.heartbeats import (
    heartbeat_checkin,
    requests_retry_session,
    send_heartbeat_checkin,
)
from opsduty_python.settings import settings
from pytest_mock import MockerFixture
from requests import Session
from responses import RequestsMock
from urllib3.util.retry import Retry


def test_requests_retry_session() -> None:
    """Make sure retries are configured correctly."""

    retries = 10
    backoff_factor = 10.0
    status_forcelist = (500,)

    session = requests_retry_session(
        session=Session(),
        retries=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )

    https_adapter = session.adapters["https://"]
    retry: Retry = https_adapter.max_retries

    assert retry.total == retries
    assert retry.connect == retries
    assert retry.read == retries
    assert retry.backoff_factor == backoff_factor
    assert retry.status_forcelist == status_forcelist


@pytest.mark.parametrize("enabled", (True, False))
@pytest.mark.parametrize("job_raise_error", (True, False))
@pytest.mark.parametrize("environment", ("prod", None))
def test_heartbeat_checkin(
    enabled: bool, job_raise_error: bool, environment: str | None, mocker: MockerFixture
) -> None:
    """Make sure the decorator calls send_heartbeat_checkin when it should."""

    mock = mocker.patch("opsduty_python.heartbeats.heartbeats.send_heartbeat_checkin")

    @heartbeat_checkin(heartbeat="test", environment=environment, enabled=enabled)
    def job() -> None:
        if job_raise_error:
            raise RuntimeError("Job failed")

    if job_raise_error:
        with pytest.raises(RuntimeError):
            job()
    else:
        job()

    if enabled and not job_raise_error:
        mock.assert_called_once_with(
            heartbeat="test", environment=environment, timeout=None
        )
    else:
        mock.assert_not_called()


@pytest.mark.parametrize("opsduty_base_url", ("https://test.com", "https://opsduty.io"))
@pytest.mark.parametrize("environment", ("prod", None))
def test_send_heartbeat_checkin(
    opsduty_base_url: str, environment: str | None, responses: RequestsMock
) -> None:
    """Test send_heartbeat_checkin."""

    heartbeat = "test"

    settings.OPSDUTY_BASE_URL = opsduty_base_url

    url = f"{opsduty_base_url}/heartbeats/checkin/{heartbeat}/"
    if environment is not None:
        url += f"{environment}/"

    # The test will fail if we don't execute this request.
    responses.add(responses.GET, url=url, status=202)

    send_heartbeat_checkin(heartbeat=heartbeat, environment=environment)


def test_send_heartbeat_not_found(responses: RequestsMock, caplog: Any) -> None:
    """Make sure the send_heartbeat_checkin method handles 404s."""

    url = f"{settings.OPSDUTY_BASE_URL}/heartbeats/checkin/not-found/"

    # The test will fail if we don't execute this request.
    responses.add(responses.GET, url=url, status=404)

    with caplog.at_level(logging.WARNING):
        send_heartbeat_checkin(heartbeat="not-found", environment=None)

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert "was not found." in record.message


def test_decorator_adds_flag() -> None:
    """
    Make sure the decorator adds a has_heartbeat_checkin flag on
    the decorated function.
    """

    def f() -> None:
        pass

    func = heartbeat_checkin(heartbeat="", environment=None)(f)

    assert func.has_heartbeat_checkin  # type: ignore
