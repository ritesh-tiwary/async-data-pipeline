# Use the official Flower image as a base
FROM mher/flower:latest

# Optional: expose the port
EXPOSE 5555

CMD ["celery", "--broker", "pyamqp://guest@rabbitmq_broker:5672//", "flower"]
