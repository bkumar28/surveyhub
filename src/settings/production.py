from .base import *

DEBUG = False


# Production Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Security settings for HTTPS (important in production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging level override
LOGGING["root"]["level"] = "WARNING"

# Validate critical environment variables
db_settings = DATABASES.get("default", {})
if not db_settings.get("NAME"):
    raise ValueError("Missing DB_NAME in environment variables.")
if not db_settings.get("USER"):
    raise ValueError("Missing DB_USER in environment variables.")
if not db_settings.get("PASSWORD"):
    raise ValueError("Missing DB_PASSWORD in environment variables.")
if not db_settings.get("HOST"):
    raise ValueError("Missing DB_HOST in environment variables.")
if not db_settings.get("PORT"):
    raise ValueError("Missing DB_PORT in environment variables.")

if not REDIS_HOST or not REDIS_PORT:
    raise ValueError("Missing REDIS_HOST or REDIS_PORT in environment variables.")

if not CELERY_BROKER_URL:
    raise ValueError("Missing CELERY_BROKER_URL in environment variables.")
