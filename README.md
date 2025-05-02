# AsyncDataPipeline

## Overview
**AsyncDataPipeline** is a high-performance, scalable FastAPI-based application designed for processing multiple files asynchronously. It uses the **Producer-Consumer** pattern with **Celery workers** to efficiently handle large batches of data and persist them into an **PostgreSQL database** and archive the data to **S3 Glacier** at the end of each financial year.

## Features
- **Asynchronous File Processing** – Handles multiple files concurrently.
- **Producer-Consumer Architecture** – Ensures optimal load distribution.
- **Celery-based Task Execution** – For efficient background processing.
- **PostgreSQL Database Integration** – Reliable data persistence.
- **Docker & Kubernetes Support** – Easy deployment in cloud-native environments.
- **Configurable Retry Mechanism** – Automatic reprocessing of failed tasks.
- **Logging & Monitoring** – Integrated logging for debugging and performance monitoring.

## Architecture
1. **FastAPI Endpoint**: Accepts file uploads and pushes tasks to a Celery queue.
2. **Celery Producer**: Queues tasks for batch processing.
3. **Celery Workers (Consumers)**: Process files asynchronously and insert data into PostgreSQL.
4. **PostgreSQL Database**: Stores the processed data.
5. **RabbitMQ (Broker)**: Handles message queueing.
6. **Mongodb (Backend)**: Store result message.
7. **Flower Dashboard** (Optional): Monitors Celery tasks.
8. **Email Notification** (Optional): Notify permanently failed Celery tasks.

```plaintext
┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌────────────────┐      ┌────────────────┐
│    Client    │ ---> │   FastAPI    │ ---> │   RabbitMQ   │ ---> │   Celery     │ ---> │   MongoDB    │ ---> │ PostgreSQL DB  │ ---> │   S3 Glacier   │ 
│   (Request)  │      │  (Producer)  │      │   (Queue)    │      │  (Workers)   │      │  (Backend)   │      │   (Storage)    │      │ (Cold Storage) │
└──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘      └────────────────┘      └────────────────┘      
```

## Installation
### Prerequisites
- Python 3.12+
- PostgreSQL
- RabbitMQ (as Celery broker)
- Mongodb (as Celery backend)
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
export CELERY_BROKER_URL="pyamqp://guest@localhost:5672//"
export CELERY_RESULT_BACKEND="mongodb://user:password@localhost:27017/celery_results"
```

Alternatively, create a `.env` file:
```
CELERY_BROKER_URL="pyamqp://guest@localhost:5672//"
CELERY_RESULT_BACKEND="mongodb://user:password@localhost:27017/celery_results"
```

## Running the Application
Start RabbitMQ (if not running already):
```bash
rabbitmq-server
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
  "task_id": "73027031-4d2a-4bd7-bc61-68c1b0bf3822",
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
- Add gRPC support for backend service integration.
- Add WebSocket support for real-time progress updates.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a pull request.

## License
MIT License. See `LICENSE` for details.
