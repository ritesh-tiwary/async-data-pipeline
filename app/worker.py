from app import settings
from celery import Celery


# Create Celery app with SQLAlchemy as broker
celery = Celery(
    "tasks",
    broker=f"sqla+{settings.db_url}",        # Use SQLAlchemy with Sybase
    backend=f"db+{settings.db_url}"          # No result backend for better performance
)

celery.conf.update(task_track_started=True)