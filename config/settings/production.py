from .base import *
import os

DEBUG = False
# Add your domain(s) or IPs here
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "your-domain.com"]

# Must be provided by env var in production
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Set DJANGO_SECRET_KEY in the environment for production.")

# Minimal hardening (tune for real deployment)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False  # True if you're terminating TLS in prod
