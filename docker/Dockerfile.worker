FROM python:3.10

WORKDIR /worker

COPY ./app /worker

COPY requirements.txt /worker/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV MONGO_URI="mongodb://admin:secret@mongodb:27017"

CMD ["celery", "--app", "app.worker.celery", "worker", "--loglevel=info"]