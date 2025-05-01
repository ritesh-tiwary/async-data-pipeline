FROM python:3.12

WORKDIR /worker

COPY ./app /worker/app

COPY requirements.txt /worker/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN addgroup --gid 1001 appuser

RUN adduser --uid 1001 --gid 1001 appuser

CMD ["celery", "--app", "app.worker.celery", "worker", "--loglevel", "info", "--uid", "appuser", "--concurrency", "4", "--queues", "tasks-queue"]
