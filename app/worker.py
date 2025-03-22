from app import settings
from celery import Celery


# Create Celery app with mongodb as broker
celery = Celery(
    "tasks",
    broker=settings.celery_broker_url, 
    backend=settings.celery_result_backend
)

celery.conf.update(task_track_started=True)