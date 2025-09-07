# Base image with Python 3.11 (Debian Bullseye variant)
FROM python:3.11-slim-bullseye

# Update system packages to close security vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Set maintainer and description labels
LABEL maintainer="Margarethe-Techstarter"
LABEL description="GitHub Action to test local LLMs via LM Studio and measure response time"
LABEL version="1.0"
# Set the working directory inside the container
WORKDIR /app

# Copy all local files to the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define the entry point for the Action
ENTRYPOINT ["python3", "main.py"]