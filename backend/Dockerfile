# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry and system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean

# Make poetry available in PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Set PYTHONPATH
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Copy dependency declarations
COPY pyproject.toml poetry.lock ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false && \
    poetry config installer.max-workers 1
RUN for i in 1 2 3; do poetry install --no-root && break || sleep 5; done

# Copy source code into /app/src
COPY src/ src/

# Copy docker run server bash
COPY ./scripts/start-dev.sh /app/docker_entrypoint.sh
RUN chmod +x /app/docker_entrypoint.sh

# Expose port
EXPOSE 8000

CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000"]
