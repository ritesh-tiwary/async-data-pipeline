import asyncio
import asyncpg

async def connect_db():
    DB_NAME = "tasks"
    DB_USER = "dbuser"
    DB_PASSWORD = "dbpassword"
    DB_HOST = "postgres_db"
    DB_PORT = "5432"

    try:
        conn = await asyncpg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        # Execute a test query
        version = await conn.fetchval("SELECT version();")
        print("PostgreSQL Version:", version)

        # Close connection
        await conn.close()

    except Exception as e:
        print("Database connection error:", e)

# Run async function
asyncio.run(connect_db())
