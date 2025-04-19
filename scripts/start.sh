python -m uvicorn app:app --host 0.0.0.0 --port 8001 &
FASTAPI_PID=$!

echo "FastAPI started with PID $FASTAPI_PID"

# Start Celery worker
python -m celery --app app.worker.celery worker --loglevel=info &
CELERY_PID=$!

echo "Celery worker started with PID $CELERY_PID"

# Trap Ctrl+C and kill both processes
trap "kill $FASTAPI_PID $CELERY_PID" EXIT

# Keep the script running
wait
