from typing import Optional, Tuple
from concurrent.futures import Future

from celery.execute import send_task
from celery.result import AsyncResult

try:
    from . import server
except ImportError as e:
    server = None
    server_import_error = e

_EWOKS_TASK = "ewoksjob.apps.ewoks.execute_graph"


def submit(*args, **kwargs) -> Tuple[AsyncResult, int]:
    return send_task(_EWOKS_TASK, args=args, kwargs=kwargs)


def submit_local(*args, **kwargs) -> Tuple[Future, int]:
    """'Local' means that the worker pool runs in the same
    process as the client.
    """
    if server is None:
        raise ImportError(server_import_error)
    pool = server.active_workflow_worker_pool()
    if pool is None:
        raise RuntimeError("No worker pool is available")
    return server._EWOKS_WORKER_POOL.submit(*args, **kwargs)


def get_future(job_id) -> Optional[AsyncResult]:
    return AsyncResult(job_id)


def get_local_future(job_id) -> Optional[Future]:
    if server is None:
        raise ImportError(server_import_error)
    pool = server.active_workflow_worker_pool()
    return pool.get_future(job_id)


def cancel(job_id):
    future = get_future(job_id)
    if future is not None:
        future.revoke()


def cancel_local(job_id):
    future = get_local_future(job_id)
    if future is not None:
        future.cancel()


def get_result(job_id, **kwargs):
    kwargs.setdefault("interval", 0.1)
    future = AsyncResult(job_id)
    if future is not None:
        return future.get(**kwargs)


def get_local_result(job_id, **kwargs):
    future = get_local_future(job_id)
    if future is not None:
        return future.result(**kwargs)
