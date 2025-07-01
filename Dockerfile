# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get clean

# Set working directory
WORKDIR /surveyhub

# Set PYTHONPATH so Django can find your code
ENV PYTHONPATH="/surveyhub:${PYTHONPATH}"

# Copy dependency declarations
COPY pyproject.toml poetry.lock ./

# Disable Poetry virtualenvs and configure max workers
RUN poetry config virtualenvs.create false && \
    poetry config installer.max-workers 1

# Install dependencies with retry logic
RUN for i in 1 2 3; do poetry install --no-root --only main && break || sleep 5; done


# Copy project code: flatten `src/` contents into container root
COPY src/manage.py ./manage.py
COPY src/settings ./settings
COPY src/wsgi.py ./wsgi.py
COPY src/asgi.py ./asgi.py
COPY src/celery.py ./celery.py
COPY src/urls.py ./urls.py
COPY src/__init__.py ./__init__.py

# Copies other apps, modules, etc.
COPY src/ ./

# Expose port for Gunicorn
EXPOSE 8000

# Command to run the app via Gunicorn
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000"]
