# AsyncDataPipeline

## Overview
**AsyncDataPipeline** is a high-performance, scalable FastAPI-based application designed for processing multiple files asynchronously. It uses the **Producer-Consumer** pattern with **Celery workers** to efficiently handle large batches of data and persist them into an **PostgreSQL database** and archive the data to **S3 Glacier** at the end of each financial year.

## Features
- **Asynchronous File Processing** – Handles multiple files concurrently.
- **Producer-Consumer Architecture** – Ensures optimal load distribution.
- **Celery-based Task Execution** – For efficient background processing.
- **Oracle Database Integration** – Reliable data persistence.
- **Docker & Kubernetes Support** – Easy deployment in cloud-native environments.
- **Configurable Retry Mechanism** – Automatic reprocessing of failed tasks.
- **Logging & Monitoring** – Integrated logging for debugging and performance monitoring.

## Architecture
1. **FastAPI Endpoint**: Accepts file uploads and pushes tasks to a Celery queue.
2. **Celery Producer**: Queues tasks for batch processing.
3. **Celery Workers (Consumers)**: Process files asynchronously and insert data into PostgreSQL.
4. **PostgreSQL Database**: Stores the processed data.
5. **Mongodb (Broker)**: Handles message queueing.
6. **Flower Dashboard** (Optional): Monitors Celery tasks.
7. **Email Notification** (Optional): Notify permanently failed Celery tasks.

```plaintext
┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌────────────────┐
│    Client    │ ---> │   FastAPI    │ ---> │   Mongodb    │ ---> │   Celery     │ ---> │PostgreSQL DB │ ---> │   S3 Glacier   │ 
│   (Request)  │      │  (Producer)  │      │   (Queue)    │      │  (Workers)   │      │   (Storage)  │      │ (Cold Storage) │
└──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘      └────────────────┘      
```

## Installation
### Prerequisites
- Python 3.9+
- PostgreSQL
- Mongodb (as Celery broker)
- Docker & Docker Compose
- Kubernetes (optional)

### Setup
Clone the repository:
```bash
git clone https://github.com/ritesh-tiwary/async-data-pipeline.git
cd async-data-pipeline
```

Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Set environment variables:
```bash
export DATABASE_URL="oracle+cx_oracle://user:password@host:port/dbname"
export CELERY_BROKER_URL="mongodb://user:password@mongodb:27017/celery_broker"
```

Alternatively, create a `.env` file:
```
DATABASE_URL=oracle+cx_oracle://user:password@host:port/dbname
CELERY_BROKER_URL=mongodb://user:password@mongodb:27017/celery_broker
```

## Running the Application
Start Redis (if not running already):
```bash
redis-server
```

Start the FastAPI application:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Start Celery workers:
```bash
celery --app app.worker.celery worker --loglevel=info
```

To monitor Celery tasks using Flower:
```bash
celery --app app.worker.celery flower
```

## API Endpoints
### 1. Upload a File
**POST** `/uploadfiles`
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/uploadfiles/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@file1.txt' \
  -F 'files=@file2.txt'
```

### 2. Check Task Status
**GET** `/task/{task_id}`

Response:
```json
{
  "task_id": "12345",
  "status": "Processing"
}
```

## Deployment
### Docker Setup
Build and run using Docker:
```bash
docker-compose up --build
```

### Kubernetes Deployment
Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

## Monitoring & Logging
- **Celery Logs**: `logs/celery.log`
- **FastAPI Logs**: `logs/api.log`
- **Flower Dashboard**: Accessible at `http://localhost:5555`

## Future Enhancements
- Add support for more file formats (JSON, XML, Parquet).
- Implement automatic scaling of Celery workers.
- Improve error handling and retries.
- Add WebSocket support for real-time progress updates.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## License
MIT License. See `LICENSE` for details.
