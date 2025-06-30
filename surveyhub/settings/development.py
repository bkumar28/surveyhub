from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Use console email backend for local testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development-specific CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Optionally add internal IPs for debug toolbar, if used
INTERNAL_IPS = ['127.0.0.1']

# Optional: Add django-debug-toolbar or other dev tools
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
