import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VALID_PRODUCTION_ENV = {
    "DJANGO_ENVIRONMENT": "production",
    "DJANGO_SECRET_KEY": "test-only-production-secret-key-that-is-not-reusable",
    "DJANGO_DEBUG": "false",
    "DJANGO_ALLOWED_HOSTS": "appointments.example.test",
    "DATABASE_NAME": "test_production_database",
    "DATABASE_USER": "test_production_user",
    "DATABASE_PASSWORD": "test-only-production-database-password",
    "DATABASE_HOST": "database.example.test",
    "DATABASE_PORT": "5432",
}
PRODUCTION_REQUIRED_SETTINGS = [
    "DJANGO_SECRET_KEY",
    "DJANGO_ALLOWED_HOSTS",
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "DATABASE_HOST",
    "DATABASE_PORT",
]


def import_settings(
    environment: dict[str, str],
    expression: str = "print('imported')",
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", f"import config.settings as settings; {expression}"],
        cwd=PROJECT_ROOT,
        env={"PYTHONPATH": str(PROJECT_ROOT), **environment},
        capture_output=True,
        text=True,
        check=False,
    )


def test_development_database_host_is_environment_selected() -> None:
    result = import_settings(
        {
            "DJANGO_ENVIRONMENT": "development",
            "DATABASE_HOST": "postgres",
        },
        "print(settings.DATABASES['default']['HOST'])",
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "postgres"


def test_development_database_port_is_environment_selected() -> None:
    result = import_settings(
        {
            "DJANGO_ENVIRONMENT": "development",
            "DATABASE_PORT": "55432",
        },
        "print(settings.DATABASES['default']['PORT'])",
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "55432"


def test_production_settings_accept_external_values() -> None:
    result = import_settings(VALID_PRODUCTION_ENV)

    assert result.returncode == 0
    assert result.stdout.strip() == "imported"


def test_production_settings_reject_missing_values() -> None:
    result = import_settings({"DJANGO_ENVIRONMENT": "production"})

    assert result.returncode != 0
    assert "Production configuration requires non-development values" in result.stderr
    assert "DJANGO_SECRET_KEY" in result.stderr
    assert "DATABASE_PASSWORD" in result.stderr


@pytest.mark.parametrize("name", PRODUCTION_REQUIRED_SETTINGS)
def test_production_settings_reject_each_omitted_required_value(name: str) -> None:
    environment = {**VALID_PRODUCTION_ENV}
    del environment[name]

    result = import_settings(environment)

    assert result.returncode != 0
    assert name in result.stderr


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("DJANGO_SECRET_KEY", "development-only-appointment-booking-secret"),
        ("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"),
        ("DATABASE_NAME", "appointment_booking_development"),
        ("DATABASE_USER", "appointment_booking_development"),
        (
            "DATABASE_PASSWORD",
            "development-only-appointment-booking-database-password",
        ),
        ("DJANGO_DEBUG", "true"),
    ],
)
def test_production_settings_reject_development_values(
    name: str,
    value: str,
) -> None:
    result = import_settings({**VALID_PRODUCTION_ENV, name: value})

    assert result.returncode != 0
    assert name in result.stderr


def test_settings_reject_unknown_environment() -> None:
    result = import_settings(
        {**os.environ, "DJANGO_ENVIRONMENT": "staging"},
    )

    assert result.returncode != 0
    assert "DJANGO_ENVIRONMENT must be development or production" in result.stderr


@pytest.mark.parametrize("name", ["DJANGO_SECRET_KEY", "DATABASE_PASSWORD"])
def test_production_settings_reject_whitespace_only_credentials(name: str) -> None:
    result = import_settings({**VALID_PRODUCTION_ENV, name: "   "})

    assert result.returncode != 0
    assert name in result.stderr


def test_settings_reject_a_test_database_matching_the_development_database() -> None:
    result = import_settings(
        {
            "DATABASE_NAME": "shared_database",
            "DATABASE_TEST_NAME": "shared_database",
        }
    )

    assert result.returncode != 0
    assert "DATABASE_TEST_NAME must differ from DATABASE_NAME" in result.stderr
