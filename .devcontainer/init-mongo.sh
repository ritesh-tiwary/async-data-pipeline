#!/bin/bash
echo "Waiting for MongoDB to start..."
sleep 5  # Give MongoDB some time to start

echo "Initializing database..."
mongosh --eval "
  db.getSiblingDB('admin').createUser({
    user: '$MONGO_INITDB_ROOT_USERNAME',
    pwd: '$MONGO_INITDB_ROOT_PASSWORD',
    roles: [{ role: 'root', db: 'admin' }]
  });
  db.getSiblingDB('$MONGO_INITDB_DATABASE').createCollection('test_collection');
"

echo "MongoDB initialization complete."
