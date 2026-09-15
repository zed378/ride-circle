# Progress Board

Single source of truth for where the project stands. Updated in the same commit as the work it describes (`00-TASK-CONVENTIONS.md` global DoD item 7).

**Last updated**: 2026-09-15
**Current phase**: Phase 0 — Foundation, 1 / 12 done. Tech stack frozen (`T0-01`, ADR-006/008/010/011 — backend on NestJS, storage driver-agnostic with local disk default); `docs/` scaffolding complete; no application code exists yet.
**Overall**: 1 / 46 tasks done

Status values: `TODO` · `BLOCKED` · `WIP` · `REVIEW` · `DONE` · `DROPPED`
Sizes: `S` under half a day · `M` one to two days · `L` several days · `XL` must be split

---

## Phase Summary

| Phase | Tasks | Done | Status | Gate to enter |
|---|---|---|---|---|
| [Phase 0 — Foundation](./PHASE-0-FOUNDATION.md) | 12 | 1 | **ACTIVE** | — |
| [Phase 1 — MVP: Ride Tracking](./PHASE-1-MVP-TRACKING.md) | 14 | 0 | Not started | Phase 0 exit |
| [Phase 2 — MVP: Social Media Share](./PHASE-2-MVP-SOCIAL-SHARE.md) | 12 | 0 | Not started | Phase 0 exit |
| [Phase 3 — Web: Landing + Admin](./PHASE-3-WEB.md) | 8 | 0 | Not started | Phase 0 exit (landing tasks); Phase 2 for admin tasks |

> Phase 1 and Phase 2 may run **in parallel** once Phase 0 is done — see `TASKS/README.md` § The Phase Rule. `T2-06` onward in Phase 2 additionally needs `T1-10` from Phase 1. Phase 3's landing-page tasks (`T3-01`–`T3-03`) only need Phase 0; its admin tasks (`T3-04` onward) need `T2-06`/`T2-09` from Phase 2, since moderation acts on posts and comments that don't exist until Social Share does.
>
> There is no Phase 4 file. Everything past MVP is `docs/`-only (Post-MVP status) until a deliberate decision to start the next phase — see `docs/47-ROADMAP/00-ROADMAP.md`.

---

## Phase 0 — Foundation

| ID | Task | Size | Status | Depends on |
|---|---|---|---|---|
| T0-01 | Confirm and freeze the tech stack | S | **DONE** | — |
| T0-02 | Initialize repository structure | S | TODO | T0-01 |
| T0-03 | Git conventions, branch strategy, CI skeleton | S | TODO | T0-02 |
| T0-04 | Backend service skeleton | M | TODO | T0-02 |
| T0-05 | Local dev environment (Docker Compose) | M | TODO | T0-04 |
| T0-06 | Migration tooling and baseline migration | S | TODO | T0-05 |
| T0-07 | Core MVP schema | L | TODO | T0-06 |
| T0-08 | Auth scaffolding (JWT + global AuthGuard) | M | TODO | T0-07 |
| T0-09 | Android app skeleton | M | TODO | T0-01, T0-02 |
| T0-09B | iOS app skeleton | M | TODO | T0-01, T0-02 |
| T0-10 | CI: full pipeline | S | TODO | T0-07, T0-09, T0-09B |
| T0-11 | Storage module (driver-agnostic) + local disk driver | M | TODO | T0-04 |

## Phase 1 — MVP: Ride Tracking

| ID | Task | Size | Status | Depends on |
|---|---|---|---|---|
| T1-01 | Location sampling module | M | TODO | T0-09 |
| T1-02 | Local point buffer + periodic disk write | S | TODO | T1-01 |
| T1-03 | RecordingService (foreground/background) | L | TODO | T1-02 |
| T1-04 | Ride lifecycle state machine | M | TODO | T0-07, T1-03 |
| T1-05 | Pause/resume + riding-time calculation | S | TODO | T1-04 |
| T1-06 | Batch GPS point upload endpoint | M | TODO | T0-08, T0-11, T1-04 |
| T1-07 | Polyline simplify + encode job | S | TODO | T1-06 |
| T1-08 | Distance calculation | M | TODO | T1-06 |
| T1-09 | Speed calculation | S | TODO | T1-08 |
| T1-10 | Ride completion pipeline | M | TODO | T1-07, T1-08, T1-09 |
| T1-11 | Ride history endpoints + UI | M | TODO | T1-10 |
| T1-12 | Edit / soft-delete ride | S | TODO | T1-11 |
| T1-13 | Mobile recording UI | M | TODO | T1-04, T1-05 |
| T1-14 | Crash-recovery flow | M | TODO | T1-02, T1-13 |

## Phase 2 — MVP: Social Media Share

| ID | Task | Size | Status | Depends on |
|---|---|---|---|---|
| T2-01 | Register / login (email + password) | M | TODO | T0-08 |
| T2-02 | OAuth Google | M | TODO | T2-01 |
| T2-03 | Reset password | S | TODO | T2-01 |
| T2-04 | Rider profile CRUD + stats display | M | TODO | T2-01 |
| T2-05 | Follow / unfollow | S | TODO | T2-04 |
| T2-06 | Publish / unpublish ride | M | TODO | T1-10, T2-04 |
| T2-07 | Feed endpoint + UI | M | TODO | T2-05, T2-06 |
| T2-08 | Kudos | S | TODO | T2-06 |
| T2-09 | Comments | S | TODO | T2-06 |
| T2-10 | In-app notifications | M | TODO | T2-05, T2-08, T2-09 |
| T2-11 | Share card rendering | M | TODO | T1-10 |
| T2-12 | Native share sheet integration | S | TODO | T2-11 |

## Phase 3 — Web: Landing Page + Admin Dashboard

| ID | Task | Size | Status | Depends on |
|---|---|---|---|---|
| T3-01 | Web app skeleton | S | TODO | T0-01, T0-02 |
| T3-02 | Landing page sections | M | TODO | T3-01 |
| T3-03 | SEO & performance | S | TODO | T3-02 |
| T3-04 | Admin auth (separate from rider auth) | M | TODO | T0-08, T3-01 |
| T3-05 | Report data model + rider-side report action | M | TODO | T2-06, T2-09 |
| T3-06 | Reports queue screen | M | TODO | T3-04, T3-05 |
| T3-07 | Moderation actions + audit log | M | TODO | T3-06 |
| T3-08 | Rider search screen | S | TODO | T3-04 |
