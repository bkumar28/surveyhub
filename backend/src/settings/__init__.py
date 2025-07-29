"""
Django settings package.
Automatically loads the appropriate settings module based on environment.
"""

from decouple import config

# Determine which settings module to use
ENVIRONMENT = config("DJANGO_ENVIRONMENT", default="development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "testing":
    from .testing import *
else:
    from .development import *
