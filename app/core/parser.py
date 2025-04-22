from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(self, name: str, bytes_obj: bytes) -> bool:...

    @abstractmethod
    def load(self,  name: str, bytes_obj: bytes) -> bool:...
