from celery import Celery
from app.logging import Logger
from app.settings import Settings


settings = Settings()
logger = Logger(__name__)
celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.worker.tasks"]
)
celery.conf.update(task_track_started=True)
task_names = ['add', 'save', 'load', 'parse']
celery.conf.task_routes = {f'app.worker.tasks.{task}': {'queue': 'tasks-queue'} for task in task_names}

logger.info("Celery worker initialized")
logger.info(f"Broker URL: {settings.CELERY_BROKER_URL}")
logger.info(f"Result backend: {settings.CELERY_RESULT_BACKEND}")
