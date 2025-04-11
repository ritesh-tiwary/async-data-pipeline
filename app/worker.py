from celery import Celery
from app.logging import Logger
from app.settings import Settings


settings = Settings()
logger = Logger(__name__)
celery = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.file_tasks"]
)
celery.conf.update(task_track_started=True)
celery.conf.task_routes = {'app.tasks.file_tasks.add': {'queue': 'file-tasks-queue'}}

logger.info("Celery worker initialized")
logger.info(f"Broker URL: {settings.CELERY_BROKER_URL}")
logger.info(f"Result backend: {settings.CELERY_RESULT_BACKEND}")
