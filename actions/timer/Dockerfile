# Base image with Python 3.11 (Debian Bullseye variant)
FROM python:3.11-slim-bullseye


# Set maintainer and description labels
LABEL maintainer="Margarethe-S"
LABEL description="GitHub Action to test local LLMs via LM Studio and measure response time"
LABEL version="1.0"


# Set the working directory inside the container
WORKDIR /app


# Copy files into container
COPY main.py /app/main.py
COPY logger.py /app/logger.py
COPY requirements.txt /app/requirements.txt
COPY prompts /app/prompts


# Set timezone based on build argument (default to UTC if not provided)
ARG TZ=UTC
ENV TZ=${TZ}


# Install dependencies and configure timezone
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y mpg123 tzdata && \
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean


# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Define the entry point for the Action
ENTRYPOINT ["python3", "/app/main.py"]
