import sys
from typing import Optional, Tuple
from uuid import uuid4
from contextlib import contextmanager
import multiprocessing
import weakref
from concurrent.futures import ProcessPoolExecutor, Future
from ewoks import execute_graph

_EWOKS_WORKER_POOL = None


def active_workflow_worker_pool():
    return _EWOKS_WORKER_POOL


class WorkflowWorkerPool(ProcessPoolExecutor):
    def __init__(self, *args, **kwargs) -> None:
        if sys.version_info < (3, 7):
            kwargs.pop("mp_context", None)
        self._jobs = weakref.WeakValueDictionary()
        super().__init__(*args, **kwargs)

    def submit(self, *args, execinfo=None, **kwargs) -> Tuple[Future, int]:
        if execinfo is None:
            execinfo = dict()
        job_id = execinfo.get("job_id")
        if "job_id" not in execinfo:
            execinfo["job_id"] = job_id = str(uuid4())
        if job_id in self._jobs:
            raise RuntimeError(f"Job '{job_id}' already exists")
        future = super().submit(execute_graph, *args, execinfo=execinfo, **kwargs)
        future.job_id = job_id
        self._jobs[job_id] = future
        return future

    def get_future(self, job_id) -> Optional[Future]:
        return self._jobs.get(job_id)


@contextmanager
def workflow_worker_pool(max_workers=1, context="spawn"):
    global _EWOKS_WORKER_POOL
    if _EWOKS_WORKER_POOL is None:
        if sys.version_info < (3, 7):
            ctx = None
        else:
            ctx = multiprocessing.get_context(context)
        with WorkflowWorkerPool(max_workers=max_workers, mp_context=ctx) as pool:
            _EWOKS_WORKER_POOL = pool
            try:
                yield pool
            finally:
                _EWOKS_WORKER_POOL = None
    else:
        yield _EWOKS_WORKER_POOL
