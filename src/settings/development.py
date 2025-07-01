from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Use console email backend for local testing
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Optional: Add django-debug-toolbar or other dev tools
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
