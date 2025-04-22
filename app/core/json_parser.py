from app.logging import Logger
from app.core.parser import Parser


class JSONParser(Parser):
    def __init__(self):
        self.logger = Logger(__name__)

    def parse(self,  name: str, bytes_obj: bytes) -> bool:
        self.logger.info(f'Parsing JSON file {name} of {len(bytes_obj)} bytes')
        return True

    def load(self,  name: str, bytes_obj: bytes) -> bool:
        self.logger.info(f'Loading JSON file {name} of {len(bytes_obj)} bytes')
        return True
