import asyncio
import asyncpg

async def connect_db():
    DB_NAME = "tasks"
    DB_USER = "dbuser"
    DB_PASSWORD = "dbpassword"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    CREATE_TABLE = """
    CREATE TABLE tbl_users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    user_name TEXT NOT NULL,
    user_age INT,
    user_location TEXT
    );
    CREATE TABLE tbl_failed_inserts (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    failed_inserts_query TEXT NOT NULL,
    failed_inserts_record TEXT NOT NULL,
    failed_inserts_error TEXT NOT NULL
    );
    """

    DROP_TABLE = """
    DROP TABLE IF EXISTS tbl_users;
    DROP TABLE IF EXISTS tbl_failed_inserts;
    """

    try:
        conn = await asyncpg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        # Execute a test query
        # await conn.execute(CREATE_TABLE)
        version = await conn.fetchval("SELECT version();")
        print("PostgreSQL Version:", version)

        # Close connection
        await conn.close()

    except Exception as e:
        print("Database connection error:", e)

# Run async function
asyncio.run(connect_db())
