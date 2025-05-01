# Use the official Flower image as a base
FROM mher/flower:latest

# Set environment variable to enable unauthenticated API
ENV FLOWER_UNAUTHENTICATED_API=true

# Optional: expose the port
EXPOSE 5555

CMD ["celery", "--broker", "pyamqp://guest@rabbitmq_broker:5672//", "flower"]
