# Experiment Log

## Purpose

Record the planning and implementation process without inventing dates, outcomes, or interventions. Exact historical timestamps are marked `unknown` where they are not available.

## Current State

- Phase: planning and pre-implementation correction.
- Application code created: none.
- Dependencies installed: none recorded.
- Database migrations created: none.
- Manual code changes: none recorded.

## Planning History

### Entry P-001: Project Charter

- Date and time: `unknown`.
- Prompt or request: Create a small appointment-booking web application for customers and one administrator, including booking, cancellation, rescheduling, availability management, history, responsive UI, tests, Docker Compose, and CI.
- Outcome: Project purpose, constraints, quality requirements, non-goals, definition of done, and experiment criteria were established.
- Failed attempts: none.
- Human intervention: the project charter was supplied by the human.
- Manual code changes: none.
- Defects found after completion: none recorded for this entry.
- Architectural changes after implementation began: none; implementation had not begun.

### Entry P-002: Product And Requirements Planning

- Date and time: `unknown`.
- Prompt or request: Produce a product specification from the charter without implementation tasks.
- Outcome: Product goal, roles, journeys, requirements, business rules, edge and error states, non-goals, acceptance criteria, assumptions, and unresolved decisions were defined.
- Failed attempts: none.
- Human intervention: the planning output was approved as the product baseline.
- Manual code changes: none.
- Defects found after completion: unresolved product decisions were explicitly retained rather than silently guessed.
- Architectural changes after implementation began: none; implementation had not begun.

### Entry P-003: Architecture Alternatives And Selection

- Date and time: `unknown`.
- Prompt or request: Propose three proportional architectures and recommend the simplest option satisfying database-enforced concurrency integrity.
- Outcome: Django modular monolith, FastAPI with a React SPA, and PostgreSQL-centric command alternatives were considered.
- Failed attempts: none.
- Human intervention: the human selected Approach 1, the integrated Django modular monolith.
- Manual code changes: none.
- Defects found after completion: none recorded for this entry.
- Architectural changes after implementation began: none; implementation had not begun.

### Entry P-004: Concurrent Booking Design

- Date and time: `unknown`.
- Prompt or request: Design concurrent booking creation before implementation.
- Outcome: Short transactions, slot row locking, a PostgreSQL partial unique index, stable conflict responses, idempotent retry behavior, and deterministic concurrency tests were approved.
- Failed attempts: none.
- Human intervention: the concurrency strategy was approved as the critical-feature design.
- Manual code changes: none.
- Defects found after completion: none recorded for this entry.
- Architectural changes after implementation began: none; implementation had not begun.

### Entry P-005: Initial Roadmap

- Date and time: `unknown`.
- Prompt or request: Divide implementation into independently verifiable milestones and small reviewable tasks.
- Outcome: A milestone roadmap from repository foundation through independent release verification was produced and materialized as project documentation.
- Failed attempts: none.
- Human intervention: the planning phase and selected roadmap were approved.
- Manual code changes: none.
- Defects found after completion: later review found ordering, dependency, CI timing, command-topology, and task-size defects listed in P-006.
- Architectural changes after implementation began: none; implementation had not begun.

### Entry P-006: Plan-Agent Review

- Date and time: `unknown`.
- Prompt or request: Review all planning documents before implementation for dependency inversions, missing traceability, late CI, unresolved blockers, command validity, repository-rule contradictions, and oversized tasks.
- Outcome: The review identified M0 task-order and metadata defects, missing pre-code traceability, CI introduced after foundational milestones, missing browser-test infrastructure, an undefined PostgreSQL host-test topology, late error and redaction prerequisites, an unresolved local-secret strategy, and oversized tasks.
- Failed attempts: none.
- Human intervention: the human approved the review corrections and supplied explicit decisions for local development defaults and PostgreSQL test topology.
- Manual code changes: none.
- Defects found after completion: the defects listed in the outcome were found after the initial roadmap documentation was completed.
- Architectural changes after implementation began: none; implementation had not begun.

### Entry P-007: Approved Pre-Implementation Corrections

- Date and time: `unknown`.
- Prompt or request: Correct planning documents only; do not scaffold, install dependencies, create migrations, or begin implementation.
- Outcome: Planning documents were corrected for M0 ordering, staged commands, incremental CI, browser-test ownership, database-test topology, local-secret handling, prerequisite error and redaction work, persistence-safe readiness, task splits, and decision blockers. No implementation artifact was created.
- Failed attempts: two combined documentation patches did not apply because expected heading context did not match the current files; neither made file changes, and both were replaced with smaller targeted patches.
- Human intervention: the human rejected PostgreSQL trust authentication and per-restart Django secret generation, and approved clearly labelled development-only defaults with strict production rejection.
- Manual code changes: none.
- Defects found after completion: consistency review found and corrected management-secret logging ownership, public-exposure blocker wording, a missing Django system-check command, credential-exchange abuse-control ownership, an omitted availability loading-state test, and an unowned frontend test path.
- Architectural changes after implementation began: none; implementation had not begun.

## Approved Architectural Choices

- Integrated Django modular monolith.
- Framework-independent domain logic.
- ORM access isolated in persistence adapters and query objects.
- Server-rendered pages with small TypeScript and Vite enhancements.
- PostgreSQL as the source of truth for booking uniqueness.
- Slot row locking plus a named partial unique index for concurrent booking integrity.
- Host tests connect to loopback-published PostgreSQL; container commands connect to `postgres`.
- Incremental GitHub Actions introduction beginning in M0.
- pytest-Playwright owns browser-test integration and Chromium execution.
- Clearly labelled local development defaults, ignored `.env` overrides, and strict production rejection of development values.

## Failed Attempts

- Two pre-implementation documentation patches failed their context checks and made no changes; the corrections were reapplied as smaller targeted patches.
- No implementation attempt has failed because implementation has not begun. Roadmap defects are recorded as defects rather than represented as failed implementation attempts.

## Human Interventions

- Supplied the original project charter.
- Selected the integrated Django modular monolith.
- Approved the product, architecture, concurrency strategy, and roadmap planning phase.
- Requested an independent Plan-agent review before implementation.
- Approved the review corrections.
- Chose password-based local PostgreSQL development defaults rather than trust authentication.
- Required a stable Django development secret across container restarts rather than per-restart generation.

## Manual Code Changes

None.

## Defects Found After Agent Completion

- M0 tooling referred to tests and configuration introduced by a later task.
- One M0 task had duplicate completion evidence and another had none.
- Traceability had not been created before code work.
- CI was introduced after foundational milestones rather than incrementally.
- PostgreSQL host-test connectivity and prerequisites were unspecified.
- Browser tests were required before Playwright ownership and setup existed.
- Booking error mapping and sensitive-value redaction were introduced later than the features requiring them.
- Local Compose secrets conflicted with one-command startup until development placeholders and production rejection were decided.
- Several tasks were too broad for one reviewable change.
- Database readiness did not explicitly preserve the persistence boundary.

## Architectural Changes Made After Implementation Began

None. Implementation has not begun.

## Reusable Implementation Entry Template

### Entry `<task-id>`: `<short title>`

- Date and time: `<value or unknown>`.
- Prompt or request: `<summary>`.
- Objective: `<roadmap objective>`.
- Files changed: `<paths or none>`.
- Tests added or changed: `<paths or none>`.
- Commands run: `<commands, including N/A entries with reasons>`.
- Command results: `<pass, fail, or N/A>`.
- Failed attempts: `<details or none>`.
- Human intervention: `<details or none>`.
- Manual code changes: `<details or none>`.
- Defects found after completion: `<details or none>`.
- Architectural changes after implementation began: `<details or none>`.
- Remaining risks: `<details or none>`.
- Completion decision: `<accepted, rejected, or blocked>`.
