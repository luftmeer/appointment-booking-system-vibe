# ADR 004: Local Development Configuration And Secrets

## Status

Accepted.

## Context

The application must start locally with Docker Compose from a clean checkout, while no production, personal, or reusable credentials may be committed. PostgreSQL requires password authentication, Django sessions require a stable secret key, and local overrides must remain easy to configure.

## Considered Alternatives

### Commit Real Or Reusable Credentials

Rejected because repository contents are not an appropriate secret store and values could be reused outside local development.

### PostgreSQL Trust Authentication

Rejected because it removes password authentication and makes accidental network exposure more dangerous.

### Generate A New Django Secret On Every Restart

Rejected because it invalidates signed data and sessions on every restart and creates inconsistent behavior across processes.

### Require An Untracked `.env` Before First Startup

Secure for secrets but conflicts with the approved clean-checkout, one-command local startup requirement.

### Commit Clearly Labelled Development-Only Placeholders

Use known, non-reusable development defaults for Compose, allow ignored `.env` overrides, and make production configuration reject all known development values.

## Decision

- Compose configuration uses clearly named development-only placeholder values for the local PostgreSQL user, password, database, and Django secret.
- Development placeholders are intentionally public, limited to this local project, and provide no production security guarantee.
- `.env` is ignored and may override local ports or placeholders.
- `.env.example` documents every supported setting and labels development defaults as unsuitable for production.
- Production configuration requires externally supplied secrets and refuses to start when any known development placeholder is present or a required value is missing.
- PostgreSQL uses password authentication; trust authentication is prohibited.
- The local Django development secret is stable across restarts. It is not generated afresh by each container start.
- A real credential means any production value, personal value, secret delivered out of band, or value intended for reuse across projects or environments. Such values must never be committed.
- A development placeholder is an intentionally public value whose only permitted use is the isolated local environment and whose exact known value is rejected by production configuration.

## Rationale

- The decision satisfies one-command local startup without representing committed placeholders as secrets.
- Stable local signing behavior avoids unnecessary session invalidation.
- Password-based PostgreSQL behavior remains closer to deployed environments than trust authentication.
- Explicit production rejection prevents accidental promotion of development values.
- Ignored local overrides support port conflicts and developer-specific configuration without changing tracked files.

## Consequences

- Local development values must be visibly named and documented as insecure.
- Production settings need startup validation for required secrets and known placeholders.
- Compose must avoid publishing PostgreSQL beyond loopback.
- Reviewers must distinguish intentional placeholders from actual credentials during secret scanning.
- Local data is not protected from other processes or users with access to the developer machine and repository.

## Known Risks

- A development placeholder could be copied into a deployed environment; production rejection and documentation mitigate this.
- Developers may put real values into `.env`; ignore rules and log redaction remain necessary.
- A stable local Django secret allows local sessions to survive restarts, so developers must clear local state when testing secret rotation.
