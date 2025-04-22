from functools import lru_cache
from app.settings import Settings

class Base:
    def __init__(self):
        self.settings = self.get_settings()

    @lru_cache()
    def get_settings(self):
        return Settings()
