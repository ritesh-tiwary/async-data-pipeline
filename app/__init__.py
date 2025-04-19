import asyncio
import aiofiles
from typing import List
from fastapi import FastAPI, UploadFile, File

from app.worker import celery
from app.worker.tasks import add_with_retry, save_data
from celery.result import AsyncResult


app = FastAPI()

@app.get('/')
def root():
    return {"message": "Application is running"}

# Producer function to read file content and put it in the queue
async def producer(files: List[UploadFile], file_queue: asyncio.Queue):
    try:
        for file in files:
            print(f"Processing file: {file.filename}")
            async with aiofiles.open(file.filename, 'rb') as f:
                content = await f.read()
            await file_queue.put((file.filename, content.decode('utf-8')))
    finally:
        # Put sentinel values to signal the consumers to exit
        for _ in range(len(files)):
            await file_queue.put(None)

# Consumer function to save data to the database
async def consumer(file_queue: asyncio.Queue):
    while True:
        item = await file_queue.get()
        if item is None:
            # Sentinel value received, exit the consumer
            file_queue.task_done()
            break
        filename, content = item
        print(f"Pushing file: {filename} ({len(content)} bytes) to celery")
        save_data.delay(filename, content)
        file_queue.task_done()

@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    # Create a queue
    file_queue = asyncio.Queue()

    # Start the producer
    producer_task = asyncio.create_task(producer(files, file_queue))
    
    # Start consumers based on the number of files
    consumer_tasks = [asyncio.create_task(consumer(file_queue)) for _ in range(len(files))]
    
    # Wait for the producer to finish
    await producer_task
    
    # Wait for the queue to be fully processed
    await file_queue.join()
    
    # Wait for all consumer tasks to finish
    await asyncio.gather(*consumer_tasks, return_exceptions=True)
    
    return {"message": "Files processed successfully"}

@app.get("/add/{x}/{y}")
def add_numbers(x: int, y: int):
    task = add_with_retry.delay(x, y)
    return {"task_id": task.id}

@app.get("/task/{task_id}")
def get_result(task_id: str):
    result = AsyncResult(task_id, app=celery)
    if result.failed():
        return {"task_id": task_id, "status": "Failed"}
    elif result.ready():
        return {"task_id": task_id, "result": result.result}
    return {"task_id": task_id, "status": "Processing"}