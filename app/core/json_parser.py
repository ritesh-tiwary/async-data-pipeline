import io
import re
import orjson
import duckdb
from pandas import read_csv
from typing import List, Tuple
from app.logging import Logger
from app.core.parser import Parser


class JSONParser(Parser):
    def __init__(self):
        self.logger = Logger(__name__)
        self.raw_data = None

    def generate_duckdb_select_query(self, mapping_df, table_alias='j') -> str:
        """ Generate a DuckDB query to extract JSON fields based on the provided mapping. """
        select_clauses = [
            f"json_extract_{row['duckdb_type']}({table_alias}, '{row['json_path']}') AS {row['column_name']}"
            for _, row in mapping_df.iterrows()
        ]
        select_str = ",\n    ".join(select_clauses)
        return f"SELECT\n    {select_str}\nFROM read_json_auto(?) AS {table_alias}"

    def generate_database_insert_query(self, table_name: str, db_columns: List[str]) -> str:
        """ Generate a database query to insert data into a table based on the provided mapping. """        
        placeholders = ", ".join(f"${i+1}" for i in range(len(db_columns)))        
        insert_sql = f"""
            INSERT INTO {table_name} ({', '.join(db_columns)})
            VALUES ({placeholders})
            """
        return insert_sql

    def validate(self, name: str, bytes_obj: bytes) -> bool:
        """Load, repair and validate potentially broken JSON file"""
        self.logger.info(f'Validating JSON file {name} of {len(bytes_obj)} bytes')
        try:
            try:
                # Attempt to load the JSON data
                self.raw_data = orjson.loads(bytes_obj)
            except orjson.JSONDecodeError:
                try:
                    self.logger.warning(f'Failed to load JSON file {name}, attempting repairs')
                    # Apply common JSON repairs
                    repairs = [
                        (r',(\s*[}\]])', r'\1'),                                    # Remove trailing commas
                        (r'//.*?\n', ''),                                           # Remove JavaScript-style comments
                        (r'(\s*"[^"]+"\s*:\s*)"([^"]+)"\s*([,}\]])', r'\1"\2"\3'),  # Fix unquoted values
                        (r'"\s*\+\s*"', ''),                                        # Remove string concatenation
                        (r'[\x00-\x1f\x7f-\x9f]', ' ')                              # Remove control characters
                    ]

                    # Decode bytes to string
                    content = bytes_obj.decode('utf-8', errors='replace')
                    for pattern, replacement in repairs:
                        content = re.sub(pattern, replacement, content)
                    
                    # Ensure valid JSON structure
                    if not content.strip().endswith(('}', ']')):
                        content = content.rsplit(',', 1)[0] + ('}' if '{' in content else ']')
                    
                    self.raw_data = orjson.loads(content.encode('utf-8'))
                except orjson.JSONDecodeError as e:
                    self.logger.error(f'Failed to repair JSON file {name}: {e}')
                    return False
        except Exception as e:
            self.logger.error(f'Error validating JSON file {name}: {e}')
        return True

    def parse(self,  name: str, bytes_obj: bytes) -> bool:
        self.logger.info(f'Parsing JSON file {name} of {len(bytes_obj)} bytes')
        if self.validate(name, bytes_obj):
            return True
        else:
            self.logger.error(f'Failed to parse JSON file {name}')
            return False

    def load(self,  name: str, data: dict, mapping_name: str, mapping_obj: bytes) -> bool:
        self.logger.info(f'Loading JSON file {name} of {len(bytes_obj)} bytes')
        mapping_df = read_csv(io.BytesIO(mapping_obj), encoding='utf-8')
        select_query = self.generate_duckdb_select_query(mapping_df)
        json_str = [orjson.dumps(obj) for obj in data]
        rows = duckdb.query(select_query, [json_str]).fetchall()
        print("rows created")
        
        table_name = mapping_name.split('_')[1]
        columns_name = mapping_df['db_column'].tolist()
        insert_query = self.generate_database_insert_query(table_name, columns_name)
        self.logger.info(f'Inserting data into {table_name} with query: {insert_query}')
        return True
