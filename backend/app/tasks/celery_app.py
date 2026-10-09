from __future__ import annotations
from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "rasta_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "main-queue"}
}
