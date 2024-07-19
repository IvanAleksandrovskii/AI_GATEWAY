# Use a slim Python runtime as a parent image
FROM python:3.12-slim

# Additional fixing instalation for Postgres, needed to work with db with linux system
RUN apt-get update && apt-get install -y libpq-dev
# Istalling netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Create a working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Copy and install requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure start.sh has executable permissions
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000