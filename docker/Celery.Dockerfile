FROM python:3.12

WORKDIR /worker

COPY ./app /worker/app

COPY requirements.txt /worker/

RUN mkdir -p /worker/uploads

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN adduser celery_worker

CMD ["celery", "--app", "app.worker.celery", "worker", "--loglevel", "info", "--uid", "celery_worker", "--concurrency", "4", "--queues", "tasks-queue"]
