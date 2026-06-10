# RESTART-00 - Repository baseline checkpoint

## 1. Status

Project restart checkpoint after removal of the previous failing GitHub Actions workflow.

Current status:

- Old workflow `.github/workflows/ci.yml` was removed from `main`.
- Previous CI recovery PR #13 was closed without merge.
- Previous CI recovery issue #12 was closed as completed after workflow reset.
- No new MVP feature work is allowed until the repository baseline is reviewed.
- MVP-06 remains blocked.

## 2. Active project roles

The project is managed with the following roles:

- Project Manager: scope, planning, deliverables, risks, Definition of Done.
- Software Architect: architecture, data model, WinMentor/WMS integrations.
- Lead Developer: repository structure, backend, frontend, API, modular implementation.
- QA Engineer: testing, security, acceptance criteria, Go/No-Go.
- UI/UX Designer: user flows, navigation and operational screens.

## 3. Project scope

The application is a separate web layer for reconciliation between WMS/xTrack and WME/WinMentor through ERP-controlled imports.

The application must remain read-only toward WMS and WME in the MVP phase.

Core rule:

> Any operation recorded in WME must also be done or logically verifiable in WMS.

## 4. Current repository baseline

Existing areas:

- Documentation for technical scope, data model, matching rules, UI flows and QA.
- Backend FastAPI structure.
- SQLAlchemy data model.
- Import parsers for WMS and WME fallback files.
- Normalization rules and service.
- Canonicalization bucket rules and service.
- Minimal frontend React/Vite shell.
- Docker and local development documentation.

Current intentional gap:

- No active GitHub Actions workflow after reset.
- No matching engine v1 yet.
- No reconciliation run API yet.
- No dashboard or operational reconciliation UI yet.
- No final reporting module yet.

## 5. Known risks

### Project management risks

- Previous work advanced through several MVP stages while CI was failing.
- Direct commits to `main` created instability.
- The project needs controlled checkpoints before further implementation.

### Architecture risks

- Matching and netting are not implemented yet.
- The import/normalization/canonicalization layers must remain audit-friendly and deterministic.
- Future ERP integration must not write back into WMS or WME during MVP.

### Backend risks

- Tests can fail if simple checks import the full FastAPI app and all routers.
- Dependency installation must be validated before reintroducing CI.
- Parser modules depend on pandas/openpyxl and need controlled test fixtures.

### Frontend risks

- Frontend dependencies should be stabilized before a strict CI build is reintroduced.
- Current UI is only a minimal shell, not an operational screen.

### QA risks

- There is currently no active automated gate.
- NOT_MATCH must not appear before normalization, canonicalization, matching and netting.
- No production or daily-use readiness may be claimed.

### UI/UX risks

- Operational screens are only documented, not implemented.
- Operator workflows must show events and rules before final totals.

## 6. Temporary working rules

Until a new baseline is accepted:

1. No MVP-06 implementation.
2. No new workflow until repository baseline is reviewed.
3. No production-ready or release claims.
4. Prefer small, narrow changes.
5. Any new workflow must start minimal and expand gradually.
6. Read-only MVP boundary remains mandatory.

## 7. Recommended next steps

### Step 1 - Repository audit

Review core backend and frontend files for import errors, dependency risks and broken tests.

### Step 2 - Dependency stabilization

Stabilize backend and frontend dependencies before creating a new workflow.

### Step 3 - Minimal local-equivalent checks

Define the smallest reliable checks:

- Python import smoke check.
- Backend unit test subset.
- Frontend TypeScript check.

### Step 4 - New minimal workflow

Only after Steps 1-3 are accepted, add a new minimal workflow.

### Step 5 - MVP-06 planning

Resume MVP-06 only after the new minimal workflow is green.

## 8. Definition of Done for RESTART-00

RESTART-00 is complete when:

- The old workflow remains removed.
- The obsolete CI recovery PR is closed without merge.
- The obsolete CI recovery issue is closed.
- This baseline document exists in `docs/`.
- The next checkpoint is clearly defined.

## 9. Go/No-Go

Current verdict:

**NO-GO for MVP-06.**

Allowed work:

- Repository audit.
- Dependency stabilization.
- Test isolation.
- Controlled CI reintroduction.

Blocked work:

- Matching engine implementation.
- Reconciliation run API.
- Dashboard UI.
- Product reconciliation UI.
- Release or production readiness promotion.
