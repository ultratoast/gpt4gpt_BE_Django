from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", False)
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

# Comma-separated hosts, e.g. "api.exampledomain.com,localhost"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost").split(",") if h.strip()]

INSTALLED_APPS = [
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "api.middleware.BearerTokenAuthMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CORS: only allow your frontend origin
CORS_ALLOWED_ORIGINS = [
    "https://ultratoast.link",
    "http://localhost"
]

# Optional but often helpful when using Authorization header
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# For simple JSON APIs
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = False
