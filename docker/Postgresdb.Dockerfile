FROM postgres:16

ENV POSTGRES_DB=tasks
ENV POSTGRES_USER=dbuser
ENV POSTGRES_PASSWORD=dbpassword

# Copy initialization SQL script if needed
# COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
