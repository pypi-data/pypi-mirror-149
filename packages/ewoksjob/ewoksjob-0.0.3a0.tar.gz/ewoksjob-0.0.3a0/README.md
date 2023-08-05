# ewoksjob

Utilities for job scheduling of [Ewoks](https://gitlab.esrf.fr/workflow/ewoks/ewoks) workflows.

Ewoks has different interfaces to execute an ewoks workflow: python API, CLI, REST API, Qt GUI, Web GUI.

Ewoksjob provides an ewoks interface for asynchronous and distributed scheduling of ewoks workflows from python.

Note that ewoksjob distributes the execution of workflows while [ewoksdask](https://gitlab.esrf.fr/workflow/ewoks/ewoksdask)
distributes the execution of tasks in a workflow. So in the context of workflows, job scheduling exists on two levels.

The primary clients that need to schedule workflows are
* [Ewoksserver](https://gitlab.esrf.fr/workflow/ewoks/ewoksserver): web backend for ewoks.
* [Bliss](https://gitlab.esrf.fr/bliss/bliss): the ESRF beamline control system.
* [Daiquiri](https://gitlab.esrf.fr/ui/daiquiri): web backend for Bliss.

## Installation

Install on the client side

```bash
pip install ewoksjob[fullclient]
```

The optional `fullclient` install option should be used when you want full client-side capabilities,
for exampe dereference URL's of ewoks task results.

Install on the worker side

```bash
pip install ewoksjob[worker]
```

## Tests

```bash
pytest --pyargs ewoksjob
```

The test environment needs `redis-server` (e.g. `conda install redis-server`).

## Getting started

Start a worker pool that can execute ewoks graphs

```bash
examples/worker.sh
```

Start a workflow on the client side

```bash
python examples/job.py
```

Adapt the three URL's as needed (ewoks events, celery message broker, celery job result storage).

## Documentation

https://ewoksjob.readthedocs.io/
