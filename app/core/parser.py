from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(self, filepath: str) -> bool:...

    @abstractmethod
    def load(self, filepath: str, mapping_name: str, mapping_obj: bytes) -> bool:...

def get_parser(name: str) -> Parser:
    """
    Factory function to get the appropriate parser based on the file type.
    """
    if name.endswith('.json'):
        from app.core.json_parser import JSONParser
        return JSONParser()
    elif name.endswith('.csv'):
        from app.core.csv_parser import CSVParser
        return CSVParser()
    else:
        raise ValueError(f"Unsupported file type: {name}")
