#!/bin/bash

# File: generate_env.sh

ENV_FILE=".env"

# Create .env-example file with environment variables
cat > "$ENV_FILE" << 'EOF'
# General Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=settings.development
ALLOWED_HOSTS=localhost,127.0.0.1,web

# Database (inside Docker: use service name instead of localhost)
DATABASE_URL=postgresql://user:password@db:5432/surveyhub

# Redis (inside Docker)
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EOF

echo "$ENV_FILE file generated successfully!"
