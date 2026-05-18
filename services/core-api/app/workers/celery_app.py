from datetime import timedelta

from ..config import ALERT_DISPATCH_INTERVAL_MINUTES, REDIS_URL

try:
    from celery import Celery

    celery = Celery("careeros", broker=REDIS_URL, backend=REDIS_URL)
    celery.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        beat_schedule={
            "dispatch-job-alerts": {
                "task": "app.workers.tasks.dispatch_job_alerts",
                "schedule": timedelta(minutes=max(1, ALERT_DISPATCH_INTERVAL_MINUTES)),
            }
        },
    )
except Exception:
    class _FakeTask:
        def __init__(self, fn):
            self.fn = fn

        def delay(self, *args, **kwargs):
            return self.fn(*args, **kwargs)

        def apply(self, args=None, kwargs=None):
            args = args or []
            kwargs = kwargs or {}
            return self.fn(*args, **kwargs)

    class _FakeCelery:
        def task(self, fn):
            return _FakeTask(fn)

    celery = _FakeCelery()
