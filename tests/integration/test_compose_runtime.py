import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMPOSE_FILE = PROJECT_ROOT / "compose.yaml"
DATABASE_NAME = "appointment_booking_development"
DATABASE_USER = "appointment_booking_development"
DATABASE_PASSWORD = "development-only-appointment-booking-database-password"
DJANGO_SECRET_KEY = "development-only-appointment-booking-secret"
CONFIGURATION_VARIABLES = {
    "DATABASE_CONNECT_TIMEOUT",
    "DATABASE_HOST",
    "DATABASE_NAME",
    "DATABASE_PASSWORD",
    "DATABASE_PORT",
    "DATABASE_STARTUP_MAX_ATTEMPTS",
    "DATABASE_STARTUP_RETRY_DELAY",
    "DATABASE_TEST_NAME",
    "DATABASE_USER",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_DEBUG",
    "DJANGO_ENVIRONMENT",
    "DJANGO_SECRET_KEY",
    "DJANGO_SETTINGS_MODULE",
    "WEB_HOST_PORT",
}


def available_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def isolated_environment() -> dict[str, str]:
    return {
        name: value
        for name, value in os.environ.items()
        if not name.startswith(("COMPOSE_", "PG"))
        and name not in CONFIGURATION_VARIABLES
    }


def run_command(
    command: list[str],
    environment: dict[str, str],
    timeout: int = 240,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=check,
    )


def compose_command(
    project_name: str,
    environment: dict[str, str],
    env_file: Path,
    *arguments: str,
    override_file: Path | None = None,
    timeout: int = 240,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    command = [
        "docker",
        "compose",
        "--env-file",
        str(env_file),
        "--file",
        str(COMPOSE_FILE),
    ]
    if override_file is not None:
        command.extend(["--file", str(override_file)])
    command.extend(["--project-name", project_name, *arguments])
    return run_command(command, environment, timeout=timeout, check=check)


def connect(port: int, password: str = DATABASE_PASSWORD) -> psycopg.Connection:
    return psycopg.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=password,
        host="127.0.0.1",
        port=port,
        connect_timeout=4,
    )


def database_fingerprint(port: int) -> tuple[str, int, int, str, str, str, bool]:
    with connect(port) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT current_database(),
                   (SELECT system_identifier FROM pg_control_system()),
                   (SELECT count(*) FROM pg_hba_file_rules
                    WHERE auth_method = 'trust'),
                   current_setting('password_encryption'),
                   to_regclass('public.django_migrations')::text,
                   to_regclass('public.django_content_type')::text,
                   (SELECT rolpassword LIKE 'SCRAM-SHA-256$%'
                    FROM pg_authid WHERE rolname = current_user)
            """
        )
        result = cursor.fetchone()

    assert result is not None
    return result


def create_sentinel(port: int) -> None:
    with connect(port) as connection, connection.cursor() as cursor:
        cursor.execute("CREATE TABLE m1_t2_runtime_sentinel (value text NOT NULL)")
        cursor.execute(
            "INSERT INTO m1_t2_runtime_sentinel (value) VALUES ('preserved')"
        )


def sentinel_value(port: int) -> str:
    with connect(port) as connection, connection.cursor() as cursor:
        cursor.execute("SELECT value FROM m1_t2_runtime_sentinel")
        result = cursor.fetchone()

    assert result is not None
    return result[0]


def inspect_container(
    container_id: str,
    environment: dict[str, str],
) -> dict[str, object]:
    return json.loads(
        run_command(["docker", "inspect", container_id], environment).stdout
    )[0]


def volume_name(container_id: str, environment: dict[str, str]) -> str:
    inspection = inspect_container(container_id, environment)
    return next(
        mount["Name"]
        for mount in inspection["Mounts"]
        if mount["Destination"] == "/var/lib/postgresql/data"
        and mount["Type"] == "volume"
    )


def assert_loopback_publication(
    container_id: str,
    container_port: int,
    host_port: int,
    environment: dict[str, str],
) -> None:
    inspection = inspect_container(container_id, environment)
    assert inspection["NetworkSettings"]["Ports"][f"{container_port}/tcp"] == [
        {"HostIp": "127.0.0.1", "HostPort": str(host_port)}
    ]


def wait_for_liveness(web_port: int, timeout: int = 120) -> bytes:
    deadline = time.monotonic() + timeout
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    while time.monotonic() < deadline:
        try:
            with opener.open(
                f"http://127.0.0.1:{web_port}/health/live", timeout=4
            ) as response:
                if response.status == 200:
                    return response.read()
        except OSError:
            time.sleep(1)
    raise AssertionError("web liveness did not become available")


def project_resources(
    project_name: str,
    environment: dict[str, str],
) -> dict[str, list[str]]:
    resource_commands = {
        "containers": ["docker", "ps", "--all", "--quiet"],
        "volumes": ["docker", "volume", "ls", "--quiet"],
        "networks": ["docker", "network", "ls", "--quiet"],
        "images": ["docker", "image", "ls", "--quiet"],
    }
    return {
        resource_type: run_command(
            [
                *command,
                "--filter",
                f"label=com.docker.compose.project={project_name}",
            ],
            environment,
        ).stdout.split()
        for resource_type, command in resource_commands.items()
    }


def cleanup_project(
    project_name: str,
    environment: dict[str, str],
    env_file: Path,
    override_file: Path | None = None,
) -> None:
    original_exception = sys.exception()
    diagnostics = []
    try:
        result = compose_command(
            project_name,
            environment,
            env_file,
            "down",
            "--volumes",
            "--rmi",
            "local",
            "--remove-orphans",
            override_file=override_file,
            timeout=60,
            check=False,
        )
        if result.returncode != 0:
            diagnostics.append(f"docker compose down failed: {result.stderr.strip()}")
    except (OSError, subprocess.SubprocessError) as error:
        diagnostics.append(f"docker compose down raised: {error}")

    try:
        resources = project_resources(project_name, environment)
        fallback_commands = {
            "containers": ["docker", "container", "rm", "--force"],
            "networks": ["docker", "network", "rm"],
            "volumes": ["docker", "volume", "rm", "--force"],
            "images": ["docker", "image", "rm", "--force"],
        }
        for resource_type in ("containers", "networks", "volumes", "images"):
            identifiers = resources[resource_type]
            if identifiers:
                fallback = run_command(
                    [*fallback_commands[resource_type], *identifiers],
                    environment,
                    check=False,
                )
                if fallback.returncode != 0:
                    diagnostics.append(
                        f"scoped {resource_type} cleanup failed: "
                        f"{fallback.stderr.strip()}"
                    )
        remaining = {
            resource_type: identifiers
            for resource_type, identifiers in project_resources(
                project_name, environment
            ).items()
            if identifiers
        }
        if remaining:
            diagnostics.append(f"project resources remain: {remaining}")
    except (OSError, subprocess.SubprocessError) as error:
        diagnostics.append(f"project cleanup verification raised: {error}")

    if diagnostics:
        message = "; ".join(diagnostics)
        if original_exception is not None:
            original_exception.add_note(message)
        else:
            raise AssertionError(message)


def test_fresh_compose_stack_authenticates_migrates_and_survives_restart(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for name in tuple(os.environ):
        if name.startswith("PG"):
            monkeypatch.delenv(name)

    project_name = f"appointment-booking-m1-t2-{uuid4().hex}"
    database_port = available_port()
    web_port = available_port()
    while web_port == database_port:
        web_port = available_port()
    env_file = tmp_path / ".env"
    env_file.write_text(f"DATABASE_PORT={database_port}\nWEB_HOST_PORT={web_port}\n")
    migration_settings = tmp_path / "runtime_migration_settings.py"
    migration_settings.write_text(
        "from config.settings import *\n"
        'INSTALLED_APPS = [*INSTALLED_APPS, "django.contrib.contenttypes"]\n'
    )
    migration_override = tmp_path / "runtime-migration.yaml"
    migration_override.write_text(
        json.dumps(
            {
                "services": {
                    "web": {
                        "environment": {
                            "DJANGO_SETTINGS_MODULE": "runtime_migration_settings"
                        },
                        "volumes": [
                            {
                                "type": "bind",
                                "source": str(migration_settings),
                                "target": "/app/runtime_migration_settings.py",
                                "read_only": True,
                            }
                        ],
                    }
                }
            }
        )
    )
    environment = isolated_environment()
    assert not any(project_resources(project_name, environment).values())

    try:
        compose_command(
            project_name,
            environment,
            env_file,
            "up",
            "--build",
            "--detach",
            timeout=180,
        )
        assert wait_for_liveness(web_port) == b'{"status": "ok"}'

        postgres_id = compose_command(
            project_name, environment, env_file, "ps", "--quiet", "postgres"
        ).stdout.strip()
        web_id = compose_command(
            project_name, environment, env_file, "ps", "--quiet", "web"
        ).stdout.strip()
        assert postgres_id
        assert web_id
        assert (
            inspect_container(postgres_id, environment)["State"]["Health"]["Status"]
            == "healthy"
        )
        assert_loopback_publication(postgres_id, 5432, database_port, environment)
        assert_loopback_publication(web_id, 8000, web_port, environment)
        assert inspect_container(web_id, environment)["Config"]["User"] == "10001:10001"

        compose_command(
            project_name,
            environment,
            env_file,
            "up",
            "--detach",
            "--force-recreate",
            "web",
            override_file=migration_override,
            timeout=180,
        )
        assert wait_for_liveness(web_port) == b'{"status": "ok"}'
        web_id = compose_command(
            project_name,
            environment,
            env_file,
            "ps",
            "--quiet",
            "web",
            override_file=migration_override,
        ).stdout.strip()
        assert web_id

        initial_fingerprint = database_fingerprint(database_port)
        assert initial_fingerprint[0] == DATABASE_NAME
        assert initial_fingerprint[2] == 0
        assert initial_fingerprint[3] == "scram-sha-256"
        assert initial_fingerprint[4] == "django_migrations"
        assert initial_fingerprint[5] == "django_content_type"
        assert initial_fingerprint[6] is True
        with pytest.raises(psycopg.OperationalError) as authentication_error:
            connect(database_port, "wrong-password")
        assert "password authentication failed" in str(authentication_error.value)
        assert DATABASE_USER in str(authentication_error.value)

        host_database = run_command(
            [
                "uv",
                "run",
                "--no-sync",
                "--env-file",
                str(env_file),
                "python",
                "-c",
                "import django; django.setup(); from django.db import connection; "
                "cursor = connection.cursor(); "
                "cursor.execute('SELECT current_database()'); "
                "print(connection.settings_dict['HOST'], "
                "connection.settings_dict['PORT'], cursor.fetchone()[0]); "
                "cursor.close()",
            ],
            {**environment, "DJANGO_SETTINGS_MODULE": "config.settings"},
        ).stdout.strip()
        assert host_database == f"127.0.0.1 {database_port} {DATABASE_NAME}"

        container_database = compose_command(
            project_name,
            environment,
            env_file,
            "exec",
            "-T",
            "web",
            "python",
            "-c",
            "import django; django.setup(); from django.db import connection; "
            "cursor = connection.cursor(); "
            "cursor.execute('SELECT current_database()'); "
            "print(cursor.fetchone()[0]); cursor.close()",
            override_file=migration_override,
        ).stdout.strip()
        assert container_database == DATABASE_NAME
        compose_command(
            project_name,
            environment,
            env_file,
            "exec",
            "-T",
            "web",
            "python",
            "manage.py",
            "migrate",
            "--check",
            override_file=migration_override,
        )
        assert (
            compose_command(
                project_name,
                environment,
                env_file,
                "exec",
                "-T",
                "web",
                "id",
                "-u",
                override_file=migration_override,
            ).stdout.strip()
            == "10001"
        )
        initial_secret = compose_command(
            project_name,
            environment,
            env_file,
            "exec",
            "-T",
            "web",
            "python",
            "-c",
            "from django.conf import settings; print(settings.SECRET_KEY)",
            override_file=migration_override,
        ).stdout.strip()
        initial_volume = volume_name(postgres_id, environment)
        create_sentinel(database_port)

        compose_command(
            project_name,
            environment,
            env_file,
            "restart",
            "postgres",
            "web",
            override_file=migration_override,
        )
        assert wait_for_liveness(web_port) == b'{"status": "ok"}'

        restarted_postgres_id = compose_command(
            project_name,
            environment,
            env_file,
            "ps",
            "--quiet",
            "postgres",
            override_file=migration_override,
        ).stdout.strip()
        restarted_fingerprint = database_fingerprint(database_port)
        restarted_secret = compose_command(
            project_name,
            environment,
            env_file,
            "exec",
            "-T",
            "web",
            "python",
            "-c",
            "from django.conf import settings; print(settings.SECRET_KEY)",
            override_file=migration_override,
        ).stdout.strip()
        assert restarted_fingerprint == initial_fingerprint
        assert restarted_secret == initial_secret == DJANGO_SECRET_KEY
        assert volume_name(restarted_postgres_id, environment) == initial_volume
        assert sentinel_value(database_port) == "preserved"
    finally:
        cleanup_project(project_name, environment, env_file, migration_override)


def test_web_does_not_start_while_postgresql_is_unhealthy(tmp_path: Path) -> None:
    project_name = f"appointment-booking-m1-t2-health-{uuid4().hex}"
    database_port = available_port()
    web_port = available_port()
    while web_port == database_port:
        web_port = available_port()
    env_file = tmp_path / ".env"
    env_file.write_text(f"DATABASE_PORT={database_port}\nWEB_HOST_PORT={web_port}\n")
    override_file = tmp_path / "unhealthy-postgres.yaml"
    override_file.write_text(
        "services:\n"
        "  postgres:\n"
        "    healthcheck:\n"
        '      test: ["CMD", "false"]\n'
        "      interval: 1s\n"
        "      timeout: 1s\n"
        "      retries: 1\n"
        "      start_period: 0s\n"
    )
    environment = isolated_environment()
    assert not any(project_resources(project_name, environment).values())

    try:
        result = compose_command(
            project_name,
            environment,
            env_file,
            "up",
            "--build",
            "--wait",
            "--wait-timeout",
            "10",
            override_file=override_file,
            timeout=30,
            check=False,
        )
        assert result.returncode != 0
        assert "unhealthy" in result.stderr.lower()
        postgres_id = compose_command(
            project_name,
            environment,
            env_file,
            "ps",
            "--all",
            "--quiet",
            "postgres",
            override_file=override_file,
        ).stdout.strip()
        assert postgres_id
        postgres_state = inspect_container(postgres_id, environment)["State"]
        assert postgres_state["Status"] == "running"
        assert postgres_state["Health"]["Status"] == "unhealthy"
        web_id = compose_command(
            project_name,
            environment,
            env_file,
            "ps",
            "--all",
            "--quiet",
            "web",
            override_file=override_file,
        ).stdout.strip()
        if web_id:
            web_status = inspect_container(web_id, environment)["State"]["Status"]
            assert web_status != "running"
    finally:
        cleanup_project(project_name, environment, env_file, override_file)
