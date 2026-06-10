# RESTART-01 - Repository audit and dependency stabilization

## 1. Status

This checkpoint follows RESTART-00 and documents the current repository audit before reintroducing any GitHub Actions workflow or starting MVP-06.

Current status:

- No active `.github/workflows/ci.yml` workflow on `main`.
- MVP-06 remains blocked.
- No release or production-readiness claim is allowed.
- The MVP remains read-only toward WMS and WME.

## 2. Issue tracking

Tracking issue:

- #14 - RESTART-01: Repository audit and dependency stabilization

## 3. Backend audit

### 3.1 Packaging

Backend packaging has been partially stabilized:

- explicit build system using setuptools and wheel;
- Python constrained to `>=3.11,<3.12`;
- core backend dependencies pinned;
- dev dependencies pinned;
- package discovery configured for `app*`.

This is a positive baseline for reintroducing a backend workflow later.

### 3.2 Backend checks currently intended

The future backend workflow should not start with a broad gate. It should be introduced gradually.

Recommended first checks:

1. install backend package;
2. import smoke check for selected modules;
3. run a minimal pytest subset;
4. only then expand to the full test suite.

### 3.3 Backend risks

Known risks:

- `app.main` imports all API routers at module import time.
- A simple health test that imports `app.main` also imports upload/API/database-related modules indirectly.
- Parser modules depend on pandas/openpyxl.
- Full API tests should use controlled database fixtures before being required in CI.

Recommended backend actions before workflow reintroduction:

1. isolate `health_check` into a lightweight module or keep the health test as a FastAPI integration test only after dependencies are stable;
2. define a minimal import smoke test list;
3. keep `ruff` initially focused on real Python errors;
4. avoid adding matching engine code until these checks are stable.

## 4. Frontend audit

### 4.1 Current frontend package status

The frontend is a minimal React/Vite/TypeScript shell.

Current package scripts:

- `dev`;
- `build`;
- `preview`;
- `lint` as `tsc --noEmit`.

### 4.2 Frontend risks

Known risks:

- `package.json` still uses `latest` for several frontend packages.
- `latest` creates non-reproducible installs and can break CI unexpectedly.
- TypeScript is strict, which is good long-term but risky while the dependency baseline is still moving.
- There is no lockfile committed yet.

Recommended frontend actions before workflow reintroduction:

1. pin frontend dependency versions;
2. add a lockfile after dependencies are confirmed;
3. keep the first frontend workflow to `npm install` plus `npm run lint` or `npm run build`, not both at once if instability continues;
4. expand gradually only after a green baseline.

## 5. Test audit

Current testing is useful but not yet a complete acceptance gate.

Risk areas:

- tests that import the full FastAPI application may fail due to unrelated router or dependency imports;
- parser tests require pandas/openpyxl availability;
- database model tests verify metadata but do not validate migrations against a live database;
- no matching/netting tests exist yet because MVP-06 is blocked.

Recommended test sequence:

1. pure unit tests for normalization rules;
2. pure unit tests for canonicalization rules;
3. parser tests with controlled in-memory dataframes;
4. API tests only after test database setup is explicit;
5. matching tests only in MVP-06 after CI baseline is green.

## 6. QA Go/No-Go

Current verdict:

**NO-GO for MVP-06.**

Allowed next work:

- dependency stabilization;
- test isolation;
- minimal smoke-test definition;
- controlled reintroduction of a small workflow.

Blocked next work:

- matching engine implementation;
- reconciliation run API;
- dashboard UI;
- product reconciliation UI;
- release or production-readiness promotion.

## 7. Recommended RESTART-02

Next checkpoint:

**RESTART-02 - Dependency stabilization patch**

Scope:

- stabilize frontend dependencies;
- isolate health/test imports;
- define minimal smoke-test commands;
- no workflow yet unless explicitly approved after review.

## 8. Definition of Done for RESTART-01

RESTART-01 is complete when:

- tracking issue #14 exists;
- backend audit is documented;
- frontend audit is documented;
- test risks are documented;
- RESTART-02 is defined as the next checkpoint;
- MVP-06 remains blocked.
