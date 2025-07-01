#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Waiting for dependent services to be ready..."
sleep 15  # Sleep for 5 seconds (adjust as needed)

echo "Applying database migrations..."
poetry run python src/manage.py migrate

echo "Collecting static files..."
poetry run python src/manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
poetry run gunicorn src.wsgi:application --bind 0.0.0.0:8000
