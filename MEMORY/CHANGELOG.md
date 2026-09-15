# Changelog

Chronological summary of what changed, at a coarser grain than individual `MEMORY/records/` entries. User-visible or operationally significant changes only — not every internal refactor.

---

## 2026-09-15 — Backend moved to NestJS; storage made driver-agnostic

User decision, before any backend code existed. ADR-010: NestJS replaces Express (ADR-007 marked Superseded; Prisma, PostgreSQL/PostGIS, Redis, BullMQ, Zod, custom JWT carried forward). ADR-011: all file storage goes through a `StorageDriver` interface, default driver = the VM's local disk; S3-compatible becomes an optional drop-in driver instead of a required service. `backend/docs/CODING_STANDARDS.md` rewritten; `docs/08-ARCHITECTURE`, `CLAUDE.md`, `AGENTS.md`, `README.md`, and `TASKS/` updated. New task `T0-11` (storage module + local driver); Phase 0 now 12 tasks, 46 overall. Record: `MEMORY/records/2026-09-15-ADR-010-011-nestjs-storage-driver.md`.

## 2026-09-15 — Product name confirmed: RideCircle (OQ-09 resolved)

User answered directly: stay with RideCircle, not RIDELINE. ADR-009 recorded. `TASKS/specs/T3-02-landing-page.md` gained a substitution table (6 locations) at the end rather than an in-place edit of the pasted spec's body. `T3-02` unblocked.

## 2026-09-15 — Landing page spec added, blocked on a naming conflict

User pasted a detailed `claude -p` landing-page design/implementation brief. Stored as `TASKS/specs/T3-02-landing-page.md` (new `Spec required` pattern added to `TASKS/00-TASK-CONVENTIONS.md`) rather than executed immediately. `docs/ASSETS.md` scaffolded per the spec's image-licensing requirement.

Read-through found the spec names the product "RIDELINE" throughout, conflicting with "RideCircle" used everywhere else in this repo. `T3-02` set to `BLOCKED`, logged as `TASKS/BACKLOG.md` OQ-09 — not resolved silently, despite the spec's own instruction not to ask questions (that instruction governs the *build* step, not this intake step).

## 2026-09-15 — Web platform added (landing page + admin dashboard)

New `web/` platform: one Next.js app for the public landing page and an internal admin moderation dashboard (ADR-008, `MEMORY/records/2026-09-15-ADR-008-web-platform.md`). Modeled directly on `callibrator/frontend` and `callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md` — same envelope-unwrap discipline, same "errors are a UI state" rule, same Zustand conventions.

`docs/01-PRD/21-ADMIN-MODERATION.md` promoted from Post-MVP to MVP — a public social feed needs a moderation path from launch, not later. New `docs/01-PRD/22-LANDING-PAGE.md` written. `TASKS/PHASE-3-WEB.md` added (8 tasks). `docs/47-ROADMAP/01-MVP-SCOPE.md` updated to list both under "In scope."

## 2026-09-15 — Tech stack frozen, platform coding standards written

`T0-01` done (`MEMORY/records/2026-09-15-T0-01-tech-stack-freeze.md`). ADR-006: native Android (Kotlin/Compose) + native iOS (Swift/SwiftUI), no cross-platform framework. ADR-007: backend is Node.js + TypeScript + Express + Prisma + Zod + PostgreSQL/PostGIS + Redis + BullMQ + custom JWT — same shape as the team's `callibrator` project, upgraded for TypeScript. `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md`, `CLAUDE.md`, `AGENTS.md`, and all `TASKS/` files updated to match (`mobile/` → `android/` + `ios/`).

Three `CODING_STANDARDS.md` documents created — `backend/docs/`, `android/docs/`, `ios/docs/` — each modeled on `callibrator/backend/docs/CODING_STANDARDS.md`'s structure and level of detail, adapted per platform.

Still no application code — this is the last purely-planning milestone before `T0-02` (repo initialization) can start.

---

## 2026-09-15 — Documentation scaffolding

`docs/` created: 48 category folders (00–47), 414 files, each tagged `Status: MVP` or `Status: Post-MVP`. 31 MVP files written in full (requirements, domain schema, GPS/ride/social mechanics); the remainder of `13-GPS`/`16-RIDE`/`24-SOCIAL` (26 files) and all Post-MVP categories (358 files) are placeholders.

`TASKS/` and `MEMORY/` established following the execution-layer convention (task IDs, Definition of Done, ADR log). Two phases planned: Phase 0 (Foundation, 10 tasks) and Phase 1/Phase 2 (MVP Ride Tracking / MVP Social Media Share, 14 + 12 tasks), runnable in parallel after Phase 0.

Five ADRs recorded (`MEMORY/DECISIONS.md`): execution-layer adoption, MVP scope boundary, deferred live-tracking, a proposed (not yet accepted) privacy-zone requirement, and fan-out-on-read for the feed.

No code written yet — this entry marks the planning baseline, not a release.
