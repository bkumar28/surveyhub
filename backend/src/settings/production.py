from .base import *

DEBUG = False


# Production Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


# Security settings for HTTPS (important in production)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HTTPS settings
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


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

# CORS settings for production (restrictive)
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="").split(",")

# Logging configuration for production
LOGGING["handlers"]["file"]["filename"] = "/var/log/django/django.log"
LOGGING["root"]["level"] = "WARNING"
LOGGING["loggers"]["django"]["level"] = "WARNING"
