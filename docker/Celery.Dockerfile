FROM python:3.12

WORKDIR /worker

COPY ./app /worker/app

COPY requirements.txt /worker/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN adduser celery_worker

CMD ["celery", "--app", "app.worker.celery", "worker", "--loglevel", "info", "--uid", "celery_worker", "--concurrency", "4", "--queues", "db-tasks-queue,file-tasks-queue"]
