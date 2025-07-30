FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Configure poetry: Don't create a virtual environment
RUN poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs

# Collect static files (will run when container starts)
# RUN python manage.py collectstatic --noinput

# Copy entrypoint and wait-for-it scripts
COPY ./scripts/start-dev.sh /start-dev.sh
RUN chmod +x /start-dev.sh

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/start-dev.sh"]
