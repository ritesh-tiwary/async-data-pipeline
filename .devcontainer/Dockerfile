FROM ubuntu:20.04

# Install MongoDB
RUN apt-get update && apt-get install -y gnupg curl && \
    curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list && \
    apt-get update && apt-get install -y mongodb-org

# Expose MongoDB port
EXPOSE 27017

# Create data directory
RUN mkdir -p /data/db

# Start MongoDB
ENTRYPOINT ["mongod", "--bind_ip_all"]