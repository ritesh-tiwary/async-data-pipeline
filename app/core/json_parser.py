from app.logging import Logger
from app.core.base import Base


class JSONParser(Base):
    def __init__(self):
        self.logger = Logger(__name__)

    def parse(self,  name: str, bytes_obj: bytes) -> bool:
        self.logger.info(f'Parsing JSON file f{name} of f{len(bytes_obj)} bytes')
        return True

    def load(self,  name: str, bytes_obj: bytes) -> bool:
        self.logger.info(f'Loading JSON file f{name} of f{len(bytes_obj)} bytes')
        return True
