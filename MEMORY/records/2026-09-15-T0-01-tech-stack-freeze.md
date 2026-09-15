# T0-01 — Freeze the tech stack

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Task** | `TASKS/PHASE-0-FOUNDATION.md` § T0-01 |
| **Phase** | Phase 0 |
| **Surface** | infra / docs |
| **Author** | Claude (scaffolding session) |
| **Commits / PR** | — (documentation-only session, no repo/CI exists yet) |
| **Status** | Completed |

---

## What Changed

Every open tech-stack question in `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` is now answered: mobile is native Android (Kotlin/Compose) + native iOS (Swift/SwiftUI), backend is Node.js/TypeScript/Express/Prisma/PostgreSQL+PostGIS/Redis/BullMQ with custom JWT auth. Three `CODING_STANDARDS.md` documents were written (`backend/`, `android/`, `ios/`) as the detail-level reference for each.

> **Superseded in part (same day):** the backend framework was changed from Express to NestJS (ADR-010) and storage was made driver-agnostic with local disk as the default (ADR-011). This record is left as written; see `MEMORY/records/2026-09-15-ADR-010-011-nestjs-storage-driver.md`.

## Why

The user asked for coding conventions modeled on `callibrator/backend/docs/CODING_STANDARDS.md`, and specified Android + iOS as the target platforms explicitly, with instructions to decide the backend stack directly ("putuskan saja yang terbaik untuk platform ini"). Writing a coding standards document meaningfully requires the stack to be decided first — so this session resolved `T0-01` as a prerequisite rather than leaving it `TODO` underneath an unfrozen assumption.

## How

- Cloned `callibrator` to read its actual `CODING_STANDARDS.md` structure and stack (Express, Sequelize, PostgreSQL, Redis, RabbitMQ, JS/CommonJS, layered controller/service/route with a `success()` response envelope), rather than inventing a convention from scratch.
- Chose Express to match `callibrator`'s shape, so its layered controller/service/route convention and response envelope carry over directly; swapped Sequelize for Prisma and JavaScript for TypeScript, since GPS/metric code benefits specifically from static types.
- For mobile, read the user's message as a decision for native (not cross-platform) given both OSes were named specifically in the context of requesting platform-specific standards, and because `docs/13-GPS/00-GPS-ARCHITECTURE.md`'s background-recording requirements are exactly where cross-platform frameworks add friction — captured in ADR-006.

## Files and Components Touched

| Path | Change |
|---|---|
| `MEMORY/DECISIONS.md` | Added ADR-006 (mobile), ADR-007 (backend); updated Decisions Pending table |
| `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` | Tech stack table, component diagram, and directory references updated from "usulan" to frozen decisions |
| `CLAUDE.md`, `AGENTS.md` | Directory layout and "Assumed Tech Stack" sections updated (`mobile/` → `android/` + `ios/`) |
| `TASKS/PHASE-0-FOUNDATION.md` | `T0-01` marked `DONE`; `T0-02` updated to reference three directories; `T0-09` split into `T0-09` (Android) + `T0-09B` (iOS); `T0-10` dependency updated |
| `TASKS/PROGRESS.md` | Task count and status updated to match |
| `TASKS/BACKLOG.md` | OQ-01, OQ-03, OQ-04 struck through as resolved |
| `TASKS/00-TASK-CONVENTIONS.md` | `Surface` field values updated to `backend`/`android`/`ios`/`infra`, with a note on when to split a cross-platform task into sub-tasks |
| `TASKS/PHASE-1-MVP-TRACKING.md`, `TASKS/PHASE-2-MVP-SOCIAL-SHARE.md` | `Surface: mobile` → `Surface: android, ios` throughout |
| `backend/docs/CODING_STANDARDS.md` | Created |
| `android/docs/CODING_STANDARDS.md` | Created |
| `ios/docs/CODING_STANDARDS.md` | Created |

## Decisions Made

| Decision | Rationale | ADR |
|---|---|---|
| Native Android + native iOS, no cross-platform framework | Background GPS recording needs deep platform-specific integration regardless; cross-platform's main benefit (shared UI code) matters less than the friction it adds here | ADR-006 |
| Node.js + TypeScript + Express + Prisma (not Go, not Sequelize) | Same shape as `callibrator`, upgraded for type safety | ADR-007 |
| Custom JWT auth, not a third-party provider | Team already operates this successfully in `callibrator` | ADR-007 |

## Deviations from the Plan

None — this task's own Definition of Done was "decide and record," which is what happened. The only note: `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` originally framed these as open "usulan" pending team confirmation; this session resolved them based on the user's explicit instruction to decide, rather than waiting for a separate confirmation round. If the actual engineering team disagrees once assembled, that's a fresh deviation to raise, not a reason this record is wrong.

## Tests Added

| Layer | What it covers |
|---|---|
| Unit | Not applicable — no code exists yet |
| Integration | Not applicable |
| E2E | Not applicable |
| Security | Not applicable |

## Definition of Done Verification

- [x] Mobile platform decision recorded (ADR-006)
- [x] Backend language/framework decision recorded (ADR-007)
- [x] Auth build-vs-buy decision recorded (folded into ADR-007)
- [x] `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` updated
- [x] `TASKS/PROGRESS.md` and the phase file updated in this same work session
- [ ] CI green — **waived**: no repository/CI pipeline exists yet (`T0-02`–`T0-10` not started); not applicable to a documentation-only task

## What Did Not Work

Nothing abandoned. One thing worth naming: initially attempted to find the `zed-auth` and `callibrator` repos via `web_search`, which failed to index either (both are small/newly-created repos) — `git clone` directly against `github.com` succeeded immediately since the domain is allowlisted for the sandbox's network. Worth remembering for future sessions: don't conclude a repo is private/inaccessible from a failed search alone.

## Follow-Ups and Open Questions

- `T0-02` onward (actual repo initialization) is now unblocked and ready to start.
- The Android/iOS coding standards documents describe patterns (Hilt DI, SwiftData, BullMQ jobs) that haven't been validated against a real running codebase yet — expect minor corrections once `T0-04`, `T0-09`, `T0-09B` actually stand the projects up. That's normal; flagging so nobody mistakes these documents for battle-tested rather than well-reasoned-but-unverified.

## What to Watch

If the actual founding engineers have stronger existing expertise in a different stack (e.g. genuinely no Node.js experience, strong Go background instead), ADR-007 should be revisited before `T0-04` starts — this decision was made by an AI agent optimizing for consistency with `callibrator` and general fit, not by interviewing the people who'll maintain the code daily.
