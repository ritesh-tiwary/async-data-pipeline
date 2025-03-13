import asyncio
from app.worker import celery
from app.logging import logger
from app.settings import db_url
from celery.exceptions import MaxRetriesExceededError

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


# Create SQLAlchemy engine
engine = create_async_engine(db_url, echo=True)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Define the table
class FileData(Base):
    __tablename__ = 'file_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, index=True)
    content = Column(String)

# Create sessionmaker
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
    )


@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def save_to_db(self, filename: str, content: str):
    try:
        async def async_save():
            async with async_session() as session:
                async with session.begin():
                    file_data = FileData(filename=filename, content=content)
                    session.add(file_data)
                    await session.commit()
        asyncio.run(async_save())
    except Exception as e:
        try:
            logger.warning(f"Retrying task due to error: {e}")
            raise self.retry(exc=e)
        except MaxRetriesExceededError:
            logger.error("Max retries reached. Task failed permanently.")
            return None
