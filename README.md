# Arq-prometheus

Prometheus metrics for [arq](https://github.com/samuelcolvin/arq)

## Installation

```sh
pip install -U arq-prometheus
```

Alternatively

```sh
poetry add arq-prometheus
```

## Description

This is an alpha release. The metrics exposed are the same as the health check.

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
    arq_prometheus = ArqPrometheusMetrics(
        ctx, delay=delay, enable_webserver=True
    )
    ctx["arq_prometheus"] = await arq_prometheus.start()

async def shutdown(ctx):
    await ctx["arq_prometheus"].stop()

class WorkerSettings:
    on_startup = startup
    on_shutdown = shutdown
    function = []  # your arq jobs
    ... # other settings

````

Start your arq worker:

```sh
arq example_worker.WorkerSettings
```

