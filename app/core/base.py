from functools import lru_cache
from app.settings import Settings
from app.logging import Logger


class Base:
    def __init__(self, name: str = __name__):
        self.logger = Logger(name)
        self.settings = self.get_settings()

    @lru_cache()
    def get_settings(self):
        return Settings()
