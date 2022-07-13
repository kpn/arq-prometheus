# Arq simple worker

This example showcases a simple worker exposing prometheus metrics.

Create a `venv` at the root of the arq-promethus folder and install it.

```sh
python -m venv .venv
. .venv/bin/activate
poetry install
```

then navigate to the folder where this readme is located and install also the requirements.txt

```sh
pip install -r requirements.txt
```


Start redis inside docker:

```sh
example/arq_prometheus_worker/scripts/init_redis
```

Run the worker:

```sh
example/arq_prometheus_worker/scripts/run
```

Trigger jobs:

```sh
example/arq_prometheus_worker/scripts/trigger-job
```

Observe by going to localhost:8081