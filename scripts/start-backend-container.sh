#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

cd /app/src

echo "Waiting for dependent services to be ready..."
sleep 15

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec poetry run gunicorn wsgi:application --bind 0.0.0.0:8000 --timeout 120
