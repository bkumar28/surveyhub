#!/bin/bash

# File: generate_env.sh

ENV_FILE=".env"

# Create .env-example file with environment variables
cat > "$ENV_FILE" << 'EOF'

# Environment variables for Django development
# This file is used to set environment variables for local development.
DEBUG=True

# Secret key for Django (change this in production)
# Use a strong, unique key in production
# This is just a placeholder; you should generate your own.
# You can use a tool like `django-admin startproject` to generate a secure key.
# For local development, you can use a simple key.
# In production, use a more secure key.
# Example: `django-admin startproject --settings=settings.production`
# or generate a key using `django.core.management.utils.get_random_secret_key()`
# or use a secure key generator.
# Note: Do not use this key in production; it's just for local development.
SECRET_KEY=n1@4!n5wuvx&=nl7n3%@8jvzbsq68j2bkh=7!pnnk=$he1m-%9

# Django settings module
DJANGO_SETTINGS_MODULE=settings.development

# Allowed hosts (adjust as needed)
# For local development, you can use localhost and
ALLOWED_HOSTS=localhost,127.0.0.1,web

# CORS settings
# Allow all origins for local development
# In production, you should restrict this to specific domains.
CORS_ALLOW_ALL_ORIGINS=True

# Database (inside Docker: use service name instead of localhost)
DB_NAME=db_test
DB_USER=db_user
DB_PASSWORD=db_pass
DB_HOST=db
DB_PORT=5432

# Redis (inside Docker)
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# Email settings
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_TIMEOUT=5
EMAIL_SSL_CERTFILE=""
EMAIL_SSL_KEYFILE=""
EMAIL_SSL_KEY_PASSWORD=""
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER=test@gmail.com
EMAIL_HOST_PASSWORD=test_pass
EOF

echo "$ENV_FILE file generated successfully!"
