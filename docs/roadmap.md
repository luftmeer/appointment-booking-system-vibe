# Implementation Roadmap

## Delivery Rules

- Implement one task identifier at a time.
- Keep every task independently reviewable and avoid unrelated changes.
- Add or change tests with every behavior change.
- Keep domain logic independent of Django and ORM access inside persistence repositories or query objects.
- Add migrations with every schema change.
- Do not weaken tests to obtain a passing build.
- Explain every new dependency.
- Update the experiment record after every task.
- Report files changed, tests changed, commands run, results, and remaining risks as completion evidence.
- Do not proceed past a milestone until its acceptance criteria and verification commands pass.
- Execute tasks within each milestone in task-identifier order unless an explicit dependency says otherwise.
- Bootstrap tasks run every repository command available after that task. Report an unavailable command exactly as `N/A — <specific reason the command does not yet exist>`.
- Never report an available command as passing unless it was actually executed.
- Every task requiring browser assertions depends on M2-T3.

Unresolved `TBD` product decisions are tracked in the product and architecture documents. A task may proceed only when its behavior does not depend on an unresolved decision or the decision has been recorded explicitly.

## M0: Repository Foundation

### Objective

Create a minimal, maintainable Django project with locked dependencies and the repository's required quality commands.

### Resulting Capability

A reviewer can install dependencies, run Django system checks, request a liveness endpoint, and run the initial test and Ruff suites.

### Dependencies

None.

### Expected Modules Or Files

`docs/experiment-log.md`, `pyproject.toml`, `uv.lock`, `manage.py`, `config/`, `apps/common/`, `tests/smoke/`, `.gitignore`, `.env.example`, and `.github/workflows/ci.yml`.

### Acceptance Criteria

- `uv sync` installs from a committed lock file.
- Django starts and passes its system check.
- `/health/live` returns `200` without requiring the database.
- Settings read environment configuration without any committed production, personal, or reusable credential.
- Ruff formatting, Ruff linting, and pytest pass.

### Required Tests

Django configuration import, liveness endpoint, allowed HTTP method, and basic test-settings smoke tests.

### Verification Commands

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python manage.py check
```

### Risks

Premature abstractions, unpinned packages, environment-specific settings, and framework dependencies leaking into future domain code.

### Explicit Non-Goals

PostgreSQL integration, Docker, frontend assets, authentication, schema design, or booking behavior.

### Completion Evidence

Record the created structure, dependency rationale, tests added, all command results, and remaining setup risks in the task report and experiment record.

### Tasks

#### M0-T1: Initialize Implementation Traceability

| Field | Detail |
| --- | --- |
| Objective | Verify and maintain the pre-code implementation experiment record. |
| Implementation notes | Confirm that planning prompts, decisions, Plan-agent findings, failures, interventions, manual changes, defects, and architectural changes are backfilled before any application code; use `none` and `unknown` explicitly. |
| Expected files affected | `docs/experiment-log.md`. |
| Acceptance criteria | Every required planning category exists, no event or timestamp is invented, and the reusable implementation entry template is ready before M0-T2. |
| Tests required | Documentation review only. |
| Completion evidence | Reviewed traceability record, files changed, and unavailable repository commands reported with exact `N/A — <reason>` entries. |

#### M0-T2: Add Locked Python Tooling And Minimal Django Configuration

| Field | Detail |
| --- | --- |
| Objective | Establish locked Python dependencies, quality tooling, and enough Django configuration for all baseline Python commands to run. |
| Implementation notes | Configure `uv`, Ruff, pytest, and pytest-django; create `manage.py`, minimal settings and URL configuration, and one configuration smoke test; do not create the common application or liveness endpoint yet. |
| Expected files affected | `pyproject.toml`, `uv.lock`, `.gitignore`, `.env.example`, `manage.py`, minimal `config/`, `tests/conftest.py`, `tests/smoke/test_configuration.py`. |
| Acceptance criteria | `uv sync`, Ruff lint and format checks, the current pytest suite, and `manage.py check` all pass from a clean environment. |
| Tests required | Minimal Django settings and URL-configuration import smoke test. |
| Completion evidence | Dependency rationale, files changed, tests added, and actual results for all five required baseline commands. |

#### M0-T3: Add The Common Application And Liveness Endpoint

| Field | Detail |
| --- | --- |
| Objective | Add the shared common application, route configuration, and database-independent liveness behavior. |
| Implementation notes | Register `apps/common`, add its URL configuration, and keep `/health/live` independent of PostgreSQL and all product logic. |
| Expected files affected | `config/`, `apps/common/`, `tests/smoke/test_health.py`. |
| Acceptance criteria | `manage.py check` passes and `/health/live` returns the documented response. |
| Tests required | Test-client checks for response status, body, content type, and unsupported methods. |
| Completion evidence | Files changed, liveness tests added, all available repository command results, and remaining module-boundary risks. |

#### M0-T4: Add Baseline Python CI

| Field | Detail |
| --- | --- |
| Objective | Verify M0 and every later task through a clean-checkout Python CI baseline. |
| Implementation notes | Add pinned GitHub Actions steps for `uv sync`, Django system checks, Ruff lint and format checks, and the current database-independent pytest suite. |
| Expected files affected | `.github/workflows/ci.yml`, CI-only environment documentation if required. |
| Acceptance criteria | A clean CI run fails for dependency, Django check, Ruff, or pytest failures and contains no deployment behavior. |
| Tests required | Execute the complete current M0 smoke suite in CI. |
| Completion evidence | Workflow file, dependency/action rationale, green clean-checkout run, and actual local equivalent command results. |

## M1: Docker And PostgreSQL Development Environment

### Objective

Provide the required one-command local stack using the Django application and PostgreSQL.

### Resulting Capability

`docker compose up --build` starts healthy `web` and `postgres` services, applies migrations, and serves database readiness.

### Dependencies

M0.

### Expected Modules Or Files

`Dockerfile`, `compose.yaml`, `.dockerignore`, `docker/entrypoint.sh`, database settings, `.env.example`, infrastructure health probe, readiness endpoint, and CI PostgreSQL configuration.

### Acceptance Criteria

- Images build from a clean checkout.
- The application runs as a non-root container user.
- PostgreSQL health gates migration and web startup.
- `/health/ready` reports database readiness.
- Repeated starts do not corrupt or recreate schema.
- PostgreSQL is published only on a configurable loopback host port.
- Host tests use `127.0.0.1`; container commands use `postgres`; environment variables select the topology.
- Clearly labelled development-only placeholders support one-command startup, `.env` remains ignored, and production settings reject development values.
- PostgreSQL trust authentication and per-restart Django secret generation are not used.
- No production, personal, or reusable credential is committed.

### Required Tests

Container build smoke test, readiness success and failure tests, PostgreSQL connection test, and migration check.

### Verification Commands

```bash
docker compose build
docker compose up -d postgres
uv run pytest tests/integration/common
uv run python manage.py check --database default
uv run python manage.py migrate
uv run python manage.py migrate --check
docker compose up -d --build web postgres
curl --fail http://localhost:8000/health/ready
docker compose down
```

### Risks

Database startup races, architecture-specific images, local values mistaken for deployed secrets, and migrations run by multiple startup processes.

### Explicit Non-Goals

Production hosting, TLS termination, backups, replication, Kubernetes, or cloud provisioning.

### Completion Evidence

Record image build results, healthy service status, readiness response, migration output, files changed, tests changed, and remaining local-environment risks.

### Tasks

#### M1-T1: Build The Web Container

| Field | Detail |
| --- | --- |
| Objective | Package the locked Django application in a reproducible container. |
| Implementation notes | Pin the Python base image, install from the lock, use a non-root user, and exclude caches and environment files. |
| Expected files affected | `Dockerfile`, `.dockerignore`. |
| Acceptance criteria | A clean image build succeeds and the configured process does not run as root. |
| Tests required | Image-build and process-user smoke checks. |
| Completion evidence | Build output, image metadata, files changed, and base-image rationale. |

#### M1-T2: Add PostgreSQL Compose Services And Startup

| Field | Detail |
| --- | --- |
| Objective | Coordinate PostgreSQL health, migration application, and Django startup. |
| Implementation notes | Use password authentication, a PostgreSQL health check, a named development volume, loopback-only port publication, and environment-selected hostnames. Commit only clearly labelled development placeholders; document every variable in `.env.example`; require production to reject missing or development values. |
| Expected files affected | `compose.yaml`, `docker/entrypoint.sh`, `config/settings/`, `.env.example`. |
| Acceptance criteria | One command starts both services; host configuration connects through `127.0.0.1`; container configuration connects through `postgres`; repeated starts retain a stable development Django secret; trust authentication is absent. |
| Tests required | Compose startup, loopback binding, host and container database connection, production-placeholder rejection, and migration smoke tests. |
| Completion evidence | Compose status, command output, and documented local-value limitations. |

#### M1-T3: Add Database Readiness

| Field | Detail |
| --- | --- |
| Objective | Distinguish process liveness from PostgreSQL readiness. |
| Implementation notes | Keep `/health/live` database-free; implement a bounded infrastructure health probe or persistence interface; make `/health/ready` delegate to it without direct ORM or database access in the HTTP view. |
| Expected files affected | `apps/common/` infrastructure health probe, view and URLs, readiness tests. |
| Acceptance criteria | Readiness returns success when PostgreSQL is available and a safe failure when unavailable. |
| Tests required | Available and unavailable database-state tests. |
| Completion evidence | Test results and observed container health behavior. |

#### M1-T4: Extend CI With PostgreSQL And Migrations

| Field | Detail |
| --- | --- |
| Objective | Add PostgreSQL-backed checks to the existing M0 CI workflow. |
| Implementation notes | Start a fresh GitHub Actions PostgreSQL service, provide CI environment values, apply migrations to an empty database, run migration drift checks, and execute current database-backed tests. |
| Expected files affected | `.github/workflows/ci.yml`, CI settings or environment documentation. |
| Acceptance criteria | CI fails for database connectivity, unapplied migrations, model drift, or current PostgreSQL-backed test failures. |
| Tests required | M1 database readiness and migration tests in CI. |
| Completion evidence | Green PostgreSQL CI stage, service configuration, commands run, and proof that it starts from an empty database. |

## M2: TypeScript Assets And Responsive Shell

### Objective

Establish progressive TypeScript enhancement and the shared accessible page shell.

### Resulting Capability

Django serves a responsive page using versioned Vite assets, and frontend quality checks are repeatable.

### Dependencies

M0 and M1.

### Expected Modules Or Files

`package.json`, `package-lock.json`, `tsconfig.json`, Vite and formatting configuration, `frontend/src/`, `templates/base.html`, asset-template integration, pytest-Playwright configuration, browser fixtures, and CI browser setup.

### Acceptance Criteria

- Node dependencies install with `npm ci`.
- TypeScript type checks and production assets build.
- Django resolves the production asset manifest.
- pytest-Playwright owns Chromium browser execution and provides a configured live application URL.
- Screenshots and traces are retained only on browser-test failure.
- The base page has semantic landmarks, visible focus, and usable layout at 320 pixels and desktop width.
- No SPA router or global client-state store is introduced.

### Required Tests

Type checking, frontend lint and formatting, production build, asset manifest resolution, browser-harness smoke test, and responsive page-shell test.

### Verification Commands

```bash
npm ci
npm run check
npm run typecheck
npm run build
docker compose up -d postgres
uv run playwright install chromium
uv run pytest tests/smoke tests/integration/frontend
uv run pytest tests/e2e/test_browser_smoke.py
```

### Risks

Asset-path differences between local and built environments, unnecessary frontend dependencies, and accessibility regressions in the shared shell.

### Explicit Non-Goals

React, client-side routing, booking forms, administrator pages, or a component framework.

### Completion Evidence

Record Node dependency rationale, build output, template tests, responsive browser evidence, and remaining frontend integration risks.

### Tasks

#### M2-T1: Configure TypeScript And Vite

| Field | Detail |
| --- | --- |
| Objective | Produce deterministic TypeScript and CSS assets with a manifest. |
| Implementation notes | Keep entry points small, pin Node packages, use hashed production assets, and avoid runtime CDN dependencies. |
| Expected files affected | `package.json`, lock file, `tsconfig.json`, `vite.config.ts`, formatter/linter config, `frontend/src/main.ts`. |
| Acceptance criteria | Type checks, frontend checks, and production build pass. |
| Tests required | Tooling checks and production manifest assertion. |
| Completion evidence | Commands, build artifact metadata, dependencies added, and rationale. |

#### M2-T2: Integrate Assets With Django Templates

| Field | Detail |
| --- | --- |
| Objective | Resolve built assets safely in server-rendered templates. |
| Implementation notes | Provide one template helper; fail clearly when a required manifest entry is absent; do not put product behavior in the helper. |
| Expected files affected | Template-tag module, settings, `templates/base.html`, `tests/integration/frontend/`. |
| Acceptance criteria | The base template loads the expected versioned CSS and JavaScript entry. |
| Tests required | Manifest success, missing-entry failure, and template rendering tests. |
| Completion evidence | Test output and rendered-page asset inspection. |

#### M2-T3: Establish Browser-Test Infrastructure

| Field | Detail |
| --- | --- |
| Objective | Add browser-test ownership and a working Chromium smoke-test harness before browser behavior is required. |
| Implementation notes | Add pytest-Playwright as the browser integration; configure Chromium, a Django live-server or equivalent application-start fixture, one test base URL, and failure-only screenshot and trace retention. |
| Expected files affected | Python dependency lock and rationale, pytest configuration, `tests/e2e/conftest.py`, `tests/e2e/test_browser_smoke.py`, browser artifact ignore rules. |
| Acceptance criteria | `uv run playwright install chromium` and the local browser smoke command succeed against the configured application; successful runs retain no artifacts and failures retain diagnostic output. |
| Tests required | One live-server page-load smoke test and one controlled failure-policy verification where practical. |
| Completion evidence | Dependency rationale, Chromium installation command, browser configuration, smoke-test result, and artifact-policy evidence. |

#### M2-T4: Create The Accessible Page Shell

| Field | Detail |
| --- | --- |
| Objective | Provide shared navigation, messaging, form, and content structures. |
| Implementation notes | Requires M2-T3. Use semantic landmarks, skip navigation, visible focus, and mobile-first CSS. |
| Expected files affected | `templates/base.html`, shared templates, `frontend/src/styles.css`. |
| Acceptance criteria | The shell remains readable and keyboard-operable from 320 pixels through desktop width. |
| Tests required | Template semantics and responsive Chromium smoke tests. |
| Completion evidence | Passing tests and mobile and desktop browser evidence. |

#### M2-T5: Extend CI With Frontend And Browser Checks

| Field | Detail |
| --- | --- |
| Objective | Add Node, TypeScript, Vite, and browser prerequisites to the existing CI workflow. |
| Implementation notes | Use `npm ci`, run frontend checks and production build, install Chromium with Playwright's CI system dependencies, and run the browser smoke suite against the configured live application. |
| Expected files affected | `.github/workflows/ci.yml`, package scripts, browser CI configuration if required. |
| Acceptance criteria | CI fails for Node lock drift, frontend checks, Vite build, Chromium setup, or browser smoke failures. |
| Tests required | Current M2 frontend and browser suites in CI. |
| Completion evidence | Green frontend/browser CI stage, browser installation output, and failure-artifact policy confirmation. |

## M3: Clean-Checkout Integration Gate

### Objective

Verify that the incrementally introduced Python, PostgreSQL, frontend, and browser CI stages work together from a clean checkout.

### Resulting Capability

One clean-checkout workflow demonstrates that all foundation checks run together without undeclared local state.

### Dependencies

M0-T4, M1-T4, and M2-T5.

### Expected Modules Or Files

`.github/workflows/ci.yml` and only minimal CI settings or helper changes needed to integrate the existing stages.

### Acceptance Criteria

- CI uses PostgreSQL, not SQLite, for database-backed tests.
- Python and Node installations use committed locks.
- Django checks, migration drift, Ruff, pytest, TypeScript, Vite, Chromium, and browser smoke checks can fail the workflow.
- A fresh PostgreSQL service and clean application checkout are used.
- No deployment credentials or release behavior exist.

### Required Tests

All tests available through M2, executed together from a clean CI environment.

### Verification Commands

```bash
uv sync
uv run python manage.py check
uv run ruff check .
uv run ruff format --check .
npm ci
npm run check
npm run typecheck
npm run build
docker compose up -d postgres
uv run playwright install chromium
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run pytest tests/e2e/test_browser_smoke.py
```

### Risks

CI and local topology divergence, unpinned actions, unsafe cache use, hidden state between jobs, and slow feedback.

### Explicit Non-Goals

Deployment, release publishing, environment promotion, or repository branch-policy changes.

### Completion Evidence

Record the integrated workflow, local equivalent commands, a green clean-checkout run, tests executed, and remaining CI limitations.

### Tasks

#### M3-T1: Verify Integrated Clean-Checkout CI

| Field | Detail |
| --- | --- |
| Objective | Confirm that all CI capabilities introduced in M0 through M2 execute together from a clean checkout. |
| Implementation notes | Remove duplicated workflow setup, preserve pinned actions, use a fresh PostgreSQL service, and keep deployment and release behavior absent. |
| Expected files affected | `.github/workflows/ci.yml`; CI settings only if integration exposes a real inconsistency. |
| Acceptance criteria | One clean-checkout run verifies Python, PostgreSQL, migrations, frontend assets, Chromium, and the current browser smoke test. |
| Tests required | Complete current Python, frontend, database, and browser smoke suites. |
| Completion evidence | Green workflow reference, stage results, service evidence, and remaining CI risks. |

## M4: Core Persistence Schema

### Objective

Create the slot, booking, and booking-event schema with database-enforced invariants.

### Resulting Capability

PostgreSQL can persist valid appointment state and rejects invalid ranges, overlapping slots, duplicate references, and duplicate active bookings.

### Dependencies

M1 and M3. The service timezone and appointment duration are not required because the schema stores explicit UTC start and end instants.

### Expected Modules Or Files

Domain types, persistence models, repositories, migrations, database factories, and `tests/database/`.

### Acceptance Criteria

- Slot start is before slot end.
- Slots for the single resource cannot overlap; adjacent slots are permitted.
- One slot can have at most one confirmed booking.
- Cancelled history can coexist with one later confirmed booking.
- Public references and idempotency-key hashes are unique.
- Management secrets are represented only by hashes.
- Every schema change has a migration.

### Required Tests

Direct PostgreSQL constraint tests, model persistence tests, migration application, migration drift, and factory smoke tests.

### Verification Commands

```bash
docker compose up -d postgres
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate
uv run pytest tests/database
```

### Risks

Constraint semantics diverging from booking status, timezone mistakes, persistence APIs leaking ORM models into domain code, and irreversible migrations.

### Explicit Non-Goals

HTTP routes, administrator forms, booking commands, or customer pages.

### Completion Evidence

Record migration files, constraint names, direct database test results, files changed, and remaining schema risks.

### Tasks

#### M4-T1: Define Slot Domain And Persistence

| Field | Detail |
| --- | --- |
| Objective | Persist explicit open or closed appointment slots with valid non-overlapping ranges. |
| Implementation notes | Keep domain types ORM-free; map them in persistence; use timezone-aware instants and named PostgreSQL constraints. |
| Expected files affected | `apps/availability/domain.py`, `models.py`, `persistence.py`, migrations, slot database tests. |
| Acceptance criteria | Invalid and overlapping ranges fail while valid and adjacent slots persist. |
| Tests required | Check constraint, exclusion constraint, adjacency, timezone, and repository round-trip tests. |
| Completion evidence | Applied migration and passing PostgreSQL tests with named constraint evidence. |

#### M4-T2: Define Booking Occupancy And Partial Uniqueness

| Field | Detail |
| --- | --- |
| Objective | Persist current booking occupancy and enforce one confirmed booking per slot. |
| Implementation notes | Define the framework-independent booking identity and `confirmed` or `cancelled` state; persist the slot reference and public reference; add the named partial unique index for confirmed occupancy. |
| Expected files affected | `apps/bookings/domain.py`, booking model and persistence adapter, focused migration, booking occupancy database tests. |
| Acceptance criteria | PostgreSQL rejects two confirmed bookings for one slot, permits cancelled history plus one confirmed booking, and preserves foreign-key and public-reference integrity. |
| Tests required | Partial uniqueness, cancelled coexistence, slot foreign key, unique public reference, and repository round-trip tests. |
| Completion evidence | Focused migration, named constraint results, persistence-boundary review, and canonical PostgreSQL command output. |

#### M4-T3: Add Booking Events, Capability Metadata, And Idempotency Persistence

| Field | Detail |
| --- | --- |
| Objective | Persist booking history events and the metadata required for private access and idempotent creation. |
| Implementation notes | Treat rescheduling as an event, store only management-secret and idempotency-key hashes, store the request fingerprint, and keep raw values out of persistence. |
| Expected files affected | Booking event domain and model, booking metadata fields, persistence adapter, focused migration, event and metadata database tests. |
| Acceptance criteria | Creation, rescheduling, and cancellation event data persists correctly; idempotency hashes are unique; no raw capability or idempotency value is stored. |
| Tests required | Event foreign keys and round trips, unique idempotency hash, metadata nullability rules, and persisted-value redaction assertions. |
| Completion evidence | Focused migration, database test output, and inspection confirming only hashes and fingerprints are stored. |

#### M4-T4: Add Deterministic Data Factories

| Field | Detail |
| --- | --- |
| Objective | Provide concise, explicit test setup for approved slot and booking states. |
| Implementation notes | Require timezone-aware values; provide future open, future closed, past, confirmed, and cancelled variants; use synthetic contacts. |
| Expected files affected | `tests/factories/`, `tests/conftest.py`. |
| Acceptance criteria | Factories create valid isolated records and do not depend on test order or wall-clock timing. |
| Tests required | Factory smoke and isolation tests. |
| Completion evidence | Passing factory tests and examples used by database tests. |

## M5: Public Availability

### Objective

Deliver public discovery of future bookable slots.

### Resulting Capability

A customer can view future open unbooked slots with clear date, time, timezone, loading, failure, and empty states.

### Dependencies

M2 and M4. The service timezone identifier must be resolved from `TBD` before user-visible date formatting is finalized.

### Expected Modules Or Files

Availability query interfaces and persistence queries, customer views, URLs, templates, TypeScript, CSS, and availability tests.

### Acceptance Criteria

- Only future open slots without a confirmed booking are selectable.
- Public responses contain no customer data.
- Date, start, end, and timezone are explicit.
- Loading or refresh progress never presents an unconfirmed slot state as authoritative.
- Empty and load-failure states are accessible.
- Displaying a slot is not represented as a reservation.

### Required Tests

Query-state matrix, query count, HTTP response, timezone rendering, loading state, empty state, failure state, and responsive browser tests.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/availability tests/integration/availability
npm run check
npm run typecheck
docker compose up -d --build web postgres
curl --fail http://localhost:8000/appointments
```

### Risks

Stale availability, N+1 queries, timezone ambiguity, and accidental PII exposure.

### Explicit Non-Goals

Slot holds, booking submission, recurrence, waitlists, or account-specific availability.

### Completion Evidence

Record query tests, HTTP tests, mobile and desktop evidence, command results, and unresolved display risks.

### Tasks

#### M5-T1: Implement The Availability Query

| Field | Detail |
| --- | --- |
| Objective | Return the authoritative public availability read model. |
| Implementation notes | Define a query interface consumed by views; keep ORM filtering in persistence; derive occupancy from confirmed bookings. |
| Expected files affected | `apps/availability/queries.py`, `persistence.py`, unit and integration query tests. |
| Acceptance criteria | Mixed open, closed, past, confirmed, and cancelled data returns exactly the approved slots. |
| Tests required | State matrix, ordering, future range, and bounded query-count tests. |
| Completion evidence | Passing query tests and recorded query count. |

#### M5-T2: Build The Availability Page And Refresh Boundary

| Field | Detail |
| --- | --- |
| Objective | Render available slots and support accessible refresh after stale data. |
| Implementation notes | Requires M2-T3. Views call only query interfaces; group by date; include timezone; use semantic slot controls and clear loading, refresh, empty, and failure states. |
| Expected files affected | Customer views, URLs, availability template, TypeScript, CSS. |
| Acceptance criteria | Populated, loading, refresh, empty, and failure states render correctly at mobile and desktop widths without presenting stale data as confirmed availability. |
| Tests required | View, template, response-contract, loading and refresh behavior, keyboard, and responsive tests. |
| Completion evidence | Browser evidence and complete test and command results. |

## M6: Administrator Authentication And Availability Management

### Objective

Protect the administrator interface and support valid availability changes.

### Resulting Capability

The single administrator can authenticate and create, close, or reopen slots; unauthorized users and invalid transitions are rejected.

### Dependencies

M4 and M5. The approved single-administrator baseline does not require a public-deployment decision. If public exposure is selected before M6, stronger authentication requirements must be decided before this milestone is accepted.

### Expected Modules Or Files

`apps/accounts/`, `apps/admin_portal/`, availability application services and persistence adapters, forms, templates, URLs, and tests.

### Acceptance Criteria

- Administrator routes enforce server-side authorization.
- Login failures are generic and basic abuse protection is active.
- Valid future non-overlapping slots can be created.
- Future unbooked slots can be closed and reopened.
- Past, overlapping, invalid, and booked-slot closure requests leave state unchanged.

### Required Tests

Login, logout, session, CSRF, authorization, abuse protection, command transaction, persistence, form, and browser tests.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/accounts tests/integration/accounts
uv run pytest tests/unit/availability tests/integration/admin_portal
uv run python manage.py check
```

### Risks

Hardcoded credentials, authorization applied only in templates, conflict logic placed in routes, or lock conventions incompatible with booking creation.

### Explicit Non-Goals

Multiple administrators, role management, MFA, password recovery, or administrator booking cancellation.

### Completion Evidence

Record security and command tests, credentials configuration review, browser evidence, command results, and remaining authentication risks.

### Tasks

#### M6-T1: Add Administrator Login, Logout, Sessions, And Authorization

| Field | Detail |
| --- | --- |
| Objective | Provide administrator login, logout, protected sessions, and server-side staff authorization. |
| Implementation notes | Use Django authentication, rotate sessions after login, use generic credential errors, and enforce staff authorization independently of templates. Bootstrap and abuse protection are deferred to M6-T2. |
| Expected files affected | `apps/accounts/`, authentication templates, settings, URLs, session and authorization tests. |
| Acceptance criteria | Valid staff access succeeds; anonymous, invalid, expired, and non-staff access fails safely; logout invalidates the session. |
| Tests required | Login success and generic failure, logout, expiry, fixation, CSRF, and staff authorization tests. |
| Completion evidence | Authentication and authorization test results, files changed, and available command results. |

#### M6-T2: Add Administrator Bootstrap Configuration And Login Abuse Protection

| Field | Detail |
| --- | --- |
| Objective | Provide repeatable administrator bootstrap configuration and bounded login abuse protection. |
| Implementation notes | Read bootstrap values only from environment configuration; document development placeholders without committing a real credential; reject development values in production; add basic login throttling without disclosing account state. |
| Expected files affected | Account bootstrap management command or service, settings, `.env.example`, login protection adapter, focused tests. |
| Acceptance criteria | Bootstrap is repeatable, no real credential is committed, production rejects development placeholders, and repeated failures activate generic abuse protection. |
| Tests required | Missing configuration, development and production validation, idempotent bootstrap, throttling threshold, recovery window, and generic response tests. |
| Completion evidence | Configuration review, secret-scan inspection, abuse-protection tests, and command results. |

#### M6-T3: Implement Availability Commands

| Field | Detail |
| --- | --- |
| Objective | Create framework-independent services for slot creation, closure, and reopening. |
| Implementation notes | Services use persistence interfaces and short transactions; closure locks the slot and rejects a confirmed booking. |
| Expected files affected | Availability services, persistence methods, domain errors, command tests. |
| Acceptance criteria | Each valid command commits once and each invalid command leaves prior state intact. |
| Tests required | Valid transitions, overlap, past range, booked closure, repeated operation, and rollback tests. |
| Completion evidence | Service and PostgreSQL test results with state assertions. |

#### M6-T4: Build The Administrator Availability UI

| Field | Detail |
| --- | --- |
| Objective | Expose availability commands through protected accessible pages. |
| Implementation notes | Requires M2-T3, M6-T1, M6-T2, and M6-T3. Views call services and queries only; distinguish open, closed, booked, and past states; preserve valid form input after errors. |
| Expected files affected | `apps/admin_portal/`, templates, URLs, TypeScript, CSS, HTTP and browser tests. |
| Acceptance criteria | The administrator completes every supported action and receives clear rejection messages for invalid actions. |
| Tests required | Authorization, CSRF, form, response, error-state, and end-to-end tests. |
| Completion evidence | Browser evidence and complete verification results. |

## M7: Concurrent Booking Creation

### Objective

Deliver the core booking workflow with database-enforced uniqueness and safe retry behavior.

### Resulting Capability

A customer can create and confirm a booking. Simultaneous requests for one slot produce exactly one confirmed booking, and duplicate delivery of one request produces one effect.

### Dependencies

M4 through M6. The standard duration is not required because customers select explicit slots.

### Expected Modules Or Files

Booking application services, persistence operations, idempotency support and redaction, minimum shared booking error mapping, customer forms and views, booking TypeScript, confirmation template, and concurrency tests.

### Acceptance Criteria

- Valid creation writes one confirmed booking and one creation event atomically.
- The selected slot is locked and revalidated inside a short transaction.
- PostgreSQL's named partial unique index remains the final invariant.
- First success returns `201`; an identical replay returns the existing booking; a competing request returns `409 slot_unavailable`.
- Changed input with the same idempotency identity returns `409 idempotency_key_reused`.
- Raw idempotency values do not appear in application logs.
- Booking request bodies and raw management secrets are not logged before the reusable M8 capability redactor is introduced.
- Confirmation appears only after commit.
- Two simultaneous independent requests leave one confirmed booking and one creation event.

### Required Tests

Domain and service behavior, transaction rollback, direct constraint violation, deterministic database race, service race, HTTP race, idempotent race, changed-payload reuse, idempotency-log redaction, booking versus slot closure, and UI conflict handling.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/bookings/test_creation.py
uv run pytest tests/integration/bookings/test_creation.py
uv run pytest tests/database/test_booking_constraints.py
uv run pytest tests/concurrency/test_booking_creation.py
uv run pytest tests/e2e/test_booking_creation.py
npm run check
npm run typecheck
```

### Risks

Check-then-insert races, broad integrity-error handling, long-held locks, idempotency key misuse, false success before commit, and flaky concurrency tests.

### Explicit Non-Goals

Cancellation, rescheduling, customer history, email delivery, waitlists, or temporary slot holds.

### Completion Evidence

Record transaction and constraint design, all race outcomes, final database row counts, HTTP and browser results, commands, files changed, and remaining concurrency risks.

### Tasks

#### M7-T1: Implement Transactional Booking Creation Service

| Field | Detail |
| --- | --- |
| Objective | Atomically create a confirmed booking and creation event. |
| Implementation notes | Validate immutable input before the transaction; lock and re-read the slot inside it; keep ORM in persistence; commit before returning. |
| Expected files affected | Booking domain errors and types, creation service, persistence adapter, unit and integration tests. |
| Acceptance criteria | Valid creation commits both records; every failure leaves neither partial booking nor partial event. |
| Tests required | Success, closed, past, occupied, event failure rollback, and recognized constraint mapping. |
| Completion evidence | Service test output and exact database state before and after rollback. |

#### M7-T2: Add Safe Idempotency

| Field | Detail |
| --- | --- |
| Objective | Recover a committed booking after a duplicate or uncertain request without creating another effect. |
| Implementation notes | Hash the key, store a canonical request fingerprint, recheck after lock wait, verify the management secret on replay, reject changed data, and redact raw idempotency values from logs when they first enter the system. |
| Expected files affected | Idempotency domain helper, booking service and persistence, minimum shared logging redaction, tests. |
| Acceptance criteria | Identical retries return one booking and one event; different requests cannot share a key; captured logs contain no raw idempotency value. |
| Tests required | Sequential and concurrent replay, changed payload, rollback then retry, replay after current-state change, and log-capture redaction. |
| Completion evidence | Stable booking-reference and row-count assertions for every replay scenario. |

#### M7-T3: Add The Server-Side Booking HTTP Contract

| Field | Detail |
| --- | --- |
| Objective | Connect validated booking input to the application service and expose stable server responses. |
| Implementation notes | Add the minimum shared mapping from booking domain and named database errors to `201`, replay `200`, validation responses, `409 slot_unavailable`, `409 idempotency_key_reused`, and retryable temporary failure; keep conflict logic out of the route; prohibit request-body and raw management-secret logging at this boundary. |
| Expected files affected | Customer booking form, views and URLs, common booking error mapper, HTTP integration tests. |
| Acceptance criteria | The server contract matches approved status and error codes, CSRF is enforced, unknown integrity errors are not mislabeled, no response claims success before commit, and captured logs contain neither the request body nor raw management secret. |
| Tests required | Input validation, CSRF, first success, replay, each expected conflict, temporary failure, unknown integrity error, response-body contract, and booking-request log-capture tests. |
| Completion evidence | HTTP contract tests, error-mapping review, files changed, and canonical PostgreSQL command results. |

#### M7-T4: Add Browser Retry, Conflict, And Confirmation Behavior

| Field | Detail |
| --- | --- |
| Objective | Provide the customer booking form, safe uncertain-outcome retry, conflict recovery, and committed confirmation UI. |
| Implementation notes | Requires M2-T3 and M7-T3. Generate separate high-entropy idempotency and management values with Web Crypto, retain them across uncertain retries, preserve contact input after conflict, refresh alternatives, and render confirmation only after success. |
| Expected files affected | Booking and confirmation templates, booking TypeScript, CSS, frontend and browser tests. |
| Acceptance criteria | Pending, validation, conflict, uncertain, replay, and confirmed states behave as approved; a new slot selection receives a new booking intent. |
| Tests required | Frontend state tests and Chromium tests for success, duplicate click, lost response retry, slot conflict, input preservation, and confirmation. |
| Completion evidence | Browser results for booking and conflict flows, frontend command results, and remaining retry risks. |

#### M7-T5: Prove Concurrency Guarantees

| Field | Detail |
| --- | --- |
| Objective | Demonstrate that database and application behavior prevent concurrent duplicates. |
| Implementation notes | Use independent PostgreSQL connections and barriers; avoid sleeps; inspect named constraints and final state. |
| Expected files affected | `tests/concurrency/`, concurrency fixtures, relevant CI configuration. |
| Acceptance criteria | Independent requests produce one success and one conflict; identical requests produce one creation and one replay; all final states are consistent. |
| Tests required | Direct insert, low-level race, service race, HTTP race, idempotent race, and slot-closure race. |
| Completion evidence | Repeatable concurrency output and database assertions showing exactly one confirmed booking. |

## M8: Customer Booking Access

### Objective

Allow a customer to return securely to one booking without an account.

### Resulting Capability

A valid management credential establishes a booking-scoped session and displays the booking; invalid credentials reveal no booking existence.

### Dependencies

M7. Lost-access recovery remains `TBD` and is not part of this milestone.

### Expected Modules Or Files

`apps/booking_access/`, customer detail query and view, credential exchange endpoint, booking-scoped session helper, templates, TypeScript, and security tests.

### Acceptance Criteria

- A management secret is exchanged through POST, not sent to the server as a URL query or path value.
- Stored booking data contains only a one-way credential hash.
- Access is scoped to one booking.
- Invalid, malformed, and cross-booking credentials produce one generic response.
- Raw credentials do not appear in logs.
- Credential exchange has basic abuse protection without disclosing booking existence.

### Required Tests

Credential hash verification, exchange, scoped access, cross-booking denial, CSRF, session rotation, generic failure, abuse protection, log redaction, and browser return-link flow.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/booking_access
uv run pytest tests/integration/booking_access
uv run pytest tests/e2e/test_booking_access.py
```

### Risks

Credential leakage, session fixation, customer and administrator session confusion, and different errors exposing booking existence.

### Explicit Non-Goals

Customer accounts, email recovery, account-wide history, or credential sharing features.

### Completion Evidence

Record security tests, log inspection, browser flow, files changed, commands, and the remaining lost-access limitation.

### Tasks

#### M8-T1: Implement Management-Credential Verification And Redaction

| Field | Detail |
| --- | --- |
| Objective | Verify a capability secret against one booking without storing or logging the raw value. |
| Implementation notes | Keep credential persistence behind an interface, use constant-time verification where applicable, return one generic invalid result, and add management-secret and capability redaction when these values first enter the application. |
| Expected files affected | `apps/booking_access/` verification service and persistence interface, shared sensitive-value redaction, focused tests. |
| Acceptance criteria | Valid verification identifies only its booking; invalid, malformed, and cross-booking values fail uniformly; no raw capability appears in persistence or captured logs. |
| Tests required | Valid, invalid, malformed, cross-booking, constant-result-shape, persistence inspection, and log-capture redaction tests. |
| Completion evidence | Verification and redaction tests, stored-value inspection, files changed, and command results. |

#### M8-T2: Add Scoped-Session Exchange And Security Behavior

| Field | Detail |
| --- | --- |
| Objective | Exchange successful credential verification for a session authorized to one booking. |
| Implementation notes | Accept the secret through a CSRF-protected POST body, rotate the session, record only the authorized booking scope, apply expiry and basic abuse protection, and keep administrator sessions separate. Abuse responses remain generic. |
| Expected files affected | Booking-access view and URL, scoped-session helper, abuse-protection adapter, settings, HTTP security tests. |
| Acceptance criteria | Valid exchange creates one scoped session; CSRF, fixation, expiry, throttling, invalid access, and attempts to access another booking fail safely without existence disclosure. |
| Tests required | Exchange success, CSRF, session rotation, expiry, abuse threshold and recovery, cross-booking denial, administrator-session separation, and generic failure tests. |
| Completion evidence | Session security tests, HTTP contract results, and remaining access risks. |

#### M8-T3: Build The Booking Detail And Return Flow

| Field | Detail |
| --- | --- |
| Objective | Display current booking details after creation or later capability exchange. |
| Implementation notes | Requires M2-T3, M8-T1, and M8-T2. Carry the initial secret in the browser URL fragment and exchange it by POST; show reference, status, date, time, timezone, and allowed actions. |
| Expected files affected | Customer views, templates, URLs, booking-access TypeScript, browser tests. |
| Acceptance criteria | The customer can revisit a booking and sees clear confirmed, cancelled, and past states. |
| Tests required | Detail rendering, fragment exchange, invalid link, expired session, and responsive browser tests. |
| Completion evidence | End-to-end return flow and full command results. |

## M9: Booking Cancellation

### Objective

Allow an authorized customer to cancel a future booking safely and release its slot.

### Resulting Capability

A confirmed booking becomes cancelled with one history event, and its future open slot returns to availability.

### Dependencies

M7 and M8.

### Expected Modules Or Files

Cancellation domain service and persistence method, customer HTTP boundary, confirmation template, detail-page state, TypeScript, and tests.

### Acceptance Criteria

- Cancellation locks the booking and uses server time.
- Status and event commit atomically.
- Repeated cancellation does not create another event.
- Past and unauthorized bookings cannot be cancelled.
- A future open slot returns to public availability.

### Required Tests

Unit transition tests, persistence transaction tests, repeated and concurrent cancellation, authorization, CSRF, availability reappearance, and browser journey.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/bookings/test_cancellation.py
uv run pytest tests/integration/bookings/test_cancellation.py
uv run pytest tests/concurrency/test_cancellation.py
uv run pytest tests/e2e/test_cancellation.py
```

### Risks

Duplicate events, cancellation at the exact start boundary, stale UI state, and occupancy not being released correctly.

### Explicit Non-Goals

Administrator cancellation, fees, notifications, deletion, or retention changes.

### Completion Evidence

Record exact event counts, availability results, concurrency outcome, browser evidence, command results, and boundary risks.

### Tasks

#### M9-T1: Implement Transactional Cancellation

| Field | Detail |
| --- | --- |
| Objective | Change one authorized future confirmed booking to cancelled and append one event. |
| Implementation notes | Lock the booking, compare with injected server time, and write state and event through persistence in one transaction. |
| Expected files affected | Cancellation service, persistence adapter, domain errors, unit and integration tests. |
| Acceptance criteria | Valid cancellation commits once; invalid states make no change. |
| Tests required | Success, repeated, already cancelled, exact start, past, event rollback, and concurrent requests. |
| Completion evidence | State and event-count assertions with commands and results. |

#### M9-T2: Add Cancellation HTTP And UI Flow

| Field | Detail |
| --- | --- |
| Objective | Provide an authorized confirmation step and clear cancelled state. |
| Implementation notes | Requires M2-T3. Require POST and CSRF; disable unavailable actions; refresh public availability after success. |
| Expected files affected | Customer views, URLs, cancellation template, booking detail template, TypeScript, HTTP and browser tests. |
| Acceptance criteria | Authorized cancellation works end to end and invalid transitions show the approved state without false success. |
| Tests required | Authorization, CSRF, response mapping, template state, and end-to-end cancellation. |
| Completion evidence | Demonstrated cancellation and returned availability with command results. |

## M10: Atomic Rescheduling

### Objective

Move a booking to a new slot without risking loss of the original appointment.

### Resulting Capability

An authorized customer can select an alternative slot; success updates the existing booking and failure preserves its original slot.

### Dependencies

M7 through M9.

### Expected Modules Or Files

Alternative-slot query, rescheduling service and persistence, customer views and templates, TypeScript, and concurrency tests.

### Acceptance Criteria

- The service locks the booking and target slot in a documented order.
- Target validation occurs after locking.
- Success preserves booking identity and contact information and appends one old-to-new event.
- Target conflict returns `409` and leaves the original booking and history unchanged.
- Past, cancelled, unauthorized, and same-slot requests fail safely.

### Required Tests

Unit transitions, transaction rollback, target uniqueness, HTTP contract, empty alternatives, two-reschedule race, booking-versus-reschedule, cancellation-versus-reschedule, and browser flows.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/bookings/test_rescheduling.py
uv run pytest tests/integration/bookings/test_rescheduling.py
uv run pytest tests/concurrency/test_rescheduling.py
uv run pytest tests/e2e/test_rescheduling.py
```

### Risks

Releasing the original slot too early, deadlocks, duplicate events, stale alternatives, and conflict errors that obscure the retained original booking.

### Explicit Non-Goals

Contact editing, recurring bookings, waitlists, service changes, or rescheduling past and cancelled records.

### Completion Evidence

Record successful and losing race outcomes, original-booking preservation, event details, files, commands, and remaining lock risks.

### Tasks

#### M10-T1: Implement Alternative-Slot Query

| Field | Detail |
| --- | --- |
| Objective | Return valid alternatives excluding the current and unavailable slots. |
| Implementation notes | Reuse availability semantics through a query interface; do not treat results as reservations. |
| Expected files affected | Availability and booking query interfaces, persistence query, tests. |
| Acceptance criteria | Only future open unbooked alternatives are returned and the current slot is excluded. |
| Tests required | Mixed-state, no-alternative, ordering, and query-count tests. |
| Completion evidence | Passing query tests and query-count record. |

#### M10-T2: Implement Transactional Rescheduling

| Field | Detail |
| --- | --- |
| Objective | Atomically move the current booking and append its old-to-new event. |
| Implementation notes | Lock booking then target slot in the approved order; update and append in one transaction; let the partial unique index arbitrate target races. |
| Expected files affected | Rescheduling service, persistence adapter, domain errors, tests. |
| Acceptance criteria | Failure at any point preserves the original booking and creates no event. |
| Tests required | Success, target conflict, closed/past/same target, event failure, and rollback tests. |
| Completion evidence | Before-and-after database assertions and command results. |

#### M10-T3: Build Rescheduling HTTP And UI Flow

| Field | Detail |
| --- | --- |
| Objective | Let customers choose and confirm an alternative while clearly retaining the original on failure. |
| Implementation notes | Requires M2-T3. Refresh alternatives after conflicts; never optimistically show the new appointment; preserve the original booking display. |
| Expected files affected | Customer views, URLs, rescheduling template, TypeScript, HTTP and browser tests. |
| Acceptance criteria | Success displays the new slot; conflict displays the unchanged original and refreshed alternatives. |
| Tests required | Authorization, CSRF, contract, empty state, conflict state, and browser journey. |
| Completion evidence | Successful and conflict browser evidence with verification results. |

#### M10-T4: Prove Cross-Operation Concurrency

| Field | Detail |
| --- | --- |
| Objective | Verify rescheduling remains atomic against competing mutations. |
| Implementation notes | Use separate PostgreSQL connections, explicit barriers, and final-state assertions. |
| Expected files affected | `tests/concurrency/test_rescheduling.py`, fixtures. |
| Acceptance criteria | Every race has one valid final state, no duplicate active booking, and no partial history. |
| Tests required | Two reschedules, booking versus reschedule, and cancellation versus reschedule. |
| Completion evidence | Repeatable race results and exact row and event counts. |

## M11: Booking History

### Objective

Expose authorized customer history and administrator-wide booking oversight.

### Resulting Capability

Customers can view events for one authorized booking, and the administrator can inspect paginated and filtered current and historical bookings.

### Dependencies

M6 and M8 through M10.

### Expected Modules Or Files

History query interfaces and persistence, customer timeline, administrator list and detail views, filters, templates, and tests.

### Acceptance Criteria

- Events display in correct chronological order with accurate old and new times.
- Customers see only their authorized booking.
- Administrator history is protected, reverse chronological, filterable, and paginated at the approved default.
- Empty results show explicit states.
- Queries avoid N+1 behavior.

### Required Tests

Query correctness, event ordering, derived past state, authorization, PII boundaries, filtering, pagination, empty state, query count, and browser tests.

### Verification Commands

```bash
docker compose up -d postgres
uv run pytest tests/unit/bookings/test_history.py
uv run pytest tests/integration/history
uv run pytest tests/e2e/test_booking_history.py
```

### Risks

PII leakage, history/current-state disagreement, inefficient pagination, and customer access widening beyond one booking.

### Explicit Non-Goals

CSV export, analytics, deletion, account-wide customer search, or customer lookup by email alone.

### Completion Evidence

Record authorization and query-count results, customer and administrator browser evidence, commands, files, and remaining history risks.

### Tasks

#### M11-T1: Implement The Customer History Query

| Field | Detail |
| --- | --- |
| Objective | Produce the history read model for one authorized customer booking. |
| Implementation notes | Keep ORM access in a persistence query, scope by the authorized booking identity, derive past display from server time, and preload the booking's events and slots. |
| Expected files affected | Customer history query interface and persistence query, focused unit and integration tests. |
| Acceptance criteria | One authorized booking returns correctly ordered current state and events without exposing any other booking and within a bounded query count. |
| Tests required | Event ordering, current status, past derivation, cross-booking isolation, and query-count tests. |
| Completion evidence | Customer query tests, authorization-state assertions, and recorded query count. |

#### M11-T2: Implement Administrator History Filtering And Pagination

| Field | Detail |
| --- | --- |
| Objective | Produce the protected administrator history read model with filters and pagination. |
| Implementation notes | Keep filtering, ordering, relation loading, and pagination in the persistence query; preserve the approved default page size and validate filter inputs. |
| Expected files affected | Administrator history query interface and persistence query, focused unit and integration tests. |
| Acceptance criteria | Results are reverse chronological, filterable, paginated, and bounded in query count; invalid filters do not expose data or create unbounded queries. |
| Tests required | Date and status filters, empty results, first and final page boundaries, invalid filters, deterministic ordering, and query count. |
| Completion evidence | Administrator query tests, page-boundary results, and recorded query count. |

#### M11-T3: Add Customer Booking Timeline

| Field | Detail |
| --- | --- |
| Objective | Display creation, rescheduling, and cancellation for one authorized booking. |
| Implementation notes | Requires M2-T3 and M11-T1. Show user-relevant timestamps and old/new slots without internal IDs or unrelated actor data. |
| Expected files affected | Customer booking view, timeline template, CSS, tests. |
| Acceptance criteria | Only authorized events appear and creation-only history is clear. |
| Tests required | Authorization, event rendering, escaping, and responsive tests. |
| Completion evidence | Rendered examples for every approved event type and passing tests. |

#### M11-T4: Add Administrator History Pages

| Field | Detail |
| --- | --- |
| Objective | Provide protected list, filtering, pagination, empty state, and booking detail. |
| Implementation notes | Requires M2-T3 and M11-T2. Views consume query interfaces only; preserve filter parameters through pagination. |
| Expected files affected | Admin views, URLs, forms, history templates, HTTP and browser tests. |
| Acceptance criteria | Administrator history works for populated, filtered, paginated, and empty results; unauthorized access fails. |
| Tests required | Authentication, filtering, pagination, escaping, empty state, and browser flow. |
| Completion evidence | Browser evidence and full verification results. |

## M12: Cross-Cutting Product Hardening

### Objective

Audit and consolidate system-wide error, security, responsive, accessibility, and test-stability behavior already introduced with the relevant features.

### Resulting Capability

The complete product behaves consistently across mobile and desktop, exposes safe errors, protects sensitive logs, and passes deterministic end-to-end and concurrency suites.

### Dependencies

M0 through M11.

### Expected Modules Or Files

Consolidated error mapping, correlation-ID middleware, logging and redaction audit, security settings, shared templates and CSS, end-to-end fixtures, accessibility checks, and CI adjustments.

### Acceptance Criteria

- Expected domain errors map to stable HTTP and UI states.
- Unexpected errors reveal no internal details.
- Logs contain no raw credentials, idempotency values, cookies, or unnecessary contact data.
- Core flows work by keyboard at 320-pixel and desktop widths.
- Status is not communicated by color alone.
- Critical concurrency tests pass repeatedly without timing sleeps.

### Required Tests

Error response and template tests, logging capture, security headers and sessions, keyboard and responsive browser tests, automated accessibility checks, repeated concurrency suites, and full regression.

### Verification Commands

```bash
docker compose up -d postgres
uv run playwright install chromium
uv run ruff check .
uv run ruff format --check .
uv run python manage.py makemigrations --check --dry-run
uv run pytest
npm run check
npm run typecheck
npm run build
uv run pytest tests/e2e
```

### Risks

Masking unexpected exceptions, flaky browser checks, environment-specific security behavior, and hardening changes accidentally altering product behavior.

### Explicit Non-Goals

External observability vendors, penetration-testing certification, unsupported-browser support, production scaling, or new product features.

### Completion Evidence

Record full-suite output, redacted log examples, accessibility and responsive evidence, repeated race results, files changed, and residual risks.

### Tasks

#### M12-T1: Audit And Consolidate Error Mapping

| Field | Detail |
| --- | --- |
| Objective | Consolidate feature-level error mappings and verify consistent safe HTTP and UI behavior. |
| Implementation notes | Requires M7-T3. Reuse the booking mapping already introduced, add missing mappings from later features, recognize database conflicts only by named constraint, and keep unknown failures generic. |
| Expected files affected | Common error mapper and error templates, feature adapters needing consolidation, focused tests. |
| Acceptance criteria | Approved 400, 403, 404, 409, 500, and 503 outcomes are consistent; unknown integrity errors are not mislabeled; unexpected failures expose no internals. |
| Tests required | Cross-feature status and error-code matrix, named-constraint behavior, unknown error, and safe template tests. |
| Completion evidence | Error-contract matrix, focused test results, and list of consolidated mappings. |

#### M12-T2: Add Correlation IDs

| Field | Detail |
| --- | --- |
| Objective | Add one safe request correlation identifier to responses and diagnostic logs. |
| Implementation notes | Generate or validate a bounded identifier, include it in responses and logs, and do not treat it as authentication or expose sensitive request data. |
| Expected files affected | Common middleware, logging context configuration, focused tests. |
| Acceptance criteria | Every request receives a valid correlation ID, malformed incoming values are replaced safely, and error responses remain traceable without leaking data. |
| Tests required | Generated, accepted, rejected, response-header, and log-context tests. |
| Completion evidence | Middleware tests, representative safe log output, and command results. |

#### M12-T3: Audit Logging And Redaction

| Field | Detail |
| --- | --- |
| Objective | Verify and consolidate redaction across all sensitive values introduced by earlier features. |
| Implementation notes | Requires M7-T2 and M8-T1. Audit existing idempotency and capability redaction, then cover passwords, cookies, contact data, and any remaining structured-log fields without replacing feature-level protections. |
| Expected files affected | Shared logging filters and settings, feature redaction adapters only where gaps exist, log-capture tests. |
| Acceptance criteria | Captured normal and error logs contain no raw password, management secret, idempotency value, cookie, or unnecessary contact data. |
| Tests required | Structured and plain log capture across login, booking, access exchange, conflict, and unexpected error paths. |
| Completion evidence | Redaction matrix, representative sanitized logs, test results, and remaining logging risks. |

#### M12-T4: Complete Responsive And Accessibility Verification

| Field | Detail |
| --- | --- |
| Objective | Verify every primary journey using keyboard, mobile, and desktop interactions. |
| Implementation notes | Requires M2-T3. Select by role and label; test focus after errors; use automated accessibility checks as support rather than the only assertion. |
| Expected files affected | Shared templates and CSS where remediation is needed, `tests/e2e/`, browser configuration. |
| Acceptance criteria | All core journeys are usable at approved widths with no critical automated accessibility finding. |
| Tests required | Keyboard, focus, mobile, desktop, and accessibility browser tests. |
| Completion evidence | Browser-suite output and failure-only trace configuration. |

#### M12-T5: Stabilize Full-System Verification

| Field | Detail |
| --- | --- |
| Objective | Make the complete suite deterministic for clean-checkout CI. |
| Implementation notes | Replace sleeps with barriers or observable states; isolate test data; retain final database assertions. |
| Expected files affected | Test fixtures, concurrency helpers, CI workflow only where required. |
| Acceptance criteria | Consecutive full and concurrency suites pass against clean PostgreSQL databases. |
| Tests required | Full regression and repeated critical races. |
| Completion evidence | Multiple consecutive green runs and documented remaining flaky-test risk, if any. |

## M13: Documentation And Independent Release Verification

### Objective

Prove the definition of done from a clean checkout and obtain an independent code review with no unresolved critical finding.

### Resulting Capability

Another engineer can start, use, test, and understand the application using repository documentation alone, and the release candidate has independent verification.

### Dependencies

All preceding milestones. Personal-data retention and public-deployment `TBD` items must be called out as deployment blockers if still unresolved.

### Expected Modules Or Files

`README.md`, updates to `docs/`, final experiment record, and an independent review report.

### Acceptance Criteria

- `docker compose up --build` works from a clean checkout with one documented command.
- README documents setup, architecture, usage, migrations, tests, security assumptions, and troubleshooting.
- All required quality commands and CI pass.
- The experiment record covers every required category.
- Independent review records severity, evidence, and disposition for every finding.
- No critical finding remains open.

### Required Tests

Clean-checkout startup, migration application, full regression, concurrency, end-to-end, documentation command review, and targeted regression for every corrected review defect.

### Verification Commands

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
npm ci
npm run check
npm run typecheck
npm run build
docker compose up -d postgres
uv run playwright install chromium
uv run pytest
docker compose up -d --build
curl --fail http://localhost:8000/health/ready
docker compose exec web python manage.py migrate --check
docker compose exec web python manage.py check --database default
docker compose down
```

### Risks

Documentation drift, incomplete traceability, non-independent review, unresolved critical defects, or unrecorded deployment limitations.

### Explicit Non-Goals

Production deployment, marketing material, formal compliance certification, or adding features during release review.

### Completion Evidence

Provide the clean-checkout transcript, green CI reference, final test results, documentation review, independent review report, resolved-finding evidence, and explicit residual risks.

### Tasks

#### M13-T1: Complete Setup, Architecture, And Usage Documentation

| Field | Detail |
| --- | --- |
| Objective | Make all setup and operational knowledge explicit and executable. |
| Implementation notes | Document one-command startup, local administrator setup, customer and administrator use, migrations, test layers, concurrency, and troubleshooting. |
| Expected files affected | `README.md`, architecture and testing documentation where implementation differs from assumptions. |
| Acceptance criteria | A reviewer follows the documentation from a clean checkout without undocumented steps. |
| Tests required | Execute every documented command and review internal links. |
| Completion evidence | Clean-checkout transcript and reviewer confirmation. |

#### M13-T2: Finalize Experiment Traceability

| Field | Detail |
| --- | --- |
| Objective | Reconcile all prompts, failures, interventions, manual changes, defects, and architectural changes. |
| Implementation notes | Use `none` for empty categories and remove secrets or unnecessary personal information. |
| Expected files affected | `docs/experiment-log.md`. |
| Acceptance criteria | Every required category is chronologically complete and reviewable. |
| Tests required | Documentation review against experiment criteria. |
| Completion evidence | Signed-off traceability review and unresolved items, if any. |

#### M13-T3: Perform Independent Code Review

| Field | Detail |
| --- | --- |
| Objective | Identify correctness, security, data-integrity, migration, and test-validity defects independently. |
| Implementation notes | The reviewer focuses on transaction boundaries, named constraints, lock order, authorization, capability handling, logging, and whether tests prove behavior. |
| Expected files affected | Independent review report; no implementation files unless a separate remediation task is approved. |
| Acceptance criteria | Every finding has severity and evidence; no critical finding remains unresolved. |
| Tests required | Targeted regression tests for each remediation plus the full suite. |
| Completion evidence | Review report, remediation references, and green CI after fixes. |

#### M13-T4: Execute Final Clean-Checkout Verification

| Field | Detail |
| --- | --- |
| Objective | Demonstrate the release candidate meets the complete definition of done. |
| Implementation notes | Use a clean workspace and empty PostgreSQL volume; execute documented commands without local undeclared dependencies. |
| Expected files affected | None unless verification reveals a separately tracked defect. |
| Acceptance criteria | One-command startup, migrations, all checks, all tests, and CI succeed; remaining `TBD` items are explicitly documented. |
| Tests required | Complete unit, integration, database, concurrency, end-to-end, and smoke suites. |
| Completion evidence | Final transcript, CI reference, review status, and residual-risk statement. |
