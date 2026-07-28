import json
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def compose_config(environment: dict[str, str]) -> dict[str, object]:
    result = subprocess.run(
        ["docker", "compose", "config", "--format", "json"],
        cwd=PROJECT_ROOT,
        env={**os.environ, **environment},
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_postgresql_binding_cannot_be_widened_by_environment() -> None:
    config = compose_config({"POSTGRES_BIND_HOST": "0.0.0.0"})
    postgres = config["services"]["postgres"]

    assert postgres["ports"][0]["host_ip"] == "127.0.0.1"


def test_web_binding_cannot_be_widened_by_environment() -> None:
    config = compose_config({"WEB_BIND_HOST": "0.0.0.0"})
    web = config["services"]["web"]

    assert web["ports"][0]["host_ip"] == "127.0.0.1"


def test_database_port_selects_only_the_host_publication() -> None:
    config = compose_config({"DATABASE_PORT": "55432"})
    postgres = config["services"]["postgres"]
    web = config["services"]["web"]

    assert postgres["ports"][0]["published"] == "55432"
    assert web["environment"]["DATABASE_PORT"] == "5432"
