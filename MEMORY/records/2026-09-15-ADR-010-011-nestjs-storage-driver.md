# ADR-010 / ADR-011 — Backend to NestJS, storage driver-agnostic

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Task** | Amends `T0-01` (`TASKS/PHASE-0-FOUNDATION.md`); adds `T0-11` |
| **Phase** | Phase 0 |
| **Surface** | backend / infra / docs |
| **Author** | Claude (Claude Code session), per user decision |
| **Commits / PR** | — (repository has no commits yet) |
| **Status** | Completed |

---

## What Changed

Two decisions from the user, both made before any backend code existed:

1. **Backend framework is NestJS**, not Express (ADR-010, supersedes the framework part of ADR-007). Everything else in ADR-007 carries forward: TypeScript, Prisma, PostgreSQL + PostGIS, Redis, BullMQ, Zod, custom JWT, the response envelope.
2. **Storage is driver-agnostic, defaulting to the VM's local disk** (ADR-011). File storage goes through a `StorageDriver` interface; S3-compatible storage is an optional driver rather than a required service.

`backend/docs/CODING_STANDARDS.md` was rewritten for NestJS and gained a full storage section (§9). A new Phase 0 task, `T0-11`, covers the storage module and local driver.

## Why

The user asked for both directly ("mengubah keputusan saya untuk menggunakan NestJS sebagai backend… saya ingin driver storage agnostik. secara default gunakan local atau disk VM nya sendiri"). Making the switch now costs only documentation; after `T0-04` it would cost a rewrite.

## How

- **Cleaned up a half-finished earlier attempt.** An earlier session had rewritten ADR-007's body to say NestJS in place, added an "Update same day" note to the `T0-01` record, and changed only the header/TOC of `backend/docs/CODING_STANDARDS.md` — the body, `CLAUDE.md`, `README.md`, `docs/08-ARCHITECTURE/`, and `TASKS/` all still said Express/S3. `MEMORY/DECISIONS.md` says a superseded ADR stays in place with a pointer forward, and `MEMORY/README.md` says records are not retroactively edited. So ADR-007 was restored to its original Express decision with status "Superseded by ADR-010 / ADR-011", the `T0-01` record's edits were reverted to its original wording plus a forward pointer, and the new decisions were written as ADR-010 and ADR-011.
- **Kept Zod rather than adopting class-validator.** The earlier in-place ADR-007 rewrite had listed "class-validator + class-transformer with Zod as fallback". That would mean two validation systems (Zod is still needed for env config and job payloads). ADR-010 keeps Zod through a small custom `ZodValidationPipe`. This is a judgment call inside the user's decision, recorded as an alternative in ADR-010 so it can be revisited.
- **Secure-by-default auth.** A global `AuthGuard` requires a rider JWT unless a route is `@Public()`; `@AdminAuth()` switches to a separate admin secret, preserving `AGENTS.md` hard rule 10.
- **Storage design.** The interface is kept small (`put`/`get`/`exists`/`delete`/`publicUrl`). Visibility lives in the key prefix (`private/`, `public/`), so raw GPS points can never be served over HTTP whichever driver is active. The database stores keys only, so switching drivers means copying data, not migrating the schema. Only the `local` driver is in scope; `s3` is documented as a drop-in, checked by a shared contract test suite.

## Files and Components Touched

| Path | Change |
|---|---|
| `backend/docs/CODING_STANDARDS.md` | Rewritten for NestJS (modules, DI, global guard/interceptor/filter, `ZodValidationPipe`, `@nestjs/bullmq`, Vitest + SWC); new §9 Storage (Driver-Agnostic); env vars updated |
| `MEMORY/DECISIONS.md` | ADR-007 restored + marked Superseded; ADR-010 and ADR-011 added; Decisions Pending row for OQ-04 updated |
| `MEMORY/records/2026-09-15-T0-01-tech-stack-freeze.md` | Earlier retroactive edits reverted; forward pointer to this record added |
| `MEMORY/MEMORY-INDEX.md`, `MEMORY/CHANGELOG.md`, `MEMORY/GLOSSARY.md` | New entry; `Track` definition says driver-agnostic storage |
| `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` | Storage principle, component diagram, tech stack table (backend, validation, storage) |
| `docs/07-DOMAIN/03-RIDE.md` | `raw_points_ref` comment: storage key, not "pointer to object storage" |
| `docs/13-GPS/00-GPS-ARCHITECTURE.md`, `docs/45-COMPLIANCE/03-LOCATION-DATA.md` | "Object storage" wording → driver-agnostic storage |
| `CLAUDE.md`, `AGENTS.md` | Tech stack table / setup comment; new storage constraint (CLAUDE.md Non-Negotiable Constraints, AGENTS.md hard rule 11) |
| `README.md` | Backend line, ADR references, Phase 0 task count (12), overall count (46) |
| `TASKS/PHASE-0-FOUNDATION.md` | `T0-01` result; `T0-02`, `T0-04`, `T0-05` (volume instead of MinIO), `T0-08` (guard instead of middleware) updated; **`T0-11` added** |
| `TASKS/PHASE-1-MVP-TRACKING.md` | `T1-06` depends on `T0-11`, writes through `StorageDriver`; `T1-12` purge via `StorageDriver.delete()` |
| `TASKS/PHASE-3-WEB.md` | `T3-04` uses `@AdminAuth()` rather than a separate middleware |
| `TASKS/PROGRESS.md`, `TASKS/BACKLOG.md` | Counts, `T0-11` row, `T1-06` dependency, OQ-04 note |

## Decisions Made

| Decision | Rationale | ADR |
|---|---|---|
| NestJS on the default Express adapter | User decision; DI + module system + global guards/filters | ADR-010 |
| Zod via a custom pipe, not class-validator | One validation system for HTTP, env, and jobs | ADR-010 |
| `StorageDriver` interface, `local` default, `s3` later | User decision; simplest deployment, swappable later without a DB migration | ADR-011 |
| Visibility in the key prefix; DB stores keys only | Driver-independent privacy guarantee for raw GPS; no migration on driver switch | ADR-011 |

## Deviations from the Plan

`docs/` wording was amended in four files (`08-ARCHITECTURE`, `07-DOMAIN/03-RIDE`, `13-GPS/00`, `45-COMPLIANCE/03`). **No requirement changed.** Raw points still stay out of the RDBMS, and the 30-day retention and hard delete are unchanged. Only the phrase "object storage (S3-compatible)" was generalized. This was done deliberately as part of this decision, not as a side effect of feature work (`AGENTS.md` rule 6).

## Tests Added

| Layer | What it covers |
|---|---|
| Unit | Not applicable — documentation-only change, no code exists |
| Integration | Not applicable |
| E2E | Not applicable |
| Security | Not applicable |

## Definition of Done Verification

- [x] ADRs recorded (ADR-010, ADR-011); superseded ADR-007 left in place with forward pointer
- [x] `backend/docs/CODING_STANDARDS.md` consistent with both ADRs
- [x] Every Express / S3-only reference in `CLAUDE.md`, `AGENTS.md`, `README.md`, `docs/`, `TASKS/` updated (historical records and ADR-007 intentionally left describing what was decided at the time)
- [x] `TASKS/PROGRESS.md` and phase files updated in the same session
- [ ] CI green — **waived**: no repository/CI exists yet

## What Did Not Work

The earlier attempt edited ADR-007 and the `T0-01` record in place and stopped partway. That left the repo contradicting itself: the header said NestJS and the body said Express. It had to be unwound before the new ADRs could be written cleanly. The lesson: when a decision changes, write the new ADR first and then sweep references, rather than editing the old ADR's body.

## Follow-Ups and Open Questions

- `T0-11` is a new task. `T1-06` now depends on it.
- An `s3` driver is not scheduled. Build it before running more than one backend instance or moving the backend off a single VM (ADR-011 consequences).
- Storage backups: whoever provisions the VM (`docs/43-DEVOPS/`, Post-MVP folder) must include `STORAGE_LOCAL_ROOT` in backups/snapshots. No MVP task owns this yet; flag it at deployment time.

## What to Watch

- **Disk usage on the VM.** Raw GPS files grow with every ride, and the hard-delete job only removes soft-deleted rides.
- **Decorator metadata in tests.** If a Nest provider comes back `undefined` only under Vitest, `unplugin-swc` is missing or misconfigured.
- **Drift between drivers.** Any new `StorageDriver` method must land for every driver at once, with a contract test.
