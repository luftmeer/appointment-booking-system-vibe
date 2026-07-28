import json
import os
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ATTEMPTS_ERROR = "DATABASE_STARTUP_MAX_ATTEMPTS must be an integer from 1 through 1000"
DELAY_ERROR = "DATABASE_STARTUP_RETRY_DELAY must be an integer from 0 through 300"
PYTHON_STUB = """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
with Path(os.environ["ENTRYPOINT_LOG"]).open("a") as log:
    log.write(json.dumps(args) + "\\n")

if args and args[0] == "-c":
    count_file = Path(os.environ["ENTRYPOINT_PROBE_COUNT"])
    count = int(count_file.read_text()) + 1 if count_file.exists() else 1
    count_file.write_text(str(count))
    if count <= int(os.environ.get("ENTRYPOINT_PROBE_FAILURES", "0")):
        raise SystemExit(1)

if args[:3] == ["manage.py", "migrate", "--noinput"]:
    if os.environ.get("ENTRYPOINT_MIGRATION_FAIL") == "1":
        raise SystemExit(42)
"""


@pytest.fixture
def entrypoint_environment(tmp_path: Path) -> dict[str, str]:
    python = tmp_path / "python"
    python.write_text(PYTHON_STUB)
    python.chmod(0o755)
    sleep = tmp_path / "sleep"
    sleep.write_text('#!/bin/sh\nprintf "%s\\n" "$1" >> "$ENTRYPOINT_SLEEP_LOG"\n')
    sleep.chmod(0o755)
    environment = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("ENTRYPOINT_")
        and name
        not in {
            "DATABASE_STARTUP_MAX_ATTEMPTS",
            "DATABASE_STARTUP_RETRY_DELAY",
        }
    }
    return {
        **environment,
        "PATH": f"{tmp_path}{os.pathsep}{os.environ['PATH']}",
        "DATABASE_STARTUP_MAX_ATTEMPTS": "10",
        "DATABASE_STARTUP_RETRY_DELAY": "0",
        "ENTRYPOINT_LOG": str(tmp_path / "entrypoint.log"),
        "ENTRYPOINT_PROBE_COUNT": str(tmp_path / "probe-count"),
        "ENTRYPOINT_SLEEP_LOG": str(tmp_path / "sleep.log"),
        "ENTRYPOINT_COMMAND_MARKER": str(tmp_path / "command-started"),
    }


def run_entrypoint(environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "/bin/sh",
            "docker/entrypoint.sh",
            "/bin/sh",
            "-c",
            'printf started > "$ENTRYPOINT_COMMAND_MARKER"',
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=2,
        check=False,
    )


def entrypoint_calls(environment: dict[str, str]) -> list[list[str]]:
    log = Path(environment["ENTRYPOINT_LOG"])
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text().splitlines()]


def entrypoint_sleeps(environment: dict[str, str]) -> list[str]:
    log = Path(environment["ENTRYPOINT_SLEEP_LOG"])
    return log.read_text().splitlines() if log.exists() else []


@pytest.mark.parametrize(
    ("name", "value", "message"),
    [
        ("DATABASE_STARTUP_MAX_ATTEMPTS", "", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_MAX_ATTEMPTS", " ", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_MAX_ATTEMPTS", "01", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_MAX_ATTEMPTS", "invalid", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_MAX_ATTEMPTS", "0", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_MAX_ATTEMPTS", "-1", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_MAX_ATTEMPTS", "1001", ATTEMPTS_ERROR),
        ("DATABASE_STARTUP_RETRY_DELAY", "", DELAY_ERROR),
        ("DATABASE_STARTUP_RETRY_DELAY", " ", DELAY_ERROR),
        ("DATABASE_STARTUP_RETRY_DELAY", "01", DELAY_ERROR),
        ("DATABASE_STARTUP_RETRY_DELAY", "invalid", DELAY_ERROR),
        ("DATABASE_STARTUP_RETRY_DELAY", "-1", DELAY_ERROR),
        ("DATABASE_STARTUP_RETRY_DELAY", "301", DELAY_ERROR),
    ],
)
def test_entrypoint_rejects_invalid_startup_bounds_before_connecting(
    entrypoint_environment: dict[str, str],
    name: str,
    value: str,
    message: str,
) -> None:
    entrypoint_environment[name] = value

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode != 0
    assert message in result.stderr
    assert entrypoint_calls(entrypoint_environment) == []


def test_entrypoint_accepts_valid_boundaries(
    entrypoint_environment: dict[str, str],
) -> None:
    entrypoint_environment["DATABASE_STARTUP_MAX_ATTEMPTS"] = "1000"
    entrypoint_environment["DATABASE_STARTUP_RETRY_DELAY"] = "300"

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode == 0
    assert [call[0] for call in entrypoint_calls(entrypoint_environment)] == [
        "-c",
        "manage.py",
    ]


def test_entrypoint_uses_defaults_when_controls_are_unset(
    entrypoint_environment: dict[str, str],
) -> None:
    entrypoint_environment.pop("DATABASE_STARTUP_MAX_ATTEMPTS")
    entrypoint_environment.pop("DATABASE_STARTUP_RETRY_DELAY")
    entrypoint_environment["ENTRYPOINT_PROBE_FAILURES"] = "1"

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode == 0
    assert "Waiting for PostgreSQL (attempt 1/10)" in result.stdout
    assert entrypoint_sleeps(entrypoint_environment) == ["1"]


def test_entrypoint_retries_then_migrates_before_starting_command(
    entrypoint_environment: dict[str, str],
) -> None:
    entrypoint_environment["DATABASE_STARTUP_MAX_ATTEMPTS"] = "3"
    entrypoint_environment["DATABASE_STARTUP_RETRY_DELAY"] = "7"
    entrypoint_environment["ENTRYPOINT_PROBE_FAILURES"] = "2"

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode == 0
    calls = entrypoint_calls(entrypoint_environment)
    assert [call[0] for call in calls] == ["-c", "-c", "-c", "manage.py"]
    assert calls[-1] == ["manage.py", "migrate", "--noinput"]
    assert entrypoint_sleeps(entrypoint_environment) == ["7", "7"]
    assert Path(entrypoint_environment["ENTRYPOINT_COMMAND_MARKER"]).read_text() == (
        "started"
    )


def test_entrypoint_stops_at_connection_attempt_limit(
    entrypoint_environment: dict[str, str],
) -> None:
    entrypoint_environment["DATABASE_STARTUP_MAX_ATTEMPTS"] = "2"
    entrypoint_environment["ENTRYPOINT_PROBE_FAILURES"] = "2"

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode != 0
    assert "PostgreSQL did not become available after 2 attempts" in result.stderr
    assert [call[0] for call in entrypoint_calls(entrypoint_environment)] == [
        "-c",
        "-c",
    ]
    assert entrypoint_sleeps(entrypoint_environment) == ["0"]
    assert not Path(entrypoint_environment["ENTRYPOINT_COMMAND_MARKER"]).exists()


def test_entrypoint_attempt_limit_of_one_does_not_sleep(
    entrypoint_environment: dict[str, str],
) -> None:
    entrypoint_environment["DATABASE_STARTUP_MAX_ATTEMPTS"] = "1"
    entrypoint_environment["ENTRYPOINT_PROBE_FAILURES"] = "1"

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode != 0
    assert [call[0] for call in entrypoint_calls(entrypoint_environment)] == ["-c"]
    assert entrypoint_sleeps(entrypoint_environment) == []


def test_entrypoint_does_not_start_command_after_migration_failure(
    entrypoint_environment: dict[str, str],
) -> None:
    entrypoint_environment["ENTRYPOINT_MIGRATION_FAIL"] = "1"

    result = run_entrypoint(entrypoint_environment)

    assert result.returncode == 42
    assert [call[0] for call in entrypoint_calls(entrypoint_environment)] == [
        "-c",
        "manage.py",
    ]
    assert not Path(entrypoint_environment["ENTRYPOINT_COMMAND_MARKER"]).exists()
