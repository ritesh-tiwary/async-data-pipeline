import asyncio
import asyncpg
import orjson
from app.core.base import Base


class Databse(Base):
    def __init__(self):
        super().__init__()
        self.DLQ_FILE = "app/logs/failed_inserts.json"  # Optional: Store failed records in a JSON file

    async def save_dlq_to_file(self, query, record, error_message):
        """Saves failed records to a JSON file as a backup."""
        failed_record = {"query": query.strip(), "record": record, "error": error_message}
        try:
            with open(self.DLQ_FILE, "a") as f:
                f.write(orjson.dumps(failed_record).decode("utf-8") + ",")
            self.logger.info(f"Saved to DLQ file: {failed_record}")
        except Exception as e:
            self.logger.error(f"Failed to save to DLQ file: {e}")

    async def send_to_dlq(self, connection, query, record, error_message):
        """Inserts failed record into the DLQ table in Postgres."""
        try:
            await connection.execute("INSERT INTO failed_inserts (query, record, error_message) VALUES ($1, $2, $3)", 
                                (query, record, error_message))
            self.logger.info(f"Sent to DLQ: {record} - Error: {error_message}")
        except Exception as e:
            self.logger.error(f"Failed to insert into DLQ: {record} - Error: {e}")
            await self.save_dlq_to_file(query, record, error_message)  # Fallback to JSON file

    async def insert_batch_with_retry(self, connection, query, batch, batch_id, consumer_id, retries=3):
        """Tries batch inserting data with retries. If all fail, moves to DLQ."""
        for attempt in range(1, retries + 1):
            try:
                await connection.executemany(query, batch)
                self.logger.info(f"Batch-{batch_id} inserted {len(batch)} records")
                return True
            except Exception as e:
                ex = str(e)
                self.logger.error(f"Batch-{batch_id} insert attempt {attempt} failed: {ex}")
                await asyncio.sleep(2**attempt)

        self.logger.error(f"Consumer-{consumer_id} failed to insert Batch-{batch_id} after {retries} attempts")
        for record in batch:
            await self.send_to_dlq(connection, query, str(record), ex)

    async def consumer(self, queue, pool, query, consumer_id, batch_size):
        """Consumes producer data from the queue and inserts it into Postgres with DLQ handling."""
        async with pool.acquire() as conn:
            batch = []
            batch_id = 0
            while True:
                try:
                    data = await queue.get()
                    if data is None:
                        if batch:
                            await self.insert_batch_with_retry(conn, query, batch, batch_id, consumer_id)
                            batch_id += 1
                        self.logger.info(f"Consumer-{consumer_id} exiting")
                        break

                    batch.append(data)
                    if len(batch) >= batch_size:
                        await self.insert_batch_with_retry(conn, query, batch, batch_id, consumer_id)
                        batch_id += 1
                        batch.clear()
                finally:
                    queue.task_done()

    async def producer(self, queue, items, num_consumers):
        """Produces items data and adds it to the queue."""
        for item in items:
            await queue.put(item)
            self.logger.info(f"Produced: {str(item)}")

        # Signal consumers to stop
        for _ in range(num_consumers):
            await queue.put(None)

    async def create_db_pool(self):
        """Create a connection pool for Postgres."""
        return await asyncpg.create_pool(**self.settings.POSTGRES_CONFIG)

    async def insert(self, query, items, num_consumers = 2, batch_size = 2):
        queue = asyncio.Queue()
        pool = await self.create_db_pool()

        try:
            producer_task = asyncio.create_task(self.producer(queue, items, num_consumers))
            consumers = [asyncio.create_task(self.consumer(queue, pool, query, consumer_id, batch_size)) for consumer_id in range(num_consumers)]

            await producer_task                                         # Ensure all data is produced
            await queue.join()                                          # Wait until all tasks are processed
            await asyncio.gather(*consumers, return_exceptions=True)    # Ensure all consumers exit
        finally:
            await pool.close()
