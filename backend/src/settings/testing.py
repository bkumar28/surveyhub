# Disable DRF throttling for tests
import sys

from .base import *

if "pytest" in sys.modules or "test" in sys.argv[0]:
    REST_FRAMEWORK = globals().get("REST_FRAMEWORK", {})
    REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}


ALLOWED_HOSTS = ["*"]


SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True if not DEBUG else False

# Optional: Add django-debug-toolbar or other dev tools
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
