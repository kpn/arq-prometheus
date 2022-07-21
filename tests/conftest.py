import pytest
from prometheus_client import CollectorRegistry

from arq_prometheus.client import ArqPrometheusMetrics


@pytest.fixture
def registry():
    return CollectorRegistry()


@pytest.fixture
def arq_prom_instance(registry):
    return ArqPrometheusMetrics(ctx={}, registry=registry, enable_webserver=False)
