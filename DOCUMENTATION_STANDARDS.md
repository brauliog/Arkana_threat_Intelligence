# Arkana Coding and Documentation Standards

**Status:** Draft  
**Owner:** Product Tech Lead  
**Applies to:** Arkana's internal Python API, supporting infrastructure, and
engineering documentation

This standard is designed to help an engineer with mid-level Python experience
and limited security-domain knowledge make a useful bug fix or feature
contribution within two to four weeks. It is intentionally specific to Arkana,
but its structure can later be adapted into an organization-wide standard.

The terms **must**, **should**, and **may** indicate required, recommended, and
optional practices. Exceptions must be explained in the pull request.

## 1. Principles

1. **Optimize for the next engineer.** A reader should be able to discover what
   the system does, run it, trace one request, test a change, and find an owner
   without private context.
2. **Keep one source of truth.** Link to canonical information instead of
   copying it into multiple documents.
3. **Document contracts and reasons.** Types, tests, schemas, and code describe
   behavior. Prose explains intent, constraints, trade-offs, and operations.
4. **Change documentation with the code.** Documentation is part of the
   definition of done, not follow-up work.
5. **Prefer executable truth.** Commands and examples should run in CI when
   practical. Generated API reference must come from the running application or
   source code.
6. **Write for scanning.** Put the result first, use descriptive headings, and
   keep procedures ordered and testable.

## 2. Documentation map and ownership

The README is the front door, not the entire knowledge base. It must remain
short enough for a new engineer to identify and complete the golden path in one
sitting.

| Artifact | Canonical location | Required content | Owner |
| --- | --- | --- | --- |
| Product and onboarding overview | `README.md` | Purpose, status, architecture, setup, golden path, checks, contribution path, links | Tech Lead |
| Coding and documentation policy | `DOCUMENTATION_STANDARDS.md` | Rules, quality gates, lifecycle policies, templates | Tech Lead |
| Current release scope | `docs/v1-scope.md` | In scope, out of scope, API contract | Tech Lead |
| Operations runbook | `docs/ops-runbook.md` | Health, deployment, incidents, rollback, verification | Tech Lead or service operator |
| API contract | Generated OpenAPI document | Routes, schemas, status codes, auth, examples | Engineer changing the API |
| Release history | `CHANGELOG.md` | User-visible changes, deprecations, migrations | Release owner |
| Focused design or migration guide | `docs/<topic>.md` | Context, decision, rollout, rollback, status | Change owner |

Detailed policy and templates live outside the README because they serve
different tasks and change at different rates. The README links to them and
remains the fast onboarding path. Internal documents must live in this
repository as Markdown; external customer documentation is a separate
deliverable and must not be mixed into these files.

The Tech Lead is accountable for documentation health. Every author remains
responsible for documentation affected by their change. Ownership means
reviewing accuracy, not writing every document personally.

## 3. Python coding standard

### 3.1 Required baseline

All new or changed Python code must:

- target Python 3.12;
- pass `ruff check .`;
- pass `mypy arkana`;
- pass the relevant unit and integration tests;
- include complete type annotations, including parameters, returns, attributes,
  collections, and `None` behavior;
- avoid `Any` unless a boundary cannot be typed; each intentional `Any` must
  have a nearby explanation;
- use domain-specific names rather than abbreviations;
- keep domain logic independent of FastAPI, SQLAlchemy, and network clients;
- convert infrastructure failures into explicit application or API behavior;
- never log secrets, API keys, full credentials, or unnecessary sensitive data.

Functions should do one recognizable job. If a function needs a long
explanation of its control flow, first consider extracting named operations.
Public behavior must not depend on undocumented global state or call order.

### 3.2 Layer responsibilities

- `arkana/api/` owns HTTP transport, authentication middleware, validation, and
  response mapping.
- `arkana/application/` owns use-case orchestration and transaction/workflow
  coordination.
- `arkana/domain/` owns deterministic business rules, scoring, signals, and
  campaign concepts.
- `arkana/infrastructure/` owns databases, HTTP/DNS/RDAP clients, and other
  external adapters.

Dependencies should point inward: API and infrastructure may call application
or domain code; domain code must not import API or infrastructure code. A pull
request that crosses these boundaries must explain why.

### 3.3 Docstrings

Use Google-style docstrings. A docstring is required for:

- every module whose purpose or constraints are not obvious from its name;
- every public class, function, method, and exported constant;
- private code with non-obvious contracts, side effects, security constraints,
  or failure behavior.

A docstring must explain the contract, not repeat the signature. Include only
applicable sections: `Args`, `Returns`, `Raises`, `Yields`, `Attributes`, and
`Note`. Types belong in annotations; do not duplicate them in prose.

```python
def calculate_risk(signals: Sequence[Signal], version: str) -> Scorecard:
    """Calculate a deterministic risk score for extracted signals.

    The same signals and scoring version always produce the same scorecard.

    Args:
        signals: Validated signals produced by the extraction pipeline.
        version: Registered scoring-rules version.

    Returns:
        The score, verdict, and version used for the calculation.

    Raises:
        UnknownScoringVersionError: If `version` is not registered.
    """
```

Do not document trivial implementation details, restate default values visible
in a signature, or maintain hand-written lists of symbols that can be generated.

### 3.4 Comments

Comments should explain **why** code exists, a security or domain constraint, an
invariant, or why an apparently simpler approach is unsafe. Because the team
includes junior engineers, a short educational explanation is encouraged for
unfamiliar security and threat-intelligence concepts.

Comments must remain close to the affected code. `TODO` and `FIXME` comments
must include an issue identifier and a removal condition:

```python
# TODO(ARK-123): Remove the API-key fallback after all clients use OAuth.
```

Do not narrate syntax, preserve commented-out code, or use a comment to hide
unclear naming or structure.

### 3.5 Errors, logging, and tests

- Raise specific exceptions and preserve causes with `raise ... from exc`.
- Error messages should state the failed operation and actionable context while
  excluding secrets.
- Structured logs should carry stable identifiers such as `scan_id`; do not use
  logs as the only record of a business event.
- Bug fixes must include a regression test that fails before the fix.
- Features must test normal behavior, relevant boundary cases, and expected
  failures.
- Unit tests should cover domain rules without external services. Integration
  tests should cover database, API, and adapter boundaries.
- Test names should describe behavior and expected result.

## 4. Project documentation standard

### 4.1 README

The README must answer, in this order:

1. What is Arkana, who is it for, and what problem does it solve?
2. What is implemented now?
3. How is the system structured and how does one request flow through it?
4. How does a new engineer run the system and complete the golden path?
5. How are checks run, and where should a change be made?
6. Where are scope, operations, standards, API, and release details?

Commands must be copyable from the repository root. Placeholder commands must
be visibly marked. When a command changes, the same pull request must update the
README.

### 4.2 System overview

The README must contain a fixed system overview with:

- major runtime components and external dependencies;
- layer boundaries and allowed responsibilities;
- the scan request's end-to-end flow;
- storage and background-processing behavior;
- links to scope and operations details.

The overview must describe the current system, not a target architecture.
Architecture Decision Records and a full threat model are intentionally deferred
from this draft and must be added in a later standards review.

### 4.3 API documentation

FastAPI's generated OpenAPI schema is the canonical route and schema reference.
Every endpoint must document:

- purpose and authentication requirement;
- request and response models;
- success and error status codes;
- stable identifier formats;
- side effects and asynchronous behavior;
- at least one realistic, non-sensitive example.

An API change must update schemas, tests, OpenAPI metadata, README examples when
affected, and `CHANGELOG.md`. OpenAPI descriptions must not promise behavior
that is absent from tests.

### 4.4 Operations documentation

Any change to startup, configuration, dependencies, migrations, health checks,
deployment, recovery, or observability must update `docs/ops-runbook.md`.
Configuration documentation must state purpose, format, default, whether it is
secret, and whether changing it requires a restart.

A runbook procedure is complete only when it includes:

1. symptom or trigger;
2. impact;
3. diagnostic evidence;
4. numbered recovery steps;
5. rollback or stop condition;
6. verification;
7. escalation owner.

### 4.5 Design and domain documentation

Create a focused `docs/<topic>.md` when a change introduces a cross-layer
workflow, migration, difficult domain concept, or staged rollout that would
overload the README or a docstring. State whether the document describes current
behavior, a proposal, or a migration in progress.

Security-domain terms should be defined on first use. Explain how a concept
affects Arkana rather than giving a generic dictionary definition.

## 5. Onboarding standard

The onboarding path targets a meaningful bug fix or feature in two to four
weeks. The README must provide the golden path: start the stack, verify health,
submit a scan, retrieve its result, run checks, and locate each participating
layer.

Expected progression:

- **Days 1–3:** run the golden path, read the system overview and v1 scope, and
  trace one scan through API, application, domain, and infrastructure code.
- **Week 1:** run all checks, pair on a small test or documentation improvement,
  and review one merged pull request.
- **Weeks 2–4:** ship a scoped bug fix or feature with tests and corresponding
  documentation.

The Tech Lead must test the onboarding path at least once per release or assign
another engineer to do so from a clean checkout. Confusing or stale steps are
product defects and should be tracked.

## 6. Pull request and review standard

Pull requests should be small enough to review coherently and must state:

- the problem and intended outcome;
- the implementation and important trade-offs;
- tests and manual verification performed;
- documentation and API-contract impact;
- migration, deployment, compatibility, and rollback impact;
- follow-up work that is explicitly out of scope.

Reviewers verify behavior, layer boundaries, typing, tests, operational impact,
and documentation accuracy. The author must either update affected docs or
write “No documentation impact” with a concrete reason.

Documentation checks are highly enforced through CI visibility but are
initially non-blocking warnings. Linting, typing, tests, migration checks, and
documentation-build results must appear on every pull request. The Tech Lead
reviews warning trends each release and promotes stable, low-noise checks to
merge-blocking status. A warning is not permission to ignore a known defect.

## 7. Versioning, changelog, and deprecation

Arkana uses Semantic Versioning (`MAJOR.MINOR.PATCH`):

- **MAJOR:** incompatible API or persisted-contract changes;
- **MINOR:** backward-compatible functionality;
- **PATCH:** backward-compatible fixes.

Before `1.0.0`, compatibility may change in a minor release, but the changelog
and migration guidance remain required. Scoring-rule versions are business
contract versions and must not be silently tied to package versions.

`CHANGELOG.md` must follow Keep a Changelog categories under an `Unreleased`
heading: Added, Changed, Deprecated, Removed, Fixed, and Security. Record
consumer- or operator-visible effects, not commit history.

Deprecations must:

1. name the deprecated behavior and replacement;
2. be announced in OpenAPI metadata and `CHANGELOG.md`;
3. include a migration example and target removal version/date;
4. remain supported for at least two bi-weekly releases unless an active
   security issue requires accelerated removal;
5. be removed only in a version that permits the compatibility break.

## 8. Automated documentation controls

The target documentation pipeline is Markdown rendered with MkDocs and built by
Read the Docs. Read the Docs hosts and builds the site; it is not the authoring
format. Until that pipeline is configured, Markdown in the repository remains
canonical.

CI should report:

- MkDocs build warnings and invalid navigation;
- broken internal links;
- Python examples that can be executed safely;
- stale generated OpenAPI output, if an OpenAPI artifact is committed;
- Ruff, mypy, tests, coverage, and migration validation.

Checks should be introduced as warnings, tuned to avoid noise, then made
merge-blocking. Generated documentation must never be manually edited.

## 9. Templates

### Pull request documentation checklist

```markdown
## Problem and outcome

## Implementation and trade-offs

## Verification
- [ ] Relevant tests added or updated
- [ ] `ruff check .`
- [ ] `mypy arkana`
- [ ] Relevant pytest suites
- [ ] Golden path manually verified when applicable

## Contract and documentation impact
- [ ] README
- [ ] OpenAPI schemas/descriptions/examples
- [ ] Operations runbook/configuration
- [ ] Scope or focused design document
- [ ] CHANGELOG
- [ ] No documentation impact (explain why)

## Deployment, compatibility, and rollback

## Out of scope
```

### Focused design or migration document

```markdown
# <Title>

**Status:** Proposed | In progress | Current | Retired
**Owner:** <name or role>
**Last verified:** YYYY-MM-DD

## Outcome
## Context and constraints
## Current behavior
## Proposed or changed behavior
## Data and API impact
## Security and operational impact
## Rollout and rollback
## Verification
## Known limitations and follow-up
```

### Runbook procedure

```markdown
### <Symptom or alert>

**Impact:** <user/system impact>
**Owner:** <role>

#### Diagnose
1. <command, dashboard, or evidence>

#### Recover
1. <safe action>

#### Stop or roll back when
- <condition>

#### Verify
1. <health check and end-to-end check>

#### Escalate
- <owner and required evidence>
```

### Changelog entry

```markdown
## [Unreleased]

### Added
- <capability and who benefits>

### Changed
- <behavior change and migration link>

### Deprecated
- <old behavior>, replaced by <new behavior>; removal target: <version/date>

### Fixed
- <observable defect and corrected behavior>
```

## 10. Deferred decisions

The following require dedicated discussion before becoming mandatory:

- Architecture Decision Record policy and template;
- threat-model scope, trust boundaries, review cadence, and ownership;
- customer-facing documentation standards;
- organization-wide reuse of this product-specific standard;
- observed onboarding bottlenecks and measurable ramp-time baselines.

Review this draft after two bi-weekly releases. Use feedback from the next
engineer onboarding cycle to remove low-value requirements and strengthen
missing controls.
