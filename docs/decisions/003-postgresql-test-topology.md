# ADR 003: PostgreSQL Development Test Topology

## Status

Accepted.

## Context

Integration, database, and concurrency tests require real PostgreSQL behavior. The repository also requires host-based `uv run pytest`, while Docker Compose uses the service hostname `postgres`. The plan previously did not define how host and container processes select compatible database addresses or how a clean test database is obtained.

## Considered Alternatives

### Run Every Test Inside The Web Container

This provides one network topology but conflicts with the approved canonical host command and makes fast host development less direct.

### Use SQLite For Host Tests

This cannot verify partial unique indexes, exclusion constraints, or row locking and is rejected.

### Start PostgreSQL Through A Testcontainers Dependency

This can isolate tests but introduces another dependency and orchestration layer that is unnecessary for the approved Compose environment.

### Publish Compose PostgreSQL On Loopback

Host tests use a loopback-only published port, while container commands use the Compose service hostname. Both read environment-based configuration.

## Decision

Use the following canonical host sequence for database-backed tests:

```bash
docker compose up -d postgres
uv run pytest
```

- Host processes use `DATABASE_HOST=127.0.0.1` and a configurable loopback-published development port.
- Container processes use `DATABASE_HOST=postgres` and PostgreSQL's container port.
- Compose publishes PostgreSQL only on `127.0.0.1`, never on all host interfaces.
- `.env.example` documents the host and container variables; ignored `.env` may override local ports and development placeholders.
- pytest uses a dedicated test database created and cleaned through Django's test database behavior. Tests must not depend on developer data.
- Migration verification starts from an empty database where the test requires clean-schema evidence.
- CI obtains PostgreSQL from a fresh GitHub Actions service container and supplies equivalent environment variables.
- `curl` verification is valid only after the web service has been started explicitly, normally with `docker compose up -d --build web postgres` or `docker compose up -d --build`.

## Rationale

- It preserves the required host `uv run pytest` workflow.
- It exercises the same PostgreSQL features used by the application.
- Loopback-only publication limits local exposure.
- Environment selection keeps host, container, and CI settings explicit without branching domain or persistence behavior.
- It avoids another infrastructure dependency.

## Consequences

- Docker and the `postgres` service are prerequisites for database-backed host tests.
- Database milestone commands must start PostgreSQL before pytest.
- Host and container settings must not silently use the wrong hostname.
- Local port conflicts are handled through ignored environment overrides.
- CI workflow configuration must provide a fresh PostgreSQL service before database tests.

## Known Risks

- A developer may run pytest without first starting PostgreSQL; failures must be clear and actionable.
- A conflicting local port can prevent startup unless overridden.
- Misconfigured publication could expose development PostgreSQL beyond loopback; Compose verification must test the binding.
- Reusing a developer database instead of Django's test database could contaminate results; test settings must reject that topology.
