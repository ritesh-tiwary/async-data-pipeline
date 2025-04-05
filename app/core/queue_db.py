# Initialize SQLAlchemy Tables for Celery
# Run the this script (init_queue_db.py) only once to create the required Celery queue tables.
# Verify Celery Queue in Sybase
# SELECT * FROM kombu_message;


from sqlalchemy import create_engine
from processor.celeryconfig import db_url
from app.settings import settings
from kombu.transport.sqlalchemy.models import Base

engine = create_engine(settings)
Base.metadata.create_all(engine)
print("Celery queue tables created successfully.")