from .base import *

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='yourdomain.com').split(',')

# Production Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# CORS setup for live frontend
CORS_ALLOWED_ORIGINS = [
    "https://your-production-frontend.com",
]

# Security settings for HTTPS (important in production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging level override
LOGGING['root']['level'] = 'WARNING'
