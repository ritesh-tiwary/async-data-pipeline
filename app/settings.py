from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field("tasks", env="DB_NAME")
    DB_USER: str = Field("dbuser", env="DB_USER")
    DB_PASSWORD: str = Field("dbpassword", env="DB_PASSWORD")

    # Celery settings
    CELERY_BROKER_URL: str = Field("redis://localhost:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field("redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")

    # API settings
    API_KEY: str = Field("your_api_key", env="API_KEY")
    API_URL: str = Field("https://api.example.com", env="API_URL")

    # Other settings
    DEBUG: bool = Field(False, env="DEBUG")