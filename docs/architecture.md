# Architecture

## Status And Decision Labels

This document describes the approved architecture for the initial application.

- **Confirmed** means approved and expected to guide implementation.
- **Assumption** means approved as a reversible default.
- **TBD** means genuinely unresolved and must not be guessed during implementation.

## Selected Technology Stack

| Area | Selection | Status | Rationale |
| --- | --- | --- | --- |
| Language | Python 3.12 | Confirmed | Stable Python baseline compatible with the selected framework and tooling. |
| Web framework | Django 5.2 LTS | Confirmed | Integrated authentication, sessions, CSRF, forms, migrations, and server rendering minimize project complexity. |
| Frontend | Django templates with small TypeScript modules | Confirmed | Provides modern interactions without SPA routing or duplicated server state. |
| Asset build | Vite | Assumption | Small, conventional TypeScript and CSS build with versioned assets. |
| Database | PostgreSQL 16 | Confirmed | Required source of truth and supports partial unique and exclusion constraints. |
| Persistence | Django ORM behind repositories and query objects | Confirmed | Keeps database access in the persistence layer and domain logic independent of Django. |
| Python packaging | `uv` and `pyproject.toml` | Confirmed | Matches repository commands and supports locked, repeatable installs. |
| Python quality | Ruff and pytest | Confirmed | Matches repository commands and project constraints. |
| Browser tests | pytest-Playwright with Chromium | Confirmed | Supports responsive, accessibility, and end-to-end verification in the required Python test workflow. |
| Local runtime | Docker Compose | Confirmed | Required repeatable local environment with one documented command. |
| CI | GitHub Actions | Confirmed | Required clean-checkout verification platform. |

Exact patch versions will be recorded in lock files during repository foundation work. No framework substitution is implied by that version pinning.

## Architectural Style

The system is an integrated modular monolith with one Django application and one PostgreSQL database.

It is not a collection of microservices. Customer and administrator interfaces share the same origin and process. Modules communicate through Python application-service and query interfaces, not network calls.

The internal dependency direction is:

```text
HTTP views and forms
        |
        v
application services and queries
        |
        v
domain rules and persistence interfaces
        |
        v
Django ORM persistence adapters
        |
        v
PostgreSQL
```

Domain rules do not import Django views, request objects, templates, or ORM models. HTTP views do not contain booking conflict logic. ORM access is isolated in persistence repositories and query objects.

## System Context

```text
Customer browser --------------------+
                                      |
Administrator browser ---------------+--> Django modular monolith --> PostgreSQL
                                      |
GitHub Actions test runner -----------+
```

External payment, email, SMS, and calendar systems do not exist in the approved scope.

## Responsibilities

### Frontend

The frontend is responsible for:

- Rendering server-provided pages and forms responsively.
- Providing keyboard-operable controls and relevant status messages.
- Performing advisory input validation for usability.
- Preventing accidental repeat clicks in one browser.
- Generating and retaining a booking idempotency value and management secret for one uncertain request flow.
- Showing pending, success, empty, validation, conflict, and uncertain-outcome states.
- Refreshing availability after a successful mutation or conflict.

The frontend is not responsible for deciding authoritative availability, transaction success, uniqueness, or authorization.

### Backend Application

The Django application is responsible for:

- Parsing HTTP input and enforcing CSRF, authentication, and authorization.
- Calling framework-independent application services and persistence queries.
- Defining short transaction boundaries for state-changing commands.
- Coordinating row locking and deterministic lock order.
- Validating business transitions against current database state.
- Writing current state and history in one transaction.
- Mapping expected domain and database conflicts to stable HTTP responses.
- Rendering pages only after successful transaction completion.

### Database

PostgreSQL is responsible for:

- Atomic commit and rollback.
- Foreign-key and check constraints.
- At most one confirmed booking per slot through a partial unique index.
- Unique booking references and idempotency-key hashes.
- Rejecting overlapping slots for the single resource.
- Row locks requested by application transactions.
- Preventing duplicate active bookings even if application prechecks are bypassed.

## Major Modules And Boundaries

### `common`

Owns health endpoints, shared error representations, correlation IDs, logging filters, and cross-cutting template helpers. It contains no booking rules. The readiness HTTP view delegates to an infrastructure health probe or persistence interface and never issues a direct ORM or database query.

### `availability`

Owns slot concepts, public availability queries, and administrator slot commands. It exposes application interfaces for creating, closing, reopening, and querying slots. Persistence adapters contain all slot ORM access.

### `bookings`

Owns booking state, booking events, and application services for create, cancel, and reschedule. It defines domain errors and persistence interfaces. It does not know about Django requests or templates.

### `booking_access`

Owns customer capability-credential verification and booking-scoped sessions. It cannot grant access to a different booking or administrator functionality.

### `accounts`

Owns administrator login, logout, session policy, and abuse protection using Django authentication.

### `customer_portal`

Owns customer-facing views, forms, URLs, and templates. It delegates state transitions to application services and reads to query objects.

### `admin_portal`

Owns protected administrator views, forms, URLs, and templates for availability and history. It contains no direct ORM or booking conflict logic.

### `persistence`

Persistence is organized per business module rather than as a separate deployable service. Repository and query modules implement domain-facing interfaces with the Django ORM. Transactions may be coordinated in application services using a narrow transaction abstraction, but raw model access does not occur in HTTP routes.

## Proposed Repository Structure

```text
AGENTS.md
README.md
pyproject.toml
uv.lock
package.json
package-lock.json
manage.py
Dockerfile
compose.yaml
config/
  settings/
  urls.py
  asgi.py
  wsgi.py
apps/
  common/
  availability/
    domain.py
    services.py
    queries.py
    persistence.py
    models.py
  bookings/
    domain.py
    services/
    queries.py
    persistence.py
    models.py
  booking_access/
  accounts/
  customer_portal/
  admin_portal/
frontend/
  src/
templates/
tests/
  unit/
  integration/
  database/
  concurrency/
  e2e/
docs/
  experiment-log.md
  decisions/
    001-technology-stack.md
    002-critical-feature-strategy.md
    003-postgresql-test-topology.md
    004-local-development-configuration.md
```

The exact package split may be simplified where a module would otherwise be empty, but the dependency boundaries are confirmed.

## Domain Entities

### Appointment Slot

Represents explicit availability for the one consulting resource.

Key attributes are ID, start timestamp, end timestamp, open or closed status, and audit timestamps. Occupancy is derived from confirmed bookings; there is no separate authoritative `booked` flag.

### Booking

Represents the current customer appointment state.

Key attributes are ID, public reference, current slot ID, `confirmed` or `cancelled` status, customer contact fields, management-secret hash, idempotency-key hash, request fingerprint, and timestamps.

### Booking Event

Represents an append-only history entry created through normal application operations.

Event types are booking created, booking rescheduled, and booking cancelled. A rescheduling event records old and new slot IDs. Rescheduling is not a booking status.

### Administrator

Uses Django's supported authentication model and staff authorization. The product has one administrator and no application-level role editor.

### Booking-Scoped Session

Represents temporary authorization to view or mutate one booking after a management credential is verified. It is separate from administrator authentication.

## Data Flow

### Public Availability

1. A customer requests the availability page.
2. The customer view calls an availability query interface.
3. The persistence query selects future open slots with no confirmed booking.
4. The view renders dates and times using the configured service timezone.

### Booking Creation

1. The browser submits slot ID, contact fields, management secret, and idempotency identity.
2. The view validates transport-level input and calls the booking application service.
3. The service checks for an idempotent replay.
4. The service starts a transaction and locks the selected slot.
5. The service rechecks idempotency, slot state, start time, and occupancy.
6. Persistence creates the confirmed booking and creation event.
7. PostgreSQL enforces the partial unique index.
8. The transaction commits before the view returns confirmation.
9. A losing request receives `409 Conflict`; an idempotent replay receives the existing booking.

### Cancellation

1. Booking-scoped access is verified.
2. The service locks the booking in a transaction.
3. It validates status and server time.
4. It changes the status and appends one cancellation event.
5. Both changes commit together.

### Rescheduling

1. Booking-scoped access is verified.
2. The service locks the booking and target slot in documented order.
3. It validates the current booking and target slot.
4. It updates the current slot and appends a rescheduling event.
5. PostgreSQL arbitrates any target conflict.
6. Failure rolls back the update and event, preserving the original booking.

## HTTP And API Boundaries

The application uses same-origin HTML pages with TypeScript-enhanced JSON or form submissions. Endpoint names are confirmed at the responsibility level; exact URL spelling may be adjusted consistently during implementation.

### Customer

```text
GET  /appointments
GET  /availability/slots
POST /bookings
POST /booking-access
GET  /booking
POST /booking/cancel
POST /booking/reschedule
```

### Administrator

```text
GET  /admin/login
POST /admin/login
POST /admin/logout
GET  /admin/availability
POST /admin/availability
POST /admin/availability/{slot_id}/close
POST /admin/availability/{slot_id}/reopen
GET  /admin/bookings
GET  /admin/bookings/{reference}
```

State-changing endpoints require POST, CSRF protection, and appropriate authorization. Views call application services; they do not query ORM models directly.

### Stable Response Semantics

- `200 OK`: Read or successful idempotent replay.
- `201 Created`: First successful booking creation.
- `400 Bad Request` or form errors: Malformed transport input.
- `403 Forbidden`: Authenticated but unauthorized administrator request where disclosure is safe.
- `404 Not Found`: Public resource is absent; customer credential failures use a generic unavailable response.
- `409 Conflict`: Slot unavailable, invalid state transition, or idempotency key reused with different input.
- `422 Unprocessable Content`: Optional JSON validation response if adopted consistently; HTML forms may use `200` with errors.
- `503 Service Unavailable`: Temporary lock, database, or uncertain infrastructure failure that may be safely retried with the same idempotency identity.

## Persistence Strategy

- Django migrations own all schema changes.
- PostgreSQL is used in integration and concurrency tests; SQLite is not an acceptable substitute.
- Repository methods implement writes and entity retrieval for application services.
- Query objects implement optimized read models for availability and history.
- Application services define transaction boundaries and lock order.
- Booking creation and its event share one transaction.
- Cancellation and its event share one transaction.
- Rescheduling and its event share one transaction.
- A named partial unique index enforces one confirmed booking per slot.
- A named exclusion constraint prevents overlapping slot ranges.
- Named constraints allow expected integrity errors to be mapped without hiding unrelated defects.

Conceptual booking invariant:

```sql
CREATE UNIQUE INDEX uniq_confirmed_booking_per_slot
ON booking (slot_id)
WHERE status = 'confirmed';
```

## Error-Handling Strategy

Domain and application services raise stable typed errors such as slot unavailable, booking not changeable, same-slot reschedule, unauthorized booking access, and idempotency-key reuse.

HTTP adapters map those errors to responses. Expected conflicts are not logged as unhandled exceptions. Unexpected exceptions are logged with correlation IDs and rendered without internal details.

Database integrity errors are handled only when their named constraint is recognized. Unknown integrity errors propagate to the global unexpected-error handler and are not mislabeled as booking conflicts.

The frontend preserves recoverable input, manages focus, and distinguishes retryable temporary failures from conflicts requiring user action.

Error and redaction protections are introduced with the values they protect. M7 adds the minimum shared booking-domain HTTP mapping and idempotency-value redaction; its booking endpoint also prohibits request-body and raw management-secret logging. M8 adds reusable management-secret and capability redaction when the booking-access boundary is introduced. M12 audits and consolidates system-wide consistency rather than introducing those protections for the first time.

## Security Considerations

- Administrator passwords use Django authentication and hashing.
- Local and CI values come from environment configuration. Tracked development defaults are clearly labelled, intentionally public placeholders and are never treated as secrets.
- `.env` remains ignored; `.env.example` documents every supported variable without containing a real credential.
- Production configuration requires externally supplied secrets and refuses to start with a missing value or any known development placeholder.
- PostgreSQL trust authentication is prohibited; local PostgreSQL uses password authentication.
- The local Django development secret is stable across restarts rather than regenerated by each container start.
- Administrator routes verify staff authorization server-side.
- Customer management credentials are high entropy, stored as one-way hashes, omitted from query strings, and redacted from logs.
- Initial management links use a URL fragment that TypeScript exchanges through a same-origin POST so web-server logs do not receive the secret.
- Booking-scoped sessions cannot access another booking or administrator routes.
- Raw idempotency values are hashed for persistence and redacted from logs.
- CSRF protection applies to all browser mutations.
- Session fixation is mitigated by rotating sessions after successful authentication or credential exchange.
- Login and credential-exchange abuse protection is required.
- Templates escape customer-provided content by default.
- HTTPS termination is outside the local Compose environment but required for any public deployment.
- Personal-data retention is `TBD` and must be settled before real customer data is used.

## Local Development And Deployment Architecture

### Local Development

```text
Docker Compose
  web: Django application and compiled TypeScript assets
  postgres: PostgreSQL database with a named development volume
```

`docker compose up --build` is the required one-command start. The web entrypoint waits for PostgreSQL and applies migrations before serving. Local-only development values must be clearly distinguished from secrets used in any deployed environment.

Compose includes clearly labelled development-only placeholders so a clean checkout can start with one command. These values are intentionally unsuitable for production and are rejected by production settings. An ignored `.env` may override them. PostgreSQL is published on a configurable loopback-only host port and is not exposed on all host interfaces.

### PostgreSQL Test Topology

The canonical host sequence for any database-backed test is:

```bash
docker compose up -d postgres
uv run pytest
```

- Host commands use `DATABASE_HOST=127.0.0.1` and the configured loopback-published port.
- Commands running in Compose use `DATABASE_HOST=postgres` and PostgreSQL's container port.
- Environment variables select the hostname, port, database, user, and development placeholder password; application code does not infer topology.
- Django creates a dedicated test database. Tests do not use developer data and must clean their own records.
- Migration verification that claims clean-schema support starts from an empty database.
- A `curl` command is valid only after the web service has been started explicitly with `docker compose up -d --build web postgres` or the complete Compose startup command.

ADR 003 records the complete test-topology decision. ADR 004 records local placeholder and production-secret requirements.

### CI

GitHub Actions is introduced incrementally. M0 verifies locked Python installation, Django checks, Ruff, and the current pytest suite. M1 adds a fresh PostgreSQL service and migration checks. M2 adds locked Node installation, TypeScript, Vite, Chromium installation, and browser prerequisites. Later milestones add their tests to those existing stages rather than creating a separate pipeline at the end.

Each CI database job receives a fresh PostgreSQL service and environment configuration equivalent to the host topology. Browser jobs install Chromium through Playwright and collect screenshots and traces only on failure.

### Deployment Boundary

The approved architecture is one web application plus PostgreSQL. Production hosting, TLS termination, backup operation, and infrastructure provisioning are not approved implementation scope. No queue, worker, message broker, service mesh, or Kubernetes component is present.

## Critical Technical Risks

| Risk | Mitigation |
| --- | --- |
| Concurrent double booking | Short row-locking transaction plus PostgreSQL partial unique index and deterministic concurrency tests. |
| Stale availability | Recheck inside the transaction and return `409` with refreshed alternatives. |
| Lost booking response | Idempotency identity and request fingerprint recover an existing committed booking. |
| Credential leakage | Hash at rest, omit from query strings, redact logs, exchange URL fragments by POST. |
| Domain/framework coupling | Domain types and services do not import Django; persistence adapters own ORM access. |
| Deadlocks | Document and test one lock order for booking, slot, cancellation, rescheduling, and administration. |
| Migration/constraint drift | Migration checks and direct PostgreSQL constraint tests in CI. |
| History inconsistency | Write current state and history event in the same transaction. |
| Frontend reporting false success | Render confirmation only after committed success or verified idempotent replay. |
| Flaky concurrency tests | Independent connections, explicit barriers, and final database-state assertions instead of timing sleeps. |

## Confirmed Decisions

- Integrated Django modular monolith.
- Server-rendered pages with small TypeScript enhancements.
- PostgreSQL as the source of truth.
- Framework-independent domain rules and explicit persistence boundaries.
- Database-enforced active-booking uniqueness.
- Docker Compose local environment and GitHub Actions CI.
- No distributed systems or asynchronous messaging.

## Remaining Assumptions And TBDs

- **Assumption:** Vite is the TypeScript asset builder.
- **Assumption:** Administrator history uses 50 records per page.
- **TBD:** Service timezone identifier.
- **TBD:** Standard appointment duration.
- **TBD:** Personal-data retention and anonymization policy.
- **TBD:** Public deployment exposure and any resulting stronger administrator-authentication requirements.
- **TBD:** Recovery mechanism for a customer who loses management access.

The product specification's open-decision register identifies the milestone blocked by each `TBD`. No open decision blocks M0 or M1.
