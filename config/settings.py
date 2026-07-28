import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

_DEVELOPMENT_DEFAULTS = {
    "DJANGO_SECRET_KEY": "development-only-appointment-booking-secret",
    "DATABASE_NAME": "appointment_booking_development",
    "DATABASE_USER": "appointment_booking_development",
    "DATABASE_PASSWORD": "development-only-appointment-booking-database-password",
}

ENVIRONMENT = os.environ.get("DJANGO_ENVIRONMENT", "development").lower()
if ENVIRONMENT not in {"development", "production"}:
    raise ImproperlyConfigured("DJANGO_ENVIRONMENT must be development or production")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", _DEVELOPMENT_DEFAULTS["DJANGO_SECRET_KEY"]
)
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

_database_name = os.environ.get(
    "DATABASE_NAME", _DEVELOPMENT_DEFAULTS["DATABASE_NAME"]
).strip()
_database_test_name = os.environ.get(
    "DATABASE_TEST_NAME", "appointment_booking_test"
).strip()
if not _database_name or not _database_test_name:
    raise ImproperlyConfigured("Database names must not be empty")
if _database_name == _database_test_name:
    raise ImproperlyConfigured("DATABASE_TEST_NAME must differ from DATABASE_NAME")

try:
    _database_connect_timeout = int(os.environ.get("DATABASE_CONNECT_TIMEOUT", "2"))
except ValueError as error:
    raise ImproperlyConfigured(
        "DATABASE_CONNECT_TIMEOUT must be a positive integer"
    ) from error
if _database_connect_timeout <= 0:
    raise ImproperlyConfigured("DATABASE_CONNECT_TIMEOUT must be a positive integer")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _database_name,
        "USER": os.environ.get("DATABASE_USER", _DEVELOPMENT_DEFAULTS["DATABASE_USER"]),
        "PASSWORD": os.environ.get(
            "DATABASE_PASSWORD", _DEVELOPMENT_DEFAULTS["DATABASE_PASSWORD"]
        ),
        "HOST": os.environ.get("DATABASE_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
        "OPTIONS": {"connect_timeout": _database_connect_timeout},
        "TEST": {"NAME": _database_test_name},
    }
}

if ENVIRONMENT == "production":
    required_settings = {
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "DATABASE_NAME",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
        "DATABASE_HOST",
        "DATABASE_PORT",
    }
    invalid_settings = {
        name for name in required_settings if not os.environ.get(name, "").strip()
    }
    invalid_settings.update(
        name
        for name, development_value in _DEVELOPMENT_DEFAULTS.items()
        if os.environ.get(name) == development_value
    )
    if not os.environ.get("DJANGO_ALLOWED_HOSTS") or set(ALLOWED_HOSTS) <= {
        "localhost",
        "127.0.0.1",
    }:
        invalid_settings.add("DJANGO_ALLOWED_HOSTS")
    if DEBUG:
        invalid_settings.add("DJANGO_DEBUG")
    if invalid_settings:
        names = ", ".join(sorted(invalid_settings))
        raise ImproperlyConfigured(
            f"Production configuration requires non-development values for: {names}"
        )

INSTALLED_APPS = ["apps.common"]
MIDDLEWARE = []
ROOT_URLCONF = "config.urls"
TEMPLATES = []

USE_TZ = True
