import os
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("name", "value", "message"),
    [
        (
            "DATABASE_STARTUP_MAX_ATTEMPTS",
            "invalid",
            "DATABASE_STARTUP_MAX_ATTEMPTS must be an integer from 1 through 1000",
        ),
        (
            "DATABASE_STARTUP_MAX_ATTEMPTS",
            "0",
            "DATABASE_STARTUP_MAX_ATTEMPTS must be an integer from 1 through 1000",
        ),
        (
            "DATABASE_STARTUP_MAX_ATTEMPTS",
            "-1",
            "DATABASE_STARTUP_MAX_ATTEMPTS must be an integer from 1 through 1000",
        ),
        (
            "DATABASE_STARTUP_MAX_ATTEMPTS",
            "1001",
            "DATABASE_STARTUP_MAX_ATTEMPTS must be an integer from 1 through 1000",
        ),
        (
            "DATABASE_STARTUP_RETRY_DELAY",
            "invalid",
            "DATABASE_STARTUP_RETRY_DELAY must be an integer from 0 through 300",
        ),
        (
            "DATABASE_STARTUP_RETRY_DELAY",
            "-1",
            "DATABASE_STARTUP_RETRY_DELAY must be an integer from 0 through 300",
        ),
        (
            "DATABASE_STARTUP_RETRY_DELAY",
            "301",
            "DATABASE_STARTUP_RETRY_DELAY must be an integer from 0 through 300",
        ),
    ],
)
def test_entrypoint_rejects_invalid_startup_bounds(
    name: str,
    value: str,
    message: str,
) -> None:
    result = subprocess.run(
        ["/bin/sh", "docker/entrypoint.sh"],
        cwd=PROJECT_ROOT,
        env={
            **os.environ,
            "DATABASE_STARTUP_MAX_ATTEMPTS": "10",
            "DATABASE_STARTUP_RETRY_DELAY": "1",
            name: value,
        },
        capture_output=True,
        text=True,
        timeout=2,
        check=False,
    )

    assert result.returncode != 0
    assert message in result.stderr
