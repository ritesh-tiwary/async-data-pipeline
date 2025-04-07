FROM python:3.10

WORKDIR /app

COPY ./app /app

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV MONGO_URI="mongodb://admin:secret@mongodb:27017"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]