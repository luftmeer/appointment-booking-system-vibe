# ADR 001: Technology Stack

## Status

Accepted.

## Context

The product is a small appointment-booking application for customers and one administrator. It requires a Python backend, PostgreSQL, a modern JavaScript or TypeScript frontend, Docker Compose, pytest, and GitHub Actions. It must provide secure sessions, server validation, migrations, responsive pages, and database-enforced concurrency integrity.

The architecture should remain proportional to the scope and minimize deployment and state-synchronization complexity.

## Considered Alternatives

### Django Modular Monolith With Server-Rendered Pages

One Django application provides templates, forms, sessions, authentication, CSRF protection, migrations, and application services. Small TypeScript modules enhance interactions.

### FastAPI API With React SPA

FastAPI exposes a versioned REST API to a separate React and TypeScript application. This offers a richer client architecture but adds client caching, API contract, authentication, and build complexity.

### PostgreSQL-Centric Command Layer

A thin Python API delegates mutations to PostgreSQL functions. This centralizes consistency but splits domain logic between Python and SQL and increases migration and skills complexity.

## Decision

Use an integrated Django modular monolith with:

- Python 3.12 and Django 5.2 LTS.
- Server-rendered Django templates.
- Small TypeScript modules built with Vite.
- PostgreSQL 16 accessed through Django ORM persistence adapters.
- `uv`, Ruff, pytest, and Playwright.
- Docker Compose for local execution.
- GitHub Actions for CI.

Domain rules remain independent of Django. Database access remains in persistence repositories and query objects. HTTP views delegate to application services.

## Rationale

- It has the fewest deployable components that satisfy all requirements.
- Django supplies secure defaults for forms, sessions, CSRF, and administrator authentication.
- Server rendering avoids unnecessary SPA server-state synchronization.
- PostgreSQL-specific constraints remain available through migrations.
- The modular boundary supports isolated domain tests without introducing services or queues.
- The stack directly supports the repository's required commands and architecture rules.

## Consequences

- The repository contains both Python and a small Node-based asset toolchain.
- The UI is less SPA-like but remains responsive and progressively enhanced.
- Developers must actively prevent Django ORM models and HTTP views from absorbing domain logic.
- External clients would require an additional API boundary later; none is currently required.
- PostgreSQL is required for meaningful integration and concurrency tests.

## Known Risks

- Business rules may drift into views or ORM models if boundaries are not reviewed.
- Vite manifest integration can differ between local and built environments.
- Teams expecting React may perceive server rendering as less familiar.
- Exact service timezone, appointment duration, data retention, and public deployment exposure remain `TBD` product decisions.
