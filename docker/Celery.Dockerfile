FROM python:3.12

WORKDIR /worker

COPY ./app /worker/app

COPY requirements.txt /worker/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["celery", "--app", "app.worker.celery", "worker", "--loglevel", "info", "--concurrency", "4", "--queues", "tasks-queue"]
