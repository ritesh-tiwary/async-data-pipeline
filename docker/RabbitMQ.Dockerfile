# Use the official RabbitMQ image
FROM rabbitmq:3-management

# Expose the default RabbitMQ and management plugin ports
EXPOSE 5672 15672

# Set environment variables for default user and password
ENV RABBITMQ_DEFAULT_USER=guest
ENV RABBITMQ_DEFAULT_PASS=guest

# Copy custom configuration file
# COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# Start RabbitMQ server
CMD ["rabbitmq-server"]