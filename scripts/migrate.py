from app import settings
from sqlalchemy import create_engine, text

engine = create_engine(settings.db_url)
def migrate():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS migrations (id INT PRIMARY KEY, name VARCHAR(255))"))
        print("Database migration completed.")

if __name__ == "__main__":
    migrate()