import io
import re
import orjson
import duckdb
from typing import List, Tuple
from app.logging import Logger
from app.core.parser import Parser


class JSONParser(Parser):
    def __init__(self):
        self.logger = Logger(__name__)
        self.raw_data = None

    def generate_duckdb_select_query(self, mapping_df, json_path, table_alias='j') -> str:
        """ Generate a DuckDB query to extract JSON fields based on the provided mapping. """        
        select_clauses = [
            f"{'json_extract_string' if row['duckdb_type'].__eq__('string') else 'json_extract'}({table_alias}, '{row['json_path']}') AS {row['column_name']}"
            for _, row in mapping_df.iterrows()
        ]

        select_str = ",\n    ".join(select_clauses)
        return f"SELECT\n    {select_str}\nFROM read_json_auto('{json_path}') AS {table_alias}"

    def generate_database_insert_query(self, table_name: str, db_columns: List[str]) -> str:
        """ Generate a database query to insert data into a table based on the provided mapping. """        
        placeholders = ", ".join(f"${i+1}" for i in range(len(db_columns)))        
        insert_sql = f"""
            INSERT INTO {table_name} ({', '.join(db_columns)})
            VALUES ({placeholders})
            """
        return insert_sql

    def validate(self, filepath: str) -> bool:
        """Load, repair and validate potentially broken JSON file"""
        self.logger.info(f'Validating JSON file {filepath}')
        try:
            try:
                # Attempt to load the JSON data
                with open(filepath, 'rb') as f:
                    self.raw_data = orjson.loads(f)
            except orjson.JSONDecodeError:
                try:
                    self.logger.warning(f'Failed to load JSON file {filepath}, attempting repairs')
                    # Apply common JSON repairs
                    repairs = [
                        (r',(\s*[}\]])', r'\1'),                                    # Remove trailing commas
                        (r'//.*?\n', ''),                                           # Remove JavaScript-style comments
                        (r'(\s*"[^"]+"\s*:\s*)"([^"]+)"\s*([,}\]])', r'\1"\2"\3'),  # Fix unquoted values
                        (r'"\s*\+\s*"', ''),                                        # Remove string concatenation
                        (r'[\x00-\x1f\x7f-\x9f]', ' ')                              # Remove control characters
                    ]

                    # Decode bytes to string
                    with open(filepath, 'rb') as f:
                        bytes_obj = f.read()
                    
                    content = bytes_obj.decode('utf-8', errors='replace')
                    for pattern, replacement in repairs:
                        content = re.sub(pattern, replacement, content)
                    
                    # Ensure valid JSON structure
                    if not content.strip().endswith(('}', ']')):
                        content = content.rsplit(',', 1)[0] + ('}' if '{' in content else ']')
                    
                    self.raw_data = orjson.loads(content.encode('utf-8'))
                except orjson.JSONDecodeError as e:
                    self.logger.error(f'Failed to repair JSON file {filepath}: {e}')
                    return False
        except Exception as e:
            self.logger.error(f'Error validating JSON file {filepath}: {e}')
        return True

    def parse(self, filepath: str) -> bool:
        if self.validate(filepath):
            parsed_json = filepath.replace('.json', '_parsed.json')
            with open(parsed_json, 'wb') as f:
                f.write(orjson.dumps(self.raw_data))
            return parsed_json
        else:
            self.logger.error(f'Failed to parse JSON file {name}')
            return False

    def load(self, filepath: str, mapping_name: str, mapping_obj: bytes) -> bool:
        self.logger.info(f'Loading JSON file from {filepath}')        
        mapping_df = duckdb.read_csv(io.BytesIO(mapping_obj), encoding='utf-8').to_df()        
        table_name = mapping_name.split('_')[1]
        columns_name = mapping_df['db_column'].tolist()
        
        select_query = self.generate_duckdb_select_query(mapping_df, filepath)
        insert_query = self.generate_database_insert_query(table_name, columns_name)
        rows = duckdb.sql(select_query).fetchall()
        
        self.logger.info(f'Inserting {len(rows)} rows into {table_name} with query: {insert_query}')
        return True
