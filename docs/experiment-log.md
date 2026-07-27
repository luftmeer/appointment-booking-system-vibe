# Experiment Log

## Purpose

Record the planning and implementation process without inventing dates, outcomes, or interventions. Exact historical timestamps are marked `unknown` where they are not available.

## Current State

- Phase: M0 repository foundation implementation.
- Application code created: minimal Django configuration plus the M0-T3 common application and database-independent liveness endpoint.
- Dependencies installed: Django, Ruff, pytest, and pytest-django from `uv.lock`.
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

## Roadmap Task History

### Entry M0-T1: Initialize Implementation Traceability

- Date and time: `unknown`.
- Prompt or request:

```text
Implement only `M0-T1` from `docs/roadmap.md`.

Read:

* `AGENTS.md`;
* the complete M0 section of `docs/roadmap.md`;
* `docs/experiment-log.md`;
* the relevant experiment criteria in `docs/product-specification.md`.

Do not begin `M0-T2`.

This is a pre-code traceability gate.

Do not create:

* Python application files;
* `pyproject.toml`;
* Django configuration;
* Docker files;
* CI workflows;
* frontend files.

Perform only the documentation work required by `M0-T1`.

For repository verification commands that do not yet exist, record:

N/A — command is introduced by M0-T2 or a later task

Do not claim that unavailable commands passed.

Update the experiment log with:

* this task prompt;
* files changed;
* planning activity backfilled;
* human decisions;
* failures or `none`;
* manual code changes or `none`;
* architectural changes;
* unresolved risks.

At completion, report:

* files changed;
* documentation checks performed;
* available commands run;
* unavailable commands and reasons;
* acceptance criteria verified;
* deviations from the roadmap;
* unresolved risks;
* confirmation that no application code was created.
```

- Objective: verify and maintain the pre-code implementation experiment record before M0-T2.
- Files changed: `docs/experiment-log.md`.
- Tests added or changed: none; M0-T1 requires documentation review only.
- Planning activity backfilled: entries P-001 through P-007 were reviewed and confirmed to cover the project charter, product planning, architecture alternatives and selection, concurrent-booking design, initial roadmap, Plan-agent review, and approved pre-implementation corrections.
- Plan-agent findings: P-006 records the identified task-order, traceability, CI, browser-test, PostgreSQL-topology, prerequisite, local-configuration, and task-size defects; P-007 records their approved documentation corrections and follow-up consistency findings.
- Human decisions: the backfilled record identifies the selected Django modular monolith, approved concurrency strategy and roadmap corrections, password-based local PostgreSQL topology, and stable local Django secret approach. For this task, the human limited work to M0-T1 documentation and prohibited M0-T2 and all application, tooling, container, CI, and frontend artifacts.
- Commands run: no repository verification command was available after M0-T1. `uv sync`: `N/A — command is introduced by M0-T2 or a later task`; `uv run ruff check .`: `N/A — command is introduced by M0-T2 or a later task`; `uv run ruff format --check .`: `N/A — command is introduced by M0-T2 or a later task`; `uv run pytest`: `N/A — command is introduced by M0-T2 or a later task`; `uv run python manage.py check`: `N/A — command is introduced by M0-T2 or a later task`.
- Command results: all five M0 baseline commands were unavailable and were not run or reported as passing.
- Failed attempts: none.
- Human intervention: the human supplied the task scope, prohibited artifacts, required unavailable-command wording, and completion-report requirements; no additional intervention occurred.
- Manual code changes: none.
- Defects found after completion: none.
- Architectural changes after implementation began: none; application implementation has not begun and the approved architecture is unchanged.
- Remaining risks: exact historical planning timestamps remain `unknown`; historical completeness is limited to the planning evidence available in the repository; future tasks must continue adding an entry after every task. Product decisions still marked `TBD` remain unresolved, although none blocks M0 or M1.
- Completion decision: accepted as the M0-T1 pre-code traceability gate.

### Entry M0-T2: Add Locked Python Tooling And Minimal Django Configuration

- Date and time: `2026-07-26`; exact time unknown.
- Prompt or request: implement only M0-T2 after reading the repository rules, complete M0 roadmap section, experiment log, and relevant product experiment criteria; do not begin M0-T3.
- Objective: establish locked Python dependencies, quality tooling, and enough Django configuration for all baseline Python commands to run.
- Files changed: `pyproject.toml`, `uv.lock`, `.gitignore`, `.env.example`, `manage.py`, `config/__init__.py`, `config/settings.py`, `config/urls.py`, `tests/conftest.py`, `tests/smoke/test_configuration.py`, and `docs/experiment-log.md`.
- Tests added or changed: added `tests/smoke/test_configuration.py` to verify the configured Django settings and root URL configuration import successfully; configured pytest and pytest-django in `pyproject.toml`; added `tests/conftest.py` as the expected empty shared-fixture placeholder.
- Dependency rationale: Django 5.2 LTS is the approved web framework; pytest supplies the required Python test runner; pytest-django configures Django safely for pytest; Ruff supplies the required formatter and linter. `uv.lock` records the exact resolved packages and hashes for Python 3.12.
- Planning activity backfilled: none; M0-T1 completed the pre-code backfill.
- Plan-agent findings: none for this task.
- Human decisions: the human limited implementation to M0-T2 and explicitly prohibited beginning M0-T3.
- Commands run: `uv sync`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `uv run python manage.py check`. `docker compose up -d postgres`: `N/A — compose configuration is introduced by M1-T2`; `docker compose up --build`: `N/A — compose configuration is introduced by M1-T2`.
- Command results: `uv sync` passed using CPython 3.12.13 and installed 10 locked packages; Ruff lint passed; Ruff formatting check passed; pytest passed with 1 test; Django reported no system-check issues. Both Docker Compose commands were unavailable and were not run or reported as passing.
- Failed attempts: none.
- Human intervention: none beyond the task scope supplied in the prompt.
- Manual code changes: none.
- Defects found after completion: none.
- Architectural changes after implementation began: none; this task implements the approved Django modular-monolith foundation without adding domain or persistence modules.
- Remaining risks: production rejection of the documented local-development placeholder is deferred to M1-T2; the common application, liveness endpoint, and their tests remain intentionally deferred to M0-T3; baseline CI remains deferred to M0-T4.
- Completion decision: accepted after all five M0-T2 baseline commands passed.

### Entry M0-T3: Add The Common Application And Liveness Endpoint

- Date and time: `2026-07-27`; exact time unknown.
- Command invocation: `/implement-task M0-T3 M0-T4 Ignore commit issues for M0-T1 and M0-T2, since they are both in the same commmit. Also, I added OpenCode toolings. Accept those and continue with your implementation task.`
- Reusable protocol source: `.opencode/commands/implement-task.md` at commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- Objective: add the shared common application, route configuration, and database-independent liveness behavior.
- Files changed: `config/settings.py`, `config/urls.py`, `apps/__init__.py`, `apps/common/__init__.py`, `apps/common/apps.py`, `apps/common/urls.py`, `apps/common/views.py`, `tests/smoke/test_health.py`, and `docs/experiment-log.md`.
- Tests added, changed, or removed: added `tests/smoke/test_health.py` with one successful liveness response test and four unsupported-method cases; no tests were changed or removed.
- Planning activity backfilled: none.
- Plan-agent findings: none.
- Independent review findings: none; the reviewer identified HEAD, OPTIONS, and TRACE as optional additional regression coverage, not an acceptance-criteria gap.
- Assumptions made: the minimal documented liveness representation is JSON `{"status": "ok"}` with `application/json`, and GET is the sole supported method. The endpoint runs in an unmarked pytest-django test, so attempted database access would be rejected by the test harness.
- Human decisions: the human accepted the existing combined M0-T1/M0-T2 commit and OpenCode tooling, limited implementation to M0-T3, and explicitly prohibited M0-T4 and every other roadmap task.
- Commands run: `git status --short --branch`; `git log --oneline --decorate -10`; `git ls-files`; `git log -1 --format='%H' -- .opencode/commands/implement-task.md && git show --stat --oneline HEAD`; `uv run pytest tests/smoke/test_health.py`; `uv sync`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `uv run python manage.py check`; `git diff --check`; final `git status --short` and scoped `git diff` review. `docker compose up -d postgres`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the Compose configuration and PostgreSQL service`; `docker compose up --build`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the Compose configuration`.
- Command results: repository inspection found a clean `master` worktree at `4168734` before M0-T3 and confirmed the reusable protocol's full commit; the focused health suite passed with 5 tests; `uv sync` resolved 13 packages and checked 10 installed packages; Ruff lint passed; Ruff formatting reported 27 files already formatted; the complete pytest suite passed with 6 tests; Django reported no system-check issues; the diff whitespace check passed; final status and diff inspection found only M0-T3 files. Both Compose commands were unavailable and were not run or reported as passing.
- Failures encountered: none.
- Retries and recovery attempts: none.
- Human intervention: none beyond the task scope and accepted repository-state decisions in the invocation.
- Manual code changes: none.
- Defects discovered: M0-T3 requires response body and content-type tests and refers to a documented response, but the planning documents do not state the exact body or media type.
- Architectural changes after implementation began: none; the endpoint remains in the approved common HTTP module and has no domain, persistence, or database dependency.
- Deviations from the roadmap: none.
- Remaining risks: consumers could require a different liveness representation if a separate external contract exists; HEAD, OPTIONS, and TRACE rejection is not covered explicitly; later readiness work must preserve the liveness endpoint's database independence. Baseline CI remains intentionally deferred to M0-T4.
- Completion decision: accepted after the focused health tests and all five required M0 baseline commands passed.

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
- M0-T2 implementation completed without a failed attempt. Roadmap defects remain recorded as defects rather than represented as failed implementation attempts.

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

None. M0-T2 began implementation without changing the approved architecture.

## Reusable Implementation Entry Template

### Entry `<task-id>`: `<short title>`

- Date and time: `<value or unknown>`.
- Prompt or request: `<summary>`.
- Objective: `<roadmap objective>`.
- Files changed: `<paths or none>`.
- Tests added or changed: `<paths or none>`.
- Planning activity backfilled: `<entry references, details, none, or unknown>`.
- Plan-agent findings: `<details, none, or unknown>`.
- Human decisions: `<details or none>`.
- Commands run: `<commands, including N/A entries with reasons>`.
- Command results: `<pass, fail, or N/A>`.
- Failed attempts: `<details or none>`.
- Human intervention: `<details or none>`.
- Manual code changes: `<details or none>`.
- Defects found after completion: `<details or none>`.
- Architectural changes after implementation began: `<details or none>`.
- Remaining risks: `<details or none>`.
- Completion decision: `<accepted, rejected, or blocked>`.
