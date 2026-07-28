import json
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
POSTGRES_IMAGE = (
    "postgres:16.13-bookworm@"
    "sha256:472efd9a66f2b2f1a5aeb18b28de74332e6ef88c2b93a1a5d812fb6db67a5f60"
)
COMPOSE_VARIABLES = {
    "DATABASE_CONNECT_TIMEOUT",
    "DATABASE_NAME",
    "DATABASE_PASSWORD",
    "DATABASE_PORT",
    "DATABASE_STARTUP_MAX_ATTEMPTS",
    "DATABASE_STARTUP_RETRY_DELAY",
    "DATABASE_USER",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_DEBUG",
    "DJANGO_SECRET_KEY",
    "POSTGRES_BIND_HOST",
    "WEB_BIND_HOST",
    "WEB_HOST_PORT",
}


def compose_environment(environment: dict[str, str]) -> dict[str, str]:
    process_environment = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("COMPOSE_") and name not in COMPOSE_VARIABLES
    }
    process_environment.update(environment)
    return process_environment


def compose_config(environment: dict[str, str]) -> dict[str, object]:
    process_environment = compose_environment(
        {"COMPOSE_DISABLE_ENV_FILE": "1", **environment}
    )
    result = subprocess.run(
        [
            "docker",
            "compose",
            "--file",
            str(PROJECT_ROOT / "compose.yaml"),
            "config",
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        env=process_environment,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_postgresql_binding_cannot_be_widened_by_environment() -> None:
    config = compose_config({"POSTGRES_BIND_HOST": "0.0.0.0"})
    postgres = config["services"]["postgres"]

    assert [port["host_ip"] for port in postgres["ports"]] == ["127.0.0.1"]


def test_web_binding_cannot_be_widened_by_environment() -> None:
    config = compose_config({"WEB_BIND_HOST": "0.0.0.0"})
    web = config["services"]["web"]

    assert [port["host_ip"] for port in web["ports"]] == ["127.0.0.1"]


def test_database_port_selects_only_the_host_publication() -> None:
    config = compose_config({"DATABASE_PORT": "55432"})
    postgres = config["services"]["postgres"]
    web = config["services"]["web"]

    assert postgres["ports"][0]["published"] == "55432"
    assert web["environment"]["DATABASE_PORT"] == "5432"


def test_compose_automatically_loads_an_ignored_env_file(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("DATABASE_PORT=55432\n")
    result = subprocess.run(
        [
            "docker",
            "compose",
            "--project-directory",
            str(tmp_path),
            "--file",
            str(PROJECT_ROOT / "compose.yaml"),
            "config",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        env=compose_environment({}),
        capture_output=True,
        text=True,
        check=True,
    )
    config = json.loads(result.stdout)

    assert config["services"]["postgres"]["ports"][0]["published"] == "55432"


def test_compose_preserves_postgresql_startup_contract() -> None:
    config = compose_config({})
    postgres = config["services"]["postgres"]
    web = config["services"]["web"]

    assert postgres["image"] == POSTGRES_IMAGE
    assert postgres["environment"]["POSTGRES_INITDB_ARGS"] == (
        "--auth-host=scram-sha-256 --auth-local=scram-sha-256"
    )
    assert postgres["healthcheck"]["test"] == [
        "CMD-SHELL",
        'pg_isready --username "$${POSTGRES_USER}" --dbname "$${POSTGRES_DB}"',
    ]
    assert [
        {
            "type": volume["type"],
            "source": volume["source"],
            "target": volume["target"],
        }
        for volume in postgres["volumes"]
    ] == [
        {
            "type": "volume",
            "source": "postgres_data",
            "target": "/var/lib/postgresql/data",
        }
    ]
    assert web["depends_on"]["postgres"]["condition"] == "service_healthy"


def test_compose_services_share_clean_checkout_database_defaults() -> None:
    config = compose_config({})
    postgres_environment = config["services"]["postgres"]["environment"]
    web_environment = config["services"]["web"]["environment"]

    assert web_environment["DATABASE_NAME"] == postgres_environment["POSTGRES_DB"]
    assert web_environment["DATABASE_USER"] == postgres_environment["POSTGRES_USER"]
    assert (
        web_environment["DATABASE_PASSWORD"]
        == postgres_environment["POSTGRES_PASSWORD"]
    )
    assert web_environment["DJANGO_SECRET_KEY"] == (
        "development-only-appointment-booking-secret"
    )


def test_blank_startup_controls_reach_entrypoint_validation() -> None:
    config = compose_config(
        {
            "DATABASE_STARTUP_MAX_ATTEMPTS": "",
            "DATABASE_STARTUP_RETRY_DELAY": "",
        }
    )
    web_environment = config["services"]["web"]["environment"]

    assert web_environment["DATABASE_STARTUP_MAX_ATTEMPTS"] == ""
    assert web_environment["DATABASE_STARTUP_RETRY_DELAY"] == ""
