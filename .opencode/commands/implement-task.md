---
description: Implement Milestone
agent: build
---

Implement only `$1` from `docs/roadmap.md`.im

Do not begin `$2` or any other roadmap task. If `$2` is `NONE`, do not begin any subsequent task.

## Preparation

Before editing:

1. Read `AGENTS.md`.
2. Read the complete milestone containing `$1` in `docs/roadmap.md`.
3. Read all planning documents and ADRs referenced by that task.
4. Inspect the current repository state and relevant existing implementation.
5. Confirm that the task's dependencies are complete.
6. Check whether an unresolved decision blocks the task.
7. Briefly state:

   * the intended changes;
   * the files or modules likely to be affected;
   * the tests required;
   * the verification commands you expect to run.

If a dependency, contradiction, or unresolved decision prevents correct implementation, stop before editing and report the blocker. Do not silently invent product behavior.

## Scope

Perform only the work required by `$1`.

* Do not implement work assigned to `$2` or another roadmap task.
* Do not make unrelated refactors or formatting changes.
* Do not expand the product scope.
* Do not alter requirements or weaken acceptance criteria to fit the implementation.
* Do not modify the roadmap merely to make the task appear complete.
* Do not introduce a dependency without explaining why it is necessary.
* Do not create a database schema change without its required migration.
* Do not bypass the architectural boundaries defined in `AGENTS.md`.
* Do not commit, push, merge, or begin the next task unless explicitly instructed.

When a small prerequisite is unexpectedly necessary, first determine whether it belongs to `$1`. If it belongs to another roadmap task, stop and report the dependency rather than implementing it implicitly.

## Implementation

Implement the smallest coherent change that satisfies `$1`.

For every behavioral change:

* add or update tests;
* test externally observable behavior where practical;
* preserve existing valid behavior;
* include relevant failure and boundary cases;
* avoid tests that merely duplicate the implementation;
* do not weaken or delete tests simply to obtain a passing result.

Keep domain, persistence, HTTP, and presentation responsibilities within their documented boundaries.

## Verification

Run:

1. every verification command specified by `$1`;
2. every repository-wide command required by `AGENTS.md` that is available after completing `$1`;
3. focused tests before the complete applicable test suite.

For a command that genuinely does not yet exist, record:

```text
N/A — command is introduced by a later roadmap task: <task identifier or reason>
```

Use `N/A` only when the command or required infrastructure is genuinely unavailable at this roadmap stage.

Do not claim that:

* an unavailable command passed;
* an unexecuted command passed;
* a task is complete while a required verification command is failing;
* passing tests prove acceptance criteria that were not actually exercised.

If verification fails, investigate and correct the failure only within the scope of `$1`. If the correct fix requires another task or an unresolved decision, stop and report it instead of broadening the implementation.

## Experiment record

Update `docs/experiment-log.md` with:

* task identifier `$1`;
* command invocation: `/implement-task $1 $2`;
* reusable protocol source: `.opencode/commands/implement-task.md`;
* protocol commit or version when available;
* files changed;
* tests added, changed, or removed;
* commands run and their results;
* assumptions made;
* human decisions or interventions;
* failures encountered, or `none`;
* retries and recovery attempts, or `none`;
* manual code changes, or `none`;
* defects discovered;
* architectural changes, or `none`;
* deviations from the roadmap, or `none`;
* unresolved risks.

Do not duplicate the full reusable command text in every experiment entry. Record the invocation and the version-controlled command source instead.

Do not invent historical events, timestamps, failures, interventions, or decisions. Use `unknown` only where information is genuinely unavailable and `none` where the category is known to be empty.

## Completion report

At completion, report:

1. task implemented;
2. files created, modified, and deleted;
3. tests added, modified, and executed;
4. documentation checks performed;
5. commands run and exact results;
6. unavailable commands and specific reasons;
7. acceptance criteria verified, criterion by criterion;
8. assumptions made;
9. deviations from the roadmap;
10. unresolved risks or blockers;
11. experiment-log entry added;
12. confirmation that `$2` and all other roadmap tasks were not started.

Do not declare `$1` complete unless every applicable acceptance criterion and verification requirement has passed.
