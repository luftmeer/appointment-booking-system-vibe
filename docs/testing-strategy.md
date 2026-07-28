# Testing Strategy

## Objectives

Testing must provide confidence in externally observable behavior, database integrity, security boundaries, and complete user journeys.

Tests shall:

- Verify product behavior rather than repeat implementation statements.
- Prove the PostgreSQL double-booking invariant independently of application prechecks.
- Exercise domain rules without requiring HTTP.
- Exercise persistence and transaction behavior against real PostgreSQL.
- Verify authorization and error responses at HTTP boundaries.
- Cover core customer and administrator workflows in a real browser.
- Remain deterministic and suitable for clean-checkout CI execution.

Tests shall not assert private helper call order, internal variable values, exact SQL text, or template implementation details unless those details form an approved external contract.

## Test Layers

### Unit Tests

Unit tests target framework-independent domain behavior and pure presentation helpers.

Scope includes:

- Booking and slot state-transition rules.
- Server-time boundary decisions using an injected clock.
- Contact normalization and request fingerprint construction.
- Error-code selection from domain outcomes.
- Idempotency comparison rules.
- Date and timezone presentation helpers where pure.
- Frontend functions that transform response states into visible UI states.

Unit tests do not mock Django ORM chains. If behavior depends on constraints, locking, queries, or transactions, it belongs in an integration or database test.

Expected qualities:

- Fast and deterministic.
- No network or database.
- Explicit examples around exact appointment start time.
- Assertions on returned state, emitted domain event data, or typed errors.

## Integration Tests

Integration tests verify boundaries between application services, persistence adapters, Django HTTP handling, and PostgreSQL.

Scope includes:

- Repository and query behavior against PostgreSQL.
- Application-service transaction commit and rollback.
- Booking and event atomicity.
- Django form and JSON input validation.
- HTTP status codes and stable error codes.
- CSRF, session, authentication, and authorization behavior.
- Booking-scoped customer access.
- Administrator availability management.
- Availability and history query correctness and query counts.
- Logging redaction.

Integration tests assert observable database state and HTTP outcomes. They do not treat a mocked repository call as proof that a booking was created.

## Database Testing Strategy

PostgreSQL is mandatory for database, integration, and concurrency suites. SQLite cannot represent the approved partial unique and exclusion constraints or the required locking behavior.

### Canonical Development Topology

The canonical host sequence is:

```bash
docker compose up -d postgres
uv run pytest
```

When an ignored `.env` supplies local overrides, host tests load it explicitly:

```bash
docker compose up -d postgres
uv run --env-file .env pytest
```

- Host tests connect with `DATABASE_HOST=127.0.0.1` through a loopback-only published port.
- Commands executed in a Compose container connect with `DATABASE_HOST=postgres`.
- Host, container, and CI choose connection values through environment variables documented in `.env.example`.
- An ignored `.env` may change the local loopback port or development placeholders.
- PostgreSQL uses password authentication; trust authentication is not permitted.
- Django's test runner creates a dedicated test database. Tests must not read or mutate the developer database.
- A migration test that claims clean-install support starts from an empty database.
- GitHub Actions provides a fresh PostgreSQL service and equivalent environment variables for every database job.

Database tests cover:

- `starts_at < ends_at` checks.
- Non-overlapping slot ranges and valid adjacent slots.
- Foreign-key behavior.
- Unique public booking references.
- Unique idempotency-key hashes.
- Partial uniqueness of confirmed bookings per slot.
- Coexistence of cancelled historical bookings with one new confirmed booking.
- Migration application to an empty database.
- Detection of model changes without migrations.

Named constraints are asserted by name when an expected integrity error forms part of conflict mapping. Tests should not assert generated SQL text.

Migration tests are added with every schema change and verify the behavior introduced by the migration. Database tests use clean transactions and explicit timezone-aware data.

## Difficult Feature: Concurrent Booking Tests

The difficult feature has multiple complementary tests because no single layer proves all guarantees.

### Direct Constraint Test

1. Create one future open slot.
2. Insert one confirmed booking.
3. Attempt a second confirmed booking for the same slot.
4. Assert PostgreSQL rejects the second write through `uniq_confirmed_booking_per_slot`.
5. Assert one confirmed booking remains.

This proves the invariant even when application conflict checks are bypassed.

### Deterministic Low-Level Race

1. Open two independent PostgreSQL connections and transactions.
2. Have both observe no confirmed booking for the slot.
3. Synchronize both workers with a barrier before insertion.
4. Let both attempt a confirmed insert.
5. Assert one commits and one receives the expected uniqueness violation.
6. Assert the final database state contains one confirmed booking.

This reproduces the unsafe check-then-insert race without relying on timing luck.

### Application-Service Race

1. Start two independent workers with distinct idempotency identities.
2. Submit the same slot through the booking application service.
3. Assert one service result is confirmed and one is slot unavailable.
4. Assert one booking and one creation event exist.

This verifies row-lock coordination and application error mapping.

### HTTP Race

1. Use two independent clients and database connections.
2. Submit simultaneous `POST /bookings` requests for the same slot.
3. Assert one receives `201 Created`.
4. Assert one receives `409 Conflict` with `slot_unavailable`.
5. Assert public availability no longer includes the slot.

This verifies externally observable behavior.

### Idempotent Race

1. Submit identical concurrent requests with the same idempotency identity and management secret.
2. Assert one booking and one creation event exist.
3. Assert one response is the first successful creation and the other is a successful replay.
4. Assert both responses refer to the same booking.

### Cross-Operation Races

Tests also cover:

- Booking creation versus administrator slot closure.
- Booking creation versus a reschedule targeting the same slot.
- Two reschedules targeting the same slot.
- Cancellation versus rescheduling of one booking.

Each test asserts both response outcomes and final database state. It is insufficient to assert only that no exception escaped.

### Concurrency Test Mechanics

- Use `pytest.mark.django_db(transaction=True)` or an equivalent transaction-enabled fixture.
- Give every worker its own database connection.
- Close inherited Django connections before starting worker operations.
- Use barriers or explicit lock coordination rather than arbitrary sleeps.
- Keep transaction time bounded.
- Repeat critical races in CI where practical, while retaining deterministic coordination.

## End-To-End Tests

pytest-Playwright owns browser integration and runs Chromium against a Django live server or equivalent explicitly started test application. The browser harness is established in M2 before any roadmap task requires browser assertions.

The harness defines:

- One configurable test base URL.
- A Django live-server or equivalent application-start fixture.
- Chromium installation through Playwright.
- Predictable test database setup through the canonical PostgreSQL topology.
- Failure-only screenshots and traces; successful runs do not retain browser artifacts by default.
- A local browser verification command and equivalent CI browser installation.

Local browser prerequisites and verification are:

```bash
docker compose up -d postgres
uv run playwright install chromium
uv run pytest tests/e2e
```

CI installs system browser dependencies with Playwright's supported `--with-deps` Chromium installation before running browser tests.

Required journeys are:

- View populated availability and create a booking.
- See no-availability and availability-failure states.
- Lose a slot conflict while retaining customer input.
- Retry after an uncertain booking response without creating a duplicate.
- Return through valid booking management access.
- Receive a generic invalid-access state.
- Cancel a future booking and see its slot return.
- Reschedule successfully.
- Lose a reschedule race and retain the original booking.
- Authenticate as administrator and create, close, and reopen availability.
- Reject administrator closure of a booked slot.
- Review customer and administrator booking history.
- Handle administrator session expiry.

Each core journey runs at a 320-pixel viewport and a standard desktop viewport where layout behavior differs. Keyboard navigation and focus after errors are verified. Automated accessibility checks support, but do not replace, behavior assertions.

End-to-end tests avoid asserting CSS class names or exact markup nesting. They select elements by role, label, accessible name, and stable user-visible status.

## Test Data And Fixture Strategy

- Factories create slots, bookings, events, and administrators through persistence interfaces or explicit database setup appropriate to the test layer.
- Factories require timezone-aware timestamps.
- Tests use an injected or frozen clock for past and boundary behavior.
- Standard slot states are future open, future closed, past open, confirmed, and cancelled.
- Contact values are clearly synthetic and never copied from real users.
- Every test owns its data and does not depend on execution order.
- Concurrency tests create isolated slots and idempotency values.
- Secrets and credentials use generated test values and do not appear in committed configuration.
- Browser tests create prerequisites through trusted test helpers, then verify behavior through the browser.

Factories should not silently create unrelated data that obscures the scenario. Invalid-state tests may use direct database operations when proving a constraint, but production services are used when testing product behavior.

## Frontend Verification

Frontend checks include:

- TypeScript compilation without emit.
- Formatting and linting.
- Production Vite build and manifest resolution.
- Unit tests for non-trivial response and retry state transitions.
- Browser tests for loading, validation, conflict, uncertain, success, and empty states.

Frontend tests do not claim to prove booking uniqueness. They verify only local click suppression, correct request identity reuse, and correct presentation of backend outcomes.

## Security Verification

Tests verify:

- Anonymous users cannot access administrator pages or mutations.
- Customer credentials authorize exactly one booking.
- Invalid access does not disclose booking existence.
- CSRF is required for browser mutations.
- Sessions rotate after authentication and capability exchange.
- Raw management credentials, idempotency values, passwords, and cookies do not appear in logs.
- Customer-provided text is escaped when rendered.
- Login and credential-exchange abuse controls activate without disclosing account state.

Security tests assert externally observable denial and absence of leaked data, not merely the presence of decorators or settings.

## Incremental CI Verification Stages

GitHub Actions runs from a clean checkout using pinned action versions and PostgreSQL.

### M0 Baseline

- Install Python dependencies from the lock file.
- Run Django system checks.
- Run Ruff formatting and linting.
- Run the current pytest suite, which is database-independent at this point.

### M1 PostgreSQL Extension

- Start a fresh PostgreSQL service.
- Supply CI database environment variables.
- Apply migrations to an empty database.
- Run migration drift and current PostgreSQL-backed tests.

### M2 Frontend And Browser Extension

- Install Node dependencies with `npm ci`.
- Run TypeScript formatting, linting, type checking, and Vite build.
- Install Chromium and its CI system dependencies.
- Run the current browser smoke suite against the configured live application.

M3 is a clean-checkout integration gate for these existing stages, not the first introduction of CI.

### Stage 1: Dependency And Static Verification

- Install Python dependencies from the lock file.
- Install Node dependencies with `npm ci`.
- Run Ruff formatting and linting.
- Run TypeScript formatting, linting, and type checks.
- Build production frontend assets.

### Stage 2: Django And Migration Verification

- Run Django system checks.
- Apply migrations to an empty PostgreSQL database.
- Run `makemigrations --check --dry-run`.

### Stage 3: Unit And Integration Tests

- Run framework-independent unit tests.
- Run persistence, HTTP, authorization, and transaction integration tests.

### Stage 4: Database And Concurrency Tests

- Run direct constraint tests.
- Run deterministic booking and rescheduling races.
- Assert final database state after every race.

### Stage 5: End-To-End Tests

- Start the complete application.
- Run Playwright customer and administrator journeys.
- Collect screenshots and traces only for failures.

No stage may use SQLite as a replacement for required PostgreSQL behavior.

## Required Quality Commands

Repository-required commands are authoritative:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run python manage.py check
docker compose up --build
```

Bootstrap tasks run every command available after that task. An unavailable command is reported exactly as `N/A — <specific reason the command does not yet exist>` and is never reported as passing.

The canonical database-backed host sequence is:

```bash
docker compose up -d postgres
uv run pytest <relevant test path>
```

Frontend commands will be added with the frontend foundation and are expected to include:

```bash
npm ci
npm run check
npm run typecheck
npm run build
```

Database and migration verification is expected to include:

```bash
docker compose up -d postgres
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate
```

A documented `curl` verification must first start the web service:

```bash
docker compose up -d --build web postgres
curl --fail http://localhost:8000/<path>
```

## Milestone Acceptance Criteria

A milestone is accepted only when:

1. Its user-visible or independently verifiable capability works.
2. All specified acceptance criteria are demonstrated through behavior or inspection.
3. New or changed behavior has tests at the appropriate layer.
4. PostgreSQL-specific behavior is tested against PostgreSQL.
5. Required repository commands pass.
6. No unrelated files are changed.
7. Migrations exist for every schema change and no uncommitted model drift remains.
8. Completion evidence lists files changed, tests changed, commands run, results, and remaining risks.
9. The experiment record is updated.
10. The change is small enough to review as one coherent roadmap task.

The final release additionally requires a clean-checkout Compose start, green CI, complete documentation, and no unresolved critical independent-review finding.
