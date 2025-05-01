from pydantic import Field
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv()


class Settings(BaseSettings):
    # Database settings    
    POSTGRES_CONFIG: dict = Field({"database":"tasks","user":"dbuser","password":"dbpassword","host":"postgres_db","port":"5432", "min_size": 5,"max_size": 20}, env="POSTGRES_CONFIG")

    # Celery settings
    CELERY_BROKER_URL: str = Field("pyamqp://guest@localhost:5672//", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field("mongodb://admin:secret@localhost:27017/celery_results", env="CELERY_RESULT_BACKEND")

    # API settings
    API_KEY: str = Field("your_api_key", env="API_KEY")
    API_URL: str = Field("https://api.example.com", env="API_URL")

    # Other settings
    STORAGE_DIR: str = Field("uploads", env="STORAGE_DIR")
    DEBUG: bool = Field(False, env="DEBUG")
