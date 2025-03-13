import asyncio
import aioodbc
import uvloop
import random
import string
import logging
import json

# Configure logging
logging.basicConfig(filename="db_inserts.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

DSN = "DRIVER=FreeTDS;SERVER=sybase_server;PORT=5000;UID=your_username;PWD=your_password;DATABASE=your_database"

DLQ_FILE = "failed_inserts.json"  # Optional: Store failed records in a JSON file

async def create_db_pool():
    """Create a connection pool for Sybase."""
    return await aioodbc.create_pool(dsn=DSN, minsize=1, maxsize=5)

async def producer(queue, num_items):
    """Produces fake user data and adds it to the queue."""
    for _ in range(num_items):
        name = ''.join(random.choices(string.ascii_letters, k=6))
        age = random.randint(18, 60)
        await queue.put((name, age))
        logging.info(f"Produced: {name}, {age}")

    # Signal consumers to stop
    for _ in range(3):  # Assuming 3 consumers
        await queue.put(None)

async def insert_with_retry(cursor, query, params, retries=3):
    """Tries inserting data with retries. If all fail, sends to DLQ."""
    for attempt in range(1, retries + 1):
        try:
            await cursor.execute(query, params)
            logging.info(f"Inserted: {params}")
            return True
        except Exception as e:
            logging.warning(f"Insert attempt {attempt} failed for {params}: {e}")
            await asyncio.sleep(2**attempt)  # Exponential backoff

    logging.error(f"Failed to insert after {retries} attempts: {params}")
    await send_to_dlq(cursor, params, str(e))
    return False

async def send_to_dlq(cursor, params, error_message):
    """Inserts failed record into the DLQ table in Sybase."""
    try:
        await cursor.execute("INSERT INTO failed_inserts (name, age, error_message) VALUES (?, ?, ?)", 
                             (params[0], params[1], error_message))
        logging.info(f"Sent to DLQ: {params} - Error: {error_message}")
    except Exception as e:
        logging.error(f"Failed to insert into DLQ: {params} - Error: {e}")
        await save_dlq_to_file(params, error_message)  # Fallback to JSON file

async def save_dlq_to_file(params, error_message):
    """Saves failed records to a JSON file as a backup."""
    failed_record = {"name": params[0], "age": params[1], "error": error_message}
    try:
        with open(DLQ_FILE, "a") as f:
            f.write(json.dumps(failed_record) + "\n")
        logging.info(f"Saved to DLQ file: {failed_record}")
    except Exception as e:
        logging.error(f"Failed to save to DLQ file: {e}")

async def consumer(queue, pool, consumer_id):
    """Consumes user data from the queue and inserts it into Sybase with DLQ handling."""
    batch_size = 5
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            batch = []
            while True:
                data = await queue.get()
                if data is None:
                    if batch:
                        await insert_batch_with_retry(cursor, batch)
                    logging.info(f"Consumer-{consumer_id} exiting")
                    break

                batch.append(data)
                if len(batch) >= batch_size:
                    await insert_batch_with_retry(cursor, batch)
                    batch.clear()

                queue.task_done()

async def insert_batch_with_retry(cursor, batch, retries=3):
    """Tries batch inserting data with retries. If all fail, moves to DLQ."""
    query = "INSERT INTO users (name, age) VALUES (?, ?)"
    for attempt in range(1, retries + 1):
        try:
            await cursor.executemany(query, batch)
            logging.info(f"Batch inserted {len(batch)} records")
            return True
        except Exception as e:
            logging.warning(f"Batch insert attempt {attempt} failed: {e}")
            await asyncio.sleep(2**attempt)

    logging.error(f"Failed to insert batch after {retries} attempts: {batch}")
    for record in batch:
        await send_to_dlq(cursor, record, str(e))
    return False

async def main():
    queue = asyncio.Queue()
    pool = await create_db_pool()

    num_items = 20  # Number of records to insert

    producer_task = asyncio.create_task(producer(queue, num_items))
    consumers = [asyncio.create_task(consumer(queue, pool, i)) for i in range(3)]  # 3 consumers

    await producer_task  # Ensure all data is produced
    await queue.join()   # Wait until all tasks are processed
    await asyncio.gather(*consumers)  # Ensure all consumers exit

    await pool.close()

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(main())  # Run with uvloop