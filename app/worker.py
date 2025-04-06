from celery import Celery
from app.logging import Logger
from app.settings import Settings


class Worker:
    def __init__(self):
        self.settings = Settings()
        self.logger = Logger(__name__)
        self.celery = Celery(
            "tasks",
            broker=self.settings.CELERY_BROKER_URL,
            backend=self.settings.CELERY_RESULT_BACKEND,
            include=["app.tasks.task"],
        )
        self.celery.conf.update(task_track_started=True)
        
        self.logger.info("Celery worker initialized")
        self.logger.info(f"Broker URL: {self.settings.CELERY_BROKER_URL}")
        self.logger.info(f"Result backend: {self.settings.CELERY_RESULT_BACKEND}")
