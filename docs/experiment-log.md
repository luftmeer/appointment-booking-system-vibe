# Experiment Log

## Purpose

Record the planning and implementation process without inventing dates, outcomes, or interventions. Exact historical timestamps are marked `unknown` where they are not available.

## Current State

- Phase: M1 Docker and PostgreSQL development environment implementation.
- Application code created: minimal Django configuration plus the M0-T3 common application and database-independent liveness endpoint.
- Dependencies installed: Django, Psycopg with its binary package, Ruff, pytest, and pytest-django from `uv.lock`.
- CI created: M0-T4 baseline GitHub Actions workflow for locked Python installation, Django checks, Ruff, and pytest; an uncommitted M1-T2 correction adds the PostgreSQL prerequisite for the now database-backed complete suite.
- Container image created: M1-T1 reproducible non-root Django web image.
- Development stack created: M1-T2 password-authenticated PostgreSQL and migration-gated Django Compose services.
- Database migrations created: none.
- Manual code changes: the human added the OpenCode tooling recorded in commit `41687345b049e95beeed401a1ed38e985afb7cee`; see the M0 traceability correction below.

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
- Human intervention: beyond the M0-T2 task scope, the human added the OpenCode tooling committed alongside M0-T2 in `41687345b049e95beeed401a1ed38e985afb7cee`. The tooling was not part of the M0-T2 roadmap implementation and was explicitly accepted by the human before M0-T3 continued.
- Manual code changes: the human added `.opencode/agents/adversarial-tester.md`, `.opencode/agents/refactor.md`, `.opencode/agents/refactoring-advisor.md`, `.opencode/agents/test-implementer.md`, and `.opencode/commands/implement-task.md` in commit `41687345b049e95beeed401a1ed38e985afb7cee`.
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
- Manual code changes: none during M0-T3; the human-confirmed OpenCode additions already existed in commit `41687345b049e95beeed401a1ed38e985afb7cee` and were accepted as repository state in the M0-T3 invocation.
- Defects discovered: M0-T3 requires response body and content-type tests and refers to a documented response, but the planning documents do not state the exact body or media type.
- Architectural changes after implementation began: none; the endpoint remains in the approved common HTTP module and has no domain, persistence, or database dependency.
- Deviations from the roadmap: none.
- Remaining risks: consumers could require a different liveness representation if a separate external contract exists; HEAD, OPTIONS, and TRACE rejection is not covered explicitly; later readiness work must preserve the liveness endpoint's database independence. Baseline CI remains intentionally deferred to M0-T4.
- Completion decision: accepted after the focused health tests and all five required M0 baseline commands passed.

### Entry M0-T4: Add Baseline Python CI

- Date and time: `2026-07-27`; exact time unknown.
- Command invocation: `/implement-task M0-T4 M1-T1`.
- Reusable protocol source: `.opencode/commands/implement-task.md` at commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- Objective: verify M0 and later tasks through a clean-checkout Python CI baseline.
- Files changed: `.github/workflows/ci.yml` and `docs/experiment-log.md`.
- Tests added, changed, or removed: none; the workflow executes the complete existing six-test M0 smoke suite.
- Dependency and action rationale: no project dependency was added. `actions/checkout` v7.0.1 materializes the source and is pinned to commit `3d3c42e5aac5ba805825da76410c181273ba90b1`; credential persistence is disabled. `astral-sh/setup-uv` v9.0.0 installs the approved package manager and is pinned to commit `c771a70e6277c0a99b617c7a806ffedaca235ff9`; uv itself is pinned to `0.11.32`, Python is constrained to the approved 3.12 minor version, and caching is disabled so the baseline does not rely on hidden cache state. Both action versions and commits were verified against their official GitHub release and tag metadata.
- Planning activity backfilled: none.
- Plan-agent findings: none.
- Independent review findings: the workflow implementation, pinning, failure gates, security permissions, scope, and local command evidence passed review; the reviewer classified the missing GitHub-hosted clean-checkout run as a blocking completion-evidence gap.
- Assumptions made: the hosted `ubuntu-24.04` runner supports the pinned Node 24 actions. The initial assumption that a fresh-container `act` run could satisfy the clean-checkout evidence was rejected by independent review because `act` copied the uncommitted worktree and skipped `actions/checkout`.
- Human decisions: the human limited implementation to M0-T4, prohibited M1-T1 and every other roadmap task, and prohibited committing or pushing without a separate instruction.
- Commands run: `git status --short --branch`; `git log --oneline --decorate -10`; repository file searches; `command -v act`, `command -v gh`, `command -v docker`, `git remote -v`, `uv --version`, and protocol commit inspection; `act --version`; `docker info --format '{{.ServerVersion}}'`; strict `act` validation, workflow listing, and dry run; `act push -j python -W .github/workflows/ci.yml -P ubuntu-24.04=ghcr.io/catthehacker/ubuntu:act-latest --container-architecture linux/amd64`; `uv sync`; `uv run pytest tests/smoke`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `uv run python manage.py check`. `docker compose up -d postgres`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the Compose configuration and PostgreSQL service`; `docker compose up --build`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the Compose configuration`.
- Command results: the worktree was initially clean at M0-T3 commit `00ebb25`; `act` 0.2.89 and Docker 29.6.2 were available, while `gh` and a Git remote were absent; strict workflow validation passed and listed one Python job for push and pull-request events; the dry run resolved every step; the fresh Linux container installed uv 0.11.32 and 10 locked packages, passed Django checks, Ruff lint, Ruff formatting for 27 Python files, and all 6 tests, and reported `Job succeeded`; local `uv sync` resolved 13 packages and checked 10 installed packages; the focused smoke suite and complete suite each passed 6 tests; local Ruff lint passed, Ruff formatting reported 27 files already formatted, and Django reported no system-check issues. Both Compose commands were unavailable and were not run or reported as passing.
- Failures encountered: independent review found that the required green clean-checkout GitHub Actions evidence is unavailable while the workflow is uncommitted and the repository has no remote; the local `act` execution does not satisfy that completion gate.
- Retries and recovery attempts: strict workflow validation, dry-run validation, and a fresh-container `act` execution all passed but could not verify hosted checkout behavior. No further recovery is possible without authorization to commit and push to a GitHub remote.
- Human intervention: none beyond the task constraints in the invocation.
- Manual code changes: none during M0-T4.
- Defects discovered: no workflow implementation defect was found. Independent review identified the missing hosted clean-checkout run as a completion-evidence blocker. A prior review's OpenCode-tooling traceability discrepancy remains pre-existing and was not rewritten as part of this task.
- Architectural changes after implementation began: none; this task implements the already approved incremental GitHub Actions baseline.
- Deviations from the roadmap: a GitHub-hosted run was unavailable because the repository has no remote and the workflow cannot be committed or pushed under the task constraints; the same workflow job was instead executed successfully in a fresh Linux container with `act`.
- Remaining risks: GitHub-hosted runner behavior is not independently verified until the workflow is committed and pushed; local `act` optimizes the checkout step by copying the source, so the pinned checkout action was verified by immutable reference and inspection rather than executed; later M1 and M2 tasks must extend this workflow with PostgreSQL, migrations, frontend, and browser checks without weakening the baseline.
- Completion decision: blocked pending an authorized commit and a green GitHub-hosted push or pull-request run from that commit; workflow validation, fresh-container execution, and all five required local M0 commands passed.

#### M0-T4 Hosted Completion Addendum

- Date and time: hosted run started `2026-07-27T20:54:57Z` and completed successfully by `2026-07-27T20:55:15Z`.
- Human intervention: the human confirmed creating and pushing M0-T4 commit `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8` after the original blocked decision.
- Remote state: `origin` is `git@github.com:luftmeer/appointment-booking-system-vibe.git`; local `main`, `origin/main`, and `origin/HEAD` resolved to M0-T4 commit `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8` when the completion evidence was reviewed.
- Hosted CI evidence: push-triggered GitHub Actions run [`30304622905`](https://github.com/luftmeer/appointment-booking-system-vibe/actions/runs/30304622905), attempt 1, completed with conclusion `success` for exact commit `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8`.
- Hosted job evidence: Python job [`90105692448`](https://github.com/luftmeer/appointment-booking-system-vibe/actions/runs/30304622905/job/90105692448) completed with conclusion `success` on `ubuntu-24.04`; checkout, uv installation, locked dependency installation, Django checks, Ruff lint, Ruff formatting, and pytest all succeeded.
- Blocker resolution: the hosted run executed the pinned checkout action and every required M0 gate from the pushed commit, resolving the clean-checkout evidence blocker while preserving the original blocked decision above as historical state.
- Completion decision: M0-T4 accepted and M0 complete after the successful hosted clean-checkout run and the previously recorded local verification results.

### M0 Traceability Correction

- Date and time: `2026-07-27`; exact correction time unknown.
- Human confirmation: the human confirmed adding the OpenCode tooling included in commit `41687345b049e95beeed401a1ed38e985afb7cee` and creating and pushing M0-T4 commit `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8`.
- Historical correction: the five `.opencode/` files listed in the M0-T2 entry were human manual changes committed alongside, but not implemented as part of, M0-T2. Their omission from the manual-change record was identified by independent review and is corrected without rewriting Git history or attributing them to the M0-T2 implementation.
- M0-T4 correction: the original blocked decision remains above; the hosted completion addendum records the later commit, push, configured remote, successful run, and successful job that resolved it.
- Files changed by this correction: `docs/experiment-log.md` only.
- Tests added, changed, or removed: none; this is a traceability-only correction.
- Commands run: `git status --short --branch`; `git log --oneline --decorate -10`; `git remote -v`; commit file inspection for `41687345b049e95beeed401a1ed38e985afb7cee` and `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8`; GitHub Actions API inspection for run `30304622905` and job `90105692448`; `uv sync`; `uv run ruff check .`; `uv run ruff format --check .`; `uv run pytest`; `uv run python manage.py check`; `git diff --check` and scoped diff review.
- Command results: the initial worktree was clean with local `main`, `origin/main`, and `origin/HEAD` at `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8`; commit inspection confirmed the five OpenCode files and M0-T4 provenance; GitHub reported the run and job successful; `uv sync` resolved 13 packages and checked 10 installed packages; Ruff lint passed; Ruff formatting reported 27 files already formatted; all 6 tests passed; Django reported no system-check issues; the diff check passed and only `docs/experiment-log.md` changed.
- Failures encountered: the initial documentation commit attempt failed before creating a commit because configured GPG signing launched an interactive curses pinentry without an available TTY.
- Retries and recovery attempts: retry the commit with signing disabled for that command only; repository Git configuration remains unchanged and commit hooks remain enabled.
- Architectural changes: none.
- Roadmap deviations: none introduced by this correction.
- Remaining M0 blockers: none.

### Entry M1-T1: Build The Web Container

- Date and time: `2026-07-28`; exact time unknown.
- Command invocation: `/implement-task M1-T1 M1-T2`.
- Reusable protocol source: `.opencode/commands/implement-task.md` at commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- Objective: package the locked Django application in a reproducible container.
- Files changed: `Dockerfile`, `.dockerignore`, and `docs/experiment-log.md`.
- Tests added, changed, or removed: none; the required image-build and process-user behavior was exercised with Docker smoke commands, and the existing six-test suite was executed unchanged.
- Base-image and tool rationale: the final image uses official `python:3.12.13-slim-bookworm` pinned to multi-platform index digest `sha256:d50fb7611f86d04a3b0471b46d7557818d88983fc3136726336b2a4c657aa30b`. Python 3.12 matches ADR 001, the exact patch improves repeatability, slim Bookworm minimizes the runtime while retaining a stable Debian base, and the index supports native AMD64 and ARM64 builds. The disposable builder obtains uv 0.11.32 from the official `ghcr.io/astral-sh/uv` image pinned to multi-platform index digest `sha256:df4cae8f3a96d175e2e5f992e597550000edbe78fdc2594d5cd8de1a217f504c`, matching the CI tool version without adding a project dependency or retaining uv in the runtime image.
- Dependency behavior: `uv sync --locked --no-dev --no-install-project --no-cache` used the committed lock file, prohibited Python downloads, and installed only `asgiref==3.12.1`, `django==5.2.16`, and `sqlparse==0.5.5` into the builder virtual environment. The final stage copies only that virtual environment; uv, uvx, and the uv cache are absent from the runtime image.
- Assumptions made: Django's built-in development server is the minimal approved local default until M1-T2 introduces startup coordination; production serving is an explicit M1 non-goal. UID and GID 10001 are unprivileged and do not conflict with a requirement elsewhere in the repository.
- Human decisions: the human limited implementation to M1-T1 and explicitly prohibited M1-T2 and every other roadmap task.
- Independent review findings: the initial image satisfied the explicit build and non-root criteria but retained approximately 41 MiB of uv cache and 53 MiB of uv/uvx build tooling. The reviewer required a disposable builder stage so the runtime image would satisfy the cache-exclusion implementation note; the correction and focused verification removed the finding.
- Commands run: initial Git status and history inspection; repository file searches; planning and ADR review; `docker buildx imagetools inspect python:3.12.13-slim-bookworm`; `docker buildx imagetools inspect ghcr.io/astral-sh/uv:0.11.32`; two no-cache `docker build --pull --no-cache --tag appointment-booking-system:m1-t1 .` executions; `docker build --check .`; image metadata inspection; runtime absence checks for `/root/.cache/uv`, `/bin/uv`, and `/bin/uvx`; `docker run --rm --entrypoint /usr/bin/id appointment-booking-system:m1-t1 -u`; in-image `manage.py check`; two detached default-process smoke runs; `docker exec appointment-booking-m1-t1-smoke /usr/bin/id -u`; `docker top appointment-booking-m1-t1-smoke -eo user,pid,args`; `curl --fail --retry 10 --retry-connrefused --retry-delay 1 http://127.0.0.1:18000/health/live`; container log inspection and removal; two final repository command passes with `uv sync`, `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest`, and `uv run python manage.py check`. `docker compose build`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the Compose configuration`; `docker compose up -d postgres`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the PostgreSQL service`; `docker compose up --build`: `N/A — command is introduced by a later roadmap task: M1-T2 adds the Compose configuration and coordinated services`.
- Command results: the initial no-cache build produced Linux ARM64 image `sha256:65cf1e85521ccc47e357c6bb9e8bc132556c5fdb4a4f1cd60f52c9b530a54ce0`, size 259,589,502 bytes. After the builder-stage correction, the no-cache rebuild produced image `sha256:fc925636db293ce058f8727c12b602915ee2b3e0e80e7276c5417460d6492aed`, size 180,829,376 bytes; runtime absence checks confirmed that uv, uvx, and `/root/.cache/uv` were not present. Dockerfile static build checks completed with no warnings. Final image metadata declared user `10001:10001` and the expected Django command; standalone and running-container UID checks both returned `10001`; Docker process metadata showed both default runserver processes under user 10001; the in-image Django check passed; the default process served `/health/live` with `200` and `{"status": "ok"}`. The final `uv sync` resolved 13 packages and checked 10 installed packages; Ruff lint passed; Ruff formatting reported 27 files already formatted; all 6 tests passed; the host Django check reported no issues. Both smoke containers were removed. Compose commands were unavailable and were not run or reported as passing.
- Failures encountered: the first image metadata template referenced the absent optional `Config.Entrypoint` map key and failed with a template parsing error; the image and runtime were unaffected. Independent review then found build-only cache and tooling retained in the initial runtime image.
- Retries and recovery attempts: metadata inspection was rerun using fields guaranteed to exist and succeeded. The Dockerfile was changed to use a no-cache builder and fresh runtime stage; the image was rebuilt and every focused and repository check was rerun successfully.
- Human intervention: none beyond the task scope supplied in the invocation.
- Manual code changes: none.
- Defects discovered: the initial single-runtime-stage image retained uv cache and tooling; the final builder/runtime split removes both.
- Architectural changes after implementation began: none; this task implements the approved Docker packaging boundary without adding product, persistence, PostgreSQL, or Compose behavior.
- Deviations from the roadmap: none.
- Remaining risks: only the host-native ARM64 image was executed locally, although both base references are pinned multi-platform indexes; byte-for-byte equality across repeated builds was not measured; the default command is intentionally a development server; Compose startup, stable development configuration, PostgreSQL, migrations, and readiness remain deferred to M1-T2 and M1-T3.
- Completion decision: accepted after the clean image build, non-root metadata and runtime checks, in-container Django check, default-process HTTP smoke test, and all five required repository commands passed.

### Entry M1-T2: Add PostgreSQL Compose Services And Startup

- Date and time: `2026-07-28`; exact time unknown.
- Command invocation: `/implement-task M1-T2 M1-T3`.
- Reusable protocol source: `.opencode/commands/implement-task.md` at commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- Objective: coordinate PostgreSQL health, migration application, and Django startup.
- Files changed: `compose.yaml`, `docker/entrypoint.sh`, `Dockerfile`, `config/settings.py`, `.env.example`, `pyproject.toml`, `uv.lock`, `tests/smoke/test_settings.py`, `tests/integration/test_compose_configuration.py`, `tests/integration/test_database.py`, `tests/integration/test_entrypoint.py`, and `docs/experiment-log.md`.
- Tests added, changed, or removed: added 21 subprocess configuration tests in `tests/smoke/test_settings.py` for environment-selected host and port, valid production configuration, all required production omissions, known development values, whitespace-only credentials, debug mode, unknown environments, and distinct test-database configuration; added three Docker Compose rendering tests proving bind overrides cannot widen loopback and one `DATABASE_PORT` controls only host publication; added one real PostgreSQL query proving the exact dedicated test database differs from the developer database; added seven entrypoint subprocess tests proving nonnumeric, zero-attempt, negative, and out-of-range startup controls fail before a connection attempt; no tests were changed or removed.
- Dependency rationale: added `psycopg[binary]>=3.2,<3.3` because Django requires a PostgreSQL DB-API adapter. The binary extra provides supported local and container wheels without adding a compiler toolchain; `uv.lock` resolved `psycopg==3.2.13`, `psycopg-binary==3.2.13`, and transitive `typing-extensions==4.16.0`.
- PostgreSQL image rationale: Compose uses official PostgreSQL `16.13-bookworm`, matching ADR 001's PostgreSQL 16 decision, pinned to multi-platform index digest `sha256:472efd9a66f2b2f1a5aeb18b28de74332e6ef88c2b93a1a5d812fb6db67a5f60` for immutable ARM64 and AMD64 resolution.
- Configuration behavior: host settings default to `DATABASE_HOST=127.0.0.1` and the configurable `DATABASE_PORT`; the same port variable controls PostgreSQL host publication while Compose fixes the web container to `postgres:5432`. Both service bind addresses are hardcoded to `127.0.0.1` and ignore attempted bind-host environment overrides. `DJANGO_ENVIRONMENT=production` rejects each missing or blank required value, known development values, local-only allowed hosts, and debug mode. A finite positive `DATABASE_CONNECT_TIMEOUT` is applied to every PostgreSQL connection and an explicit `DATABASE_TEST_NAME` must differ from the developer database. `.env.example` labels every default as development-only and documents every supported Django, database, startup, and host-port variable.
- Startup behavior: Compose initializes PostgreSQL with SCRAM-SHA-256 local and host authentication, publishes PostgreSQL and web only on fixed loopback addresses, stores data in `appointment-booking-system_postgres_data`, and starts web only after PostgreSQL reports healthy. The non-root web entrypoint validates an attempt count from 1 through 1000 and an integer retry delay from 0 through 300 seconds before connecting, combines the default two-second per-attempt connection timeout with at most 10 attempts and one-second retry delays, applies migrations once connectivity succeeds, and executes the one-process Django development server; migration errors are not retried or hidden.
- Assumptions made: `DJANGO_ENVIRONMENT` intentionally supports only `development` and `production`; public deployment remains unresolved and outside M1. The default PostgreSQL and Django values are public project-specific development placeholders, not security boundaries. Django's development server remains appropriate only for this local stack.
- Human decisions: the human limited implementation to M1-T2 and explicitly prohibited M1-T3 and every other roadmap task.
- Independent review findings: the first review found bind-host overrides that could expose services, split PostgreSQL host-port settings, a retry count without per-attempt timeout, incomplete production missing/blank validation, and a prefix-based test-database assertion. Fixed loopback addresses and one port variable, finite Psycopg timeout/startup controls, stronger configuration validation, adversarial Compose rendering tests, and an exact `current_database()` assertion resolved those findings. The resumed review confirmed all five resolutions but found that malformed attempt or delay controls could bypass or obscure the startup bound. Pre-connection range validation and black-box subprocess/container tests resolved the additional finding. Final read-only review confirmed every finding resolved, found no blocking, required, or optional issue, and accepted M1-T2 without M1-T3 scope.
- Commands run: repository and planning inspection; PostgreSQL image digest inspection; `uv lock`; repeated `uv sync`, focused settings/Compose/database/entrypoint tests, and focused Ruff checks; `docker compose config` including adversarial bind and `DATABASE_PORT=55432` rendering; `uv lock --check`; `/bin/sh -n docker/entrypoint.sh`; `docker build --check .`; repeated `docker compose build`; black-box no-network entrypoint timeout and malformed-control probes; fresh-volume PostgreSQL initialization; default and non-default host-port database tests; `uv run python manage.py check --database default`; `uv run python manage.py migrate`; `uv run python manage.py migrate --check`; PostgreSQL port, volume, HBA, and authentication inspection; repeated one-command `docker compose up --build --wait`; container logs, process user, container-side settings and database checks; retry-all-errors liveness curls; secret and PostgreSQL cluster fingerprint capture; `docker compose restart postgres web`; final `uv sync`, Ruff, pytest, and Django checks with PostgreSQL running; final Compose cleanup and `.env` ignore inspection. `uv run pytest tests/integration/common`: `N/A — command and readiness tests are introduced by a later roadmap task: M1-T3`; `curl --fail http://localhost:8000/health/ready`: `N/A — endpoint is introduced by a later roadmap task: M1-T3`.
- Command results: final Compose rendering fixed both bind addresses to `127.0.0.1`, ignored adversarial bind variables, mapped `DATABASE_PORT=55432` only to PostgreSQL host publication, fixed the web container to `postgres:5432`, and preserved SCRAM initialization, health gating, and the named volume. Final web image `sha256:1b9a9fa1371ee9e26d41a527a75944c5650f2d5d3ea9bc272eaca639016d26d0` built successfully; nonnumeric, zero-attempt, negative, out-of-range, and oversized startup controls exited immediately with explicit configuration errors; the no-network startup probe exited nonzero in 1.35 seconds under test-only one-second timeout, two-attempt, zero-delay bounds. A fresh PostgreSQL volume initialized successfully; the exact `appointment_booking_test` database test passed at both default port 5432 and overridden host port 55432. Both services reached healthy state and web ran as UID 10001. Host and container settings selected `127.0.0.1` and `postgres`; authenticated connections succeeded from both; wrong-password authentication was rejected. PostgreSQL reported zero trust rules and Docker reported only `127.0.0.1:5432` publication. Host and entrypoint migrations completed with no migrations to apply, and `migrate --check` passed. Secret, PostgreSQL system, and volume fingerprints remained identical across final simultaneous restart; each web start migrated before serving. `/health/live` repeatedly returned `200` and `{"status": "ok"}`. The corrected focused settings/Compose suite passed 24 tests, the entrypoint suite passed seven tests, focused PostgreSQL tests passed at both ports, and the complete suite passed all 38 tests. Final `uv sync` resolved 16 packages and checked 13 installed packages; Ruff lint passed; Ruff formatting reported 31 files already formatted; Django reported no issues.
- Failures encountered: focused Ruff initially found one 91-character settings line; the first wrong-password probe omitted `DJANGO_SETTINGS_MODULE` and failed before connecting; the first web startup exhausted retries because the direct probe also lacked `DJANGO_SETTINGS_MODULE`; one empty patch invocation was aborted without changes; independent review found the five security, topology, timeout, validation, and isolation gaps; the first correction contained one mismatched delimiter and one format violation, causing focused lint and pytest initialization to fail; resumed review found that malformed startup attempt or delay values could defeat the claimed startup bound.
- Retries and recovery attempts: the original settings line, password probe, and image environment were corrected and their checks passed. After the first review, loopback/port, timeout, production, and test-isolation behavior was corrected; the delimiter and formatting errors were fixed; all focused tests, fresh-volume/non-default-port infrastructure checks, restart checks, and the full repository suite were rerun successfully. After resumed review, both startup controls gained pre-connection validation with shell-safe upper bounds; host subprocess and image-level no-network probes covered invalid, zero, negative, out-of-range, oversized, and valid zero-delay behavior; the image, healthy stack, and complete repository gates were rerun successfully.
- Human intervention: none beyond the task scope supplied in the invocation.
- Manual code changes: none.
- Defects discovered: the initial entrypoint probe lacked Django settings; bind-address and split-port overrides weakened topology guarantees; connection retries lacked a per-attempt timeout; production validation allowed missing host/port and blank credentials; test isolation relied on a database-name prefix; and malformed or shell-overflowing startup-control values could defeat the retry bound. All were corrected within M1-T2.
- Architectural changes after implementation began: none; this task implements approved ADR 003 and ADR 004 topology and configuration decisions without adding domain, readiness endpoint, or CI behavior.
- Deviations from the roadmap: none.
- Remaining risks: changing PostgreSQL identity or password values after the named volume has initialized requires an explicit local volume reset or database role update; the named volume intentionally survives `docker compose down`; default worst-case startup wait is approximately 29 seconds plus process overhead; the current GitHub Actions job does not provide PostgreSQL until M1-T4; the liveness endpoint intentionally remains database-independent and `/health/ready` remains deferred to M1-T3; the web command is a development server.
- Completion decision: accepted after Compose startup, loopback binding, host and container PostgreSQL connections, SCRAM/no-trust inspection, production validation tests, migration and restart smoke tests, liveness verification, and every applicable repository command passed.

#### M1-T2 Post-Commit Review Correction Addendum

- Date and time: `2026-07-28`; exact time unknown.
- Trigger: after commit `de5bf52`, the human requested another independent review against `AGENTS.md` and M1-T2, then requested implementation of the resulting recommendations without a commit and with human verification before any commit.
- Review findings: production validation compared the raw rather than normalized database name; local-only allowed-host validation omitted IPv6 loopback; Compose loaded ignored `.env` overrides that plain host commands did not consume; blank startup controls selected defaults instead of reaching validation; and durable tests did not independently protect startup, migration ordering and failure propagation, complete Compose publication, health gating, authentication, fresh initialization, and persistence behavior. Optional findings identified a fixed Compose project name and stale current dependency inventory.
- Files changed: `.env.example`, `Dockerfile`, `compose.yaml`, `config/settings.py`, `docker/entrypoint.sh`, `docs/decisions/003-postgresql-test-topology.md`, `docs/testing-strategy.md`, `tests/smoke/test_settings.py`, `tests/integration/test_compose_configuration.py`, `tests/integration/test_compose_runtime.py`, `tests/integration/test_entrypoint.py`, and `docs/experiment-log.md`.
- Tests added or changed: settings coverage increased from 21 to 28 tests for uv env-file loading, normalized development database rejection, canonical IPv6 and hostname loopback-only values, and mixed external hosts; entrypoint coverage increased from seven to 19 tests for unset defaults, blank, whitespace, leading-zero, lower/upper bounds, exact attempts and sleeps, eventual success, migration ordering, and migration failure propagation; Compose rendering coverage increased from three to seven tests for automatic `.env` discovery, all publications, the full PostgreSQL health command, SCRAM initialization, immutable image, named volume, health dependency, clean-checkout default equality, and blank controls; two isolated runtime tests now exercise a fresh default stack and an unhealthy PostgreSQL dependency. The complete inventory is 63 tests.
- Implementation corrections: production compares the normalized effective database name and classifies canonical IPv4, IPv6, bracketed IPv6, `localhost`, and `*.localhost` loopback values with the standard library. Compose and the entrypoint default startup controls only when unset, so blanks reach canonical range validation. The existing virtualenv is added to image `PATH`, allowing the entrypoint to use `python` consistently and enabling controlled shell tests. The fixed Compose project name was removed so separate checkout names can remain isolated. No application dependency was added: Compose continues loading `.env`, while documented host commands use uv's built-in `--env-file` support.
- Runtime test isolation: each runtime test sanitizes ambient Compose and application selectors, supplies absolute Compose files, uses a unique project, random loopback ports, and a temporary env file, and removes only project-labelled containers, volumes, networks, and local images. The clean stack starts first with tracked database, user, password, and Django-secret defaults. The same env file drives a real host Django query. A temporary bind-mounted test settings module then enables Django's built-in contenttypes migrations, proving real migration application without adding production schema. Runtime checks cover host and container database access, exact loopback publications, PostgreSQL health gating, zero trust rules, SCRAM defaults and stored verifier, explicit wrong-password rejection, UID 10001, unapplied migrations, sentinel data persistence, stable cluster/volume/secret identity, liveness, and cleanup.
- Dependency changes: none; uv's existing env-file support and Python's standard-library `ipaddress` module avoid new packages.
- Commands run: repository status, history, roadmap, ADR, testing-strategy, settings, Compose, Dockerfile, test, and experiment-log inspection; `uv run --help`; uv settings documentation inspection; repeated focused pytest and Ruff checks; `/bin/sh -n docker/entrypoint.sh`; `docker compose config --quiet`; `docker build --check .`; `uv lock --check`; repeated isolated runtime pytest runs; `uv sync`; `docker compose up -d postgres`; `docker compose up -d --wait postgres`; complete Ruff, pytest, and Django gates; adversarial test reviews before and after runtime hardening.
- Command results: final focused settings, entrypoint, and Compose rendering tests passed all 54 tests. The final isolated runtime suite passed both tests in 183.02 seconds, including automatic defaults, migrations, unhealthy dependency gating, ambient-environment isolation, all-resource cleanup, and scoped fallback assertions. The final complete repository run passed all 63 tests in 219.45 seconds; lint passed; formatting reported 32 files already formatted; `uv sync`, Django and migration checks, shell syntax, Compose rendering, Dockerfile static checks, lock checks, and `git diff --check` passed. Standard `docker compose up --build --wait` built web image `sha256:bc840d60ccfc00f97369aa68e12e6df1473bbc345aab8c6a3387556c32a1bb6a`; both services became healthy on loopback, web ran as UID/GID 10001, container settings used host `postgres`, entrypoint logs showed migration before server startup, and `/health/live` returned `200` with `{"status": "ok"}`.
- Failures encountered: initial focused Ruff found two overlong test lines. The first hardened runtime query used nonexistent `pg_authid.passwd` instead of `rolpassword`. The next run proved that a project with no migrations does not create `django_migrations`, confirming the review's vacuous-migration concern; the test was changed to apply built-in contenttypes migrations through an isolated temporary settings override. Psycopg's connection-level wrong-password `OperationalError` exposed the explicit PostgreSQL authentication diagnostic but no SQLSTATE, so the assertion uses that exact diagnostic alongside successful connectivity, zero trust rules, and the SCRAM verifier. A later complete formatting check found one final line for Ruff to format. One runtime rerun exceeded its outer timeout while Docker Desktop delayed a web health-check exec despite the live server responding directly; the generated full-UUID project was explicitly removed, Compose wait and cleanup commands gained deadlines, and the positive lifecycle test now polls the actual loopback liveness endpoint after detached health-gated startup while the separate unhealthy-dependency test retains Compose health-state assertions. Every other failed test cleaned its unique Compose project automatically.
- Independent test review: the first adversarial pass found runtime-harness isolation and acceptance-evidence gaps. After hardening, the resumed pass found no remaining R1-R5 production or M1-T2 behavioral blocker. A fresh final reviewer then required sanitizing the remaining settings, entrypoint, and direct Psycopg test environments and verifying cleanup during failed test bodies across project-labelled containers, volumes, networks, and local images. Those requirements and its optional automatic `.env`, full-UUID project name, unset-default, and evidence-wording findings were corrected before the final 63-test pass. Final resumed review confirmed RQ-1, RQ-2, and original R1-R5 resolved, found no blocking or required issue, and declared the uncommitted correction ready for human verification without authorizing a commit.
- Scope: no readiness endpoint, persistence health interface, CI PostgreSQL service, domain behavior, or other M1-T3/M1-T4 work was added.
- Remaining risks: runtime Compose tests require Docker and a sufficiently recent Compose plugin; dynamic host-port reservation has a small bind race; the maximum startup controls permit a long but finite wait; the local web process remains Django's development server; database readiness and PostgreSQL CI remain deferred to M1-T3 and M1-T4.
- Completion decision: implementation corrections and behavioral evidence are complete, but no correction commit will be created until the human verifies the uncommitted diff and explicitly authorizes the next action.

#### M1-T2 CI Completion Correction Addendum

- Date and time: `2026-07-29`; exact time unknown.
- Trigger: after the post-commit correction was published, an independent review reconciled the repository with the earlier uncommitted evidence and found the exact pushed commit's hosted workflow red because the complete suite had become PostgreSQL-backed before CI supplied PostgreSQL.
- Human authorization and provenance: the human explicitly confirmed authorizing commit `fba930028d9cf1f57b3f733d160dcea0b5be0a01` and its push to `main`. The human then authorized a roadmap correction adding the PostgreSQL service and CI environment required to run the complete M1-T2 suite without weakening or skipping database/runtime tests, explicitly excluding M1-T3 readiness work. No follow-up commit or push is authorized yet.
- Hosted failure evidence: push run [`30372466131`](https://github.com/luftmeer/appointment-booking-system-vibe/actions/runs/30372466131), Python job `90319594663`, ran exact commit `fba930028d9cf1f57b3f733d160dcea0b5be0a01` and failed in `Test Python` with exit code 1 after 1 minute 33 seconds. Public unauthenticated access exposed the failed step but not detailed logs; the workflow itself had no PostgreSQL service or database environment despite collecting the PostgreSQL-backed suite.
- Review findings addressed: the runtime host query still inherited uv env-file selectors, and fallback cleanup/original-exception behavior was implemented but not directly exercised. The runtime environment now removes `UV_ENV_FILE` and `UV_NO_ENV_FILE`; pure harness tests inject hostile ambient controls, nonzero Compose cleanup, all four project resource classes, scoped fallback success, post-cleanup rechecks, Compose timeout, and original body-exception preservation.
- Files changed: `.github/workflows/ci.yml`, `tests/integration/test_compose_runtime.py`, and `docs/experiment-log.md`.
- Tests added or changed: added three non-Docker harness tests for ambient-control removal, resource-scoped fallback cleanup, and timeout diagnostics preserving the original body failure. The complete inventory increases from 63 to 66 tests; no existing test is skipped, filtered, or weakened.
- Workflow correction: the existing Python job now supplies the immutable PostgreSQL 16.13 Bookworm image already approved for Compose, CI-only public database placeholders, SCRAM host/local initialization, loopback host settings, a dedicated Django test database, and Docker health gating. The complete `uv run pytest` command remains unchanged. The timeout increases from 10 to 20 minutes because the suite now includes two real Docker Compose lifecycle tests.
- Scope: this correction supplies only the prerequisite needed by the existing M1-T2 database/runtime tests. It does not add `/health/ready`, a persistence health interface, readiness tests, domain behavior, or other M1-T3 implementation.
- Commands run: repository status/history/commit inspection; workflow, runtime test, database test, and experiment-log inspection; public GitHub run inspection; attempted `gh run view 30372466131 --log-failed`; focused cleanup/environment pytest; focused and complete Ruff checks and formatting; `act --strict --validate`; `act --strict --list`; `act push --strict --dryrun` for the Python job; isolated CI-project resource preflight; fresh CI-equivalent `docker compose up -d --wait postgres`; `uv sync`; complete pytest and Django/migration checks under the exact CI job environment; shell syntax, Compose rendering, Dockerfile, lock, and diff checks; CI PostgreSQL status, loopback, database, SCRAM, and HBA inspection; isolated CI-project cleanup.
- Command results: worktree began clean with local and remote `main` at authorized commit `fba9300`; three focused harness tests passed; strict workflow validation passed; listing reported one Python job for push and pull-request events. A fresh isolated PostgreSQL volume initialized with the CI identity and became healthy on `127.0.0.1:5432`; the unchanged complete suite passed all 66 tests in 57.45 seconds under the exact CI environment. `uv sync`, Ruff lint, formatting for 32 files, Django and migration checks, shell syntax, Compose rendering, Dockerfile static checks, lock checks, and `git diff --check` passed. PostgreSQL reported database `appointment_booking_ci`, `scram-sha-256` password encryption, and zero trust HBA rules. The isolated containers, network, and volume were removed.
- Failures encountered: `gh` was unavailable, and public unauthenticated GitHub access did not expose detailed failed-job logs. `act` dry-run rendered the pinned PostgreSQL service and job container but `act 0.2.89` panicked in `containerReference.GetHealth` while querying a nonexistent dry-run service container, so it did not complete workflow dry-run validation. The first read-only CI database metadata probe omitted `DJANGO_SETTINGS_MODULE` and failed before connecting; the corrected probe used `config.settings` and returned the expected database, SCRAM setting, and zero trust count.
- Remaining verification: obtain independent review and request human verification of the uncommitted diff. Hosted clean-checkout success remains unavailable until the human later authorizes a follow-up commit and push.
- Completion decision: blocked pending human verification of the uncommitted diff, an explicitly authorized commit/push, and a green hosted run for that exact commit.

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
- Manually added the five OpenCode tooling files included in commit `41687345b049e95beeed401a1ed38e985afb7cee` and later explicitly accepted them as repository state.
- Created and pushed M0-T4 commit `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8`, enabling successful hosted CI run `30304622905`.
- Confirmed authorizing M1-T2 correction commit `fba930028d9cf1f57b3f733d160dcea0b5be0a01` and its push to `main`, then authorized the narrowly scoped PostgreSQL CI prerequisite correction while keeping M1-T3 readiness out of scope.

## Manual Code Changes

- `.opencode/agents/adversarial-tester.md`, added by the human in commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- `.opencode/agents/refactor.md`, added by the human in commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- `.opencode/agents/refactoring-advisor.md`, added by the human in commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- `.opencode/agents/test-implementer.md`, added by the human in commit `41687345b049e95beeed401a1ed38e985afb7cee`.
- `.opencode/commands/implement-task.md`, added by the human in commit `41687345b049e95beeed401a1ed38e985afb7cee`.

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
- M0 task entries initially omitted the human provenance of the OpenCode tooling committed in `41687345b049e95beeed401a1ed38e985afb7cee`; the M0 traceability correction records it.
- M0-T4 initially lacked a hosted clean-checkout run and remained blocked until the human pushed commit `3bfde5f7c0ea4ff263769330cadb5239e5b2cae8` and GitHub Actions run `30304622905` passed.
- M1-T2 correction commit `fba930028d9cf1f57b3f733d160dcea0b5be0a01` initially failed hosted run `30372466131` because the complete suite required PostgreSQL before the workflow supplied its approved PostgreSQL prerequisite.

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
