import asyncio
import datetime
import urllib.request
from typing import Any

import pytest

from arq_prometheus.client import ArqPrometheusMetrics


@pytest.fixture
def futures_factory(result: Any = None):
    """Produce futures with an explicit result, useful to mock async calls."""

    def wrapper(result: Any):
        f: asyncio.Future = asyncio.Future()
        f.set_result(result)
        return f

    return wrapper


@pytest.fixture
def aredis_mock(mocker, futures_factory):
    """Async mock"""

    def wrapper(result: Any = None):
        m = mocker.Mock()
        m.get.return_value = futures_factory(result)
        return m

    return wrapper


@pytest.mark.asyncio
async def test_client_called_once(registry, aredis_mock):

    # Easy coroutine mock
    redis = aredis_mock()

    ctx = {"redis": redis}
    arq_prom_instance = ArqPrometheusMetrics(
        ctx=ctx,
        registry=registry,
        enable_webserver=False,
        delay=datetime.timedelta(milliseconds=800),
    )
    await arq_prom_instance.start()
    await asyncio.sleep(1)
    await arq_prom_instance.stop()

    redis.get.assert_called_once_with(arq_prom_instance.health_check_key)


@pytest.mark.asyncio
async def test_client_called_some_times(registry, aredis_mock):
    """Inside a second, it should be called aprox 5 times."""
    # Easy coroutine mock
    redis = aredis_mock()

    ctx = {"redis": redis}
    arq_prom_instance = ArqPrometheusMetrics(
        ctx=ctx,
        registry=registry,
        enable_webserver=False,
        delay=datetime.timedelta(milliseconds=200),
    )
    await arq_prom_instance.start()
    await asyncio.sleep(1)
    await arq_prom_instance.stop()

    redis.get.assert_called_with(arq_prom_instance.health_check_key)
    assert 8 > redis.get.call_count > 3


@pytest.mark.asyncio
async def test_integration_read_sequence_and_report_properly(
    registry, aredis_mock, futures_factory, mocker
):
    """In the 3 times it gets called, it should report the latest values."""

    # Mock data
    read_sequence = [
        futures_factory("j_complete=0 j_failed=0 j_retried=0 j_ongoing=0 queued=0"),
        futures_factory("j_complete=1 j_failed=0 j_retried=0 j_ongoing=0 queued=4"),
        futures_factory("j_complete=4 j_failed=8 j_retried=0 j_ongoing=235 queued=119"),
        mocker.DEFAULT,
        mocker.DEFAULT,
    ]
    redis = aredis_mock()
    redis.get.side_effect = read_sequence

    # Initialize our arq prom instance
    ctx = {"redis": redis}
    arq_prom_instance = ArqPrometheusMetrics(
        ctx=ctx,
        registry=registry,
        enable_webserver=True,
        delay=datetime.timedelta(milliseconds=200),
    )
    # Start arq prom
    await arq_prom_instance.start()

    # Let it sleep for a sec, it should gather all metrics
    await asyncio.sleep(1)
    # We ask the web server for the metrics result
    http_contents = urllib.request.urlopen("http://localhost:8081").read()
    # Stop everything
    await arq_prom_instance.stop()

    # Assert results
    redis.get.assert_called_with(arq_prom_instance.health_check_key)
    assert 8 > redis.get.call_count > 3
    assert b"arq_jobs_completed 4.0" in http_contents
    assert b"arq_jobs_failed 8.0" in http_contents
    assert b"arq_jobs_retried 0.0" in http_contents
    assert b"arq_jobs_ongoing 235.0" in http_contents
    assert b"arq_queued_inprogress 119.0" in http_contents
