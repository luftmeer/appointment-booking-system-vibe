# Repository Instructions

## Commands

Install dependencies:

    uv sync

Run backend tests:

    uv run pytest

Start PostgreSQL before database-backed host tests:

    docker compose up -d postgres

Run the Django system check:

    uv run python manage.py check

Run linting:

    uv run ruff check .

Run formatting check:

    uv run ruff format --check .

Start the development environment:

    docker compose up --build

## Architecture

- Domain logic must not depend directly on the web framework.
- Database access belongs in the persistence layer.
- API routes must not contain booking conflict logic.
- PostgreSQL is the source of truth for booking uniqueness.

## Development rules

- Implement one roadmap task at a time.
- Behaviour changes require tests.
- Do not weaken tests to make them pass.
- Do not introduce new dependencies without explaining why.
- Do not modify unrelated files.
- Do not claim completion without running every required command that is available after the current task.
- Database schema changes require migrations.
- Never store production, personal, or reusable credentials in the repository. Clearly labelled development-only placeholders are not security boundaries and must be rejected by production configuration.

## Staged command applicability

- Bootstrap tasks must run every repository command that exists after that task.
- Report an unavailable command exactly as `N/A — <specific reason the command does not yet exist>`.
- A task may not report an available command as passing unless it was actually executed.
- From `M0-T2` onward, `uv sync`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest`, and `uv run python manage.py check` must pass.
- From `M1` onward, start PostgreSQL with `docker compose up -d postgres` before host-based database tests.

## Completion evidence

For every task, report:

- files changed
- tests added or changed
- commands run
- command results
- remaining risks
