import pika


host='localhost'
port=5672
username='guest'
password='guest'
credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)

try:
    connection = pika.BlockingConnection(parameters)
    if connection.is_open:
        print("Successfully connected to RabbitMQ!")
        connection.close()
except pika.exceptions.AMQPConnectionError as e:
    print(f"Connection failed: {e}")
