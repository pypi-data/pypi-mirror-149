from ewokscore.tests.examples.graphs import get_graph
from ..server import workflow_worker_pool
from ..client import submit, get_future
from ..client import submit_local, get_local_future


def test_submit(celery_session_worker):
    graph, expected = get_graph("acyclic1")
    expected = expected["task6"]
    future1 = submit(graph, outputs=[{"all": False}])
    future2 = get_future(future1.task_id)
    results = future1.get(timeout=3)
    assert results == expected
    results = future2.get(timeout=0)
    assert results == expected


def test_submit_local():
    with workflow_worker_pool():
        graph, expected = get_graph("acyclic1")
        expected = expected["task6"]
        future1 = submit_local(graph, outputs=[{"all": False}])
        future2 = get_local_future(future1.job_id)
        results = future1.result(timeout=3)
        assert results == expected
        results = future2.result(timeout=0)
        assert results == expected
