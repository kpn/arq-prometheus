# Arq-prometheus

![Build status](https://github.com/kpn/arq-prometheus/actions/workflows/test.yaml/badge.svg)
[![PyPI Package latest release](https://img.shields.io/pypi/v/arq-prometheus.svg?style=flat-square)](https://pypi.org/project/arq-prometheus/)
[![PyPI Package download count (per month)](https://img.shields.io/pypi/dm/arq-prometheus?style=flat-square)](https://pypi.org/project/arq-prometheus/)
[![Supported versions](https://img.shields.io/pypi/pyversions/arq-prometheus.svg?style=flat-square)](https://pypi.org/project/arq-prometheus/)
[![Codecov](https://img.shields.io/codecov/c/github/kpn/arq-prometheus.svg?style=flat-square)](https://codecov.io/gh/kpn/arq-prometheus)


Prometheus metrics for [arq](https://github.com/samuelcolvin/arq)

⚠️ WARNING! This is a project in alpha phase ⚠️

## Installation

[Pip](https://pip.pypa.io/en/stable/)

```sh
pip install -U arq-prometheus
```

[Poetry](https://python-poetry.org/)

```sh
poetry add arq-prometheus
```

## Description

The metrics exposed are the same as the health check.

| Metric name             | Description                      |
| ----------------------- | -------------------------------- |
| `arq_jobs_completed`    | The number of jobs completed     |
| `arq_jobs_failed`       | The total number of errored jobs |
| `arq_jobs_retried`      | The total number of retried jobs |
| `arq_ongoing_jobs`      | The number of jobs in progress   |
| `arq_queued_inprogress` | The number of jobs in progress   |

When working with `arq` I found some limitations, it was specially hard to get access to
the worker in order to retrieve information like the `queue_name` or `health_check_key`.
The startup and shutdown functions only make available a `ctx` with the redis connection.
This means that if you provide a custom `queue_name` or `health_check_key`, you will
also have to provide them to `ArqPrometheusMetrics`.

## Usage

````python
# example_worker.py
from arq_prometheus import ArqPrometheusMetrics

async def startup(ctx):
    arq_prometheus = ArqPrometheusMetrics(ctx, delay=delay)
    ctx["arq_prometheus"] = await arq_prometheus.start()

async def shutdown(ctx):
    await ctx["arq_prometheus"].stop()

class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    function = []  # your arq jobs
    ... # other settings

````

Start your arq worker,

```sh
arq example_worker.WorkerSettings
```

Make request to `localhost:8081` (or open in browser).

```sh
curl localhost:8081
```


## Arguments

- `ctx: dict`: arq context
- `queue_name: str = default_queue_name`: name of the arq queue
- `health_check_key: Optional[str] = None`: arq health key
- `delay: datetime.timedelta = datetime.timedelta(seconds=5)`: a datetime.timedelta
- `enable_webserver: bool = True`: set to True if you want a web server exposing the metrics
- `addr: str = "0.0.0.0"`: webserver address
- `port: int = 8081`: webserver port
- `registry: prom.CollectorRegistry = prom.REGISTRY`: the prometheus registry, usually you do not have to override this