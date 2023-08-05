import os
import celery
import ewoks


app = celery.Celery("ewoks")
if os.environ.get("CELERY_CONFIG_MODULE"):
    app.config_from_envvar("CELERY_CONFIG_MODULE", force=True)


@app.task(bind=True)
def execute_graph(self, *args, execinfo=None, **kwargs):
    if execinfo is None:
        execinfo = dict()
    if "job_id" not in execinfo:
        execinfo["job_id"] = self.request.id
    return ewoks.execute_graph(*args, execinfo=execinfo, **kwargs)
