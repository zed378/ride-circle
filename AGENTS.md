# AGENTS.md

Instructions for any AI coding agent (Claude Code, Codex, or otherwise) working in this repository. This file follows the [agents.md](https://agents.md) convention and should stay consistent with `CLAUDE.md` — if you update one, update the other.

## Project Summary

This repository implements **RideCircle**: a motorcycle-native ride-tracking and social-sharing platform. The full long-term product plan exists under **`docs/`** (48 category folders, `docs/README.md` is the way in) and is the authoritative source for requirements, domain model, and architecture. **Only two pillars are currently in scope**: Ride Tracking and Social Media Share — every `docs/` file is tagged `Status: MVP` or `Status: Post-MVP`; implement only the former. Do not re-derive requirements from scratch — look them up.

## Setup Commands

```bash
# Backend (NestJS + TypeScript)
cd backend && npm install

# Android (Kotlin)
cd android && ./gradlew build

# iOS (Swift)
cd ios && xcodebuild -resolvePackageDependencies

# Web (Next.js)
cd web && npm install
```

## Build & Test Commands

```bash
# Backend
cd backend && npm run build
cd backend && npm test
cd backend && npm run lint

# Android
cd android && ./gradlew test
cd android && ./gradlew lint

# iOS
cd ios && xcodebuild test -scheme RideCircle

# Web
cd web && npm run build
cd web && npm test
cd web && npm run lint
```

Run the relevant test command(s) before considering any change complete. A change touching GPS metric calculation or the ride state machine requires the full backend test suite, not just the package you edited — `docs/13-GPS/` and `docs/16-RIDE/` describe cross-cutting invariants (e.g. riding-time calculation depends on pause events) that a narrow test run can miss.

## Where to Find the Spec for Any Task

| Task | Primary document(s) |
|---|---|
| First time in the repo | `README.md`, `docs/47-ROADMAP/01-MVP-SCOPE.md` |
| System architecture | `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` |
| Database/migrations | `docs/07-DOMAIN/00-DOMAIN-MODEL.md` and entity files |
| Ride recording / GPS / metrics | `docs/13-GPS/`, `docs/16-RIDE/`, `docs/01-PRD/04-RIDE-RECORDING.md`, `docs/01-PRD/06-RIDE-ANALYTICS.md` |
| Auth / profile | `docs/01-PRD/01-AUTHENTICATION.md`, `docs/01-PRD/02-RIDER-PROFILE.md` |
| Feed / social | `docs/24-SOCIAL/`, `docs/01-PRD/14-SOCIAL-FEED.md`, `docs/01-PRD/15-COMMENTS-KUDOS.md` |
| Landing page | `docs/01-PRD/22-LANDING-PAGE.md`, `web/docs/CODING_STANDARDS.md` |
| Admin moderation dashboard | `docs/01-PRD/21-ADMIN-MODERATION.md`, `web/docs/CODING_STANDARDS.md` |
| Location privacy | `docs/45-COMPLIANCE/03-LOCATION-DATA.md` |
| What's in scope right now | `docs/47-ROADMAP/01-MVP-SCOPE.md`, `TASKS/PROGRESS.md` |
| Definition of done | `TASKS/00-TASK-CONVENTIONS.md` |

## Feature Workflow

For any non-trivial task: read the task card in the relevant `TASKS/PHASE-N-....md` file, follow every `Docs refs` link, confirm dependencies are `DONE` in `TASKS/PROGRESS.md`, implement, then write a `MEMORY/records/` change record before marking the task `DONE`. Skip the full record only for trivial, clearly-scoped changes (typo fixes, config tweaks) — anything touching GPS calculation, the ride state machine, or the social graph's data model should go through the full workflow.

## Code Style

Full detail lives in each surface's own coding standards document — read it before writing code in that surface:

- Backend: `backend/docs/CODING_STANDARDS.md`
- Android: `android/docs/CODING_STANDARDS.md`
- iOS: `ios/docs/CODING_STANDARDS.md`
- Web (landing + admin): `web/docs/CODING_STANDARDS.md`

- **Commits**: scoped to one task; reference the task ID and the `docs/` document(s) implemented, per `TASKS/00-TASK-CONVENTIONS.md`.

## Hard Rules (Do Not Violate)

1. Implement only `docs/` files tagged `Status: MVP`. For `Status: Post-MVP` work, stop and confirm with the user explicitly before writing any code.
2. A new `Ride` defaults to `visibility: private` — never default to public (`docs/45-COMPLIANCE/03-LOCATION-DATA.md`).
3. GPS-derived metrics (speed, distance) must apply the documented filtering (low-confidence point exclusion, 220 km/h jump cap) — an unfiltered number is a wrong number, not a shortcut.
4. Do not implement a later-phase feature while an earlier phase is incomplete (`TASKS/README.md` § The Phase Rule).
5. Do not create database tables, models, or scaffolding for Post-MVP entities (`Motorcycle`, `Club`, `Event`, `Segment`, etc.) in anticipation of future need (`docs/07-DOMAIN/00-DOMAIN-MODEL.md` § Catatan desain).
6. `docs/` is reference documentation, not implementation output — don't edit it as a side effect of feature work; if the requirement itself needs to change, that's a deliberate, separate action the user should be aware of (Deviation Protocol, `TASKS/00-TASK-CONVENTIONS.md`).
7. Never log raw GPS point traces, passwords, or auth tokens.
8. Every `DONE` task has a corresponding `MEMORY/records/` entry — a task without one is not done, however finished the code looks (`MEMORY/README.md`).
9. Do not resolve an item in `TASKS/BACKLOG.md` § Open Questions or `MEMORY/DECISIONS.md` § Decisions Pending unilaterally — raise it with the user.
10. Admin authentication (`web/`, `/admin/*`) is a separate flow from rider authentication (`docs/01-PRD/01-AUTHENTICATION.md`) — never a role flag layered on top of a rider JWT (`docs/01-PRD/21-ADMIN-MODERATION.md`).
11. All file storage goes through the `StorageDriver` interface (`backend/docs/CODING_STANDARDS.md` §9, ADR-011) — never `fs` or a cloud SDK directly from domain code, and never persist a URL or filesystem path where a storage key belongs.

## PR / Change Instructions

- Link the PR description to the specific `docs/` sections the change implements, so reviewers can check against the requirement rather than only against the diff.
- State the task ID and which test layers were added/run.
- If the change deviates from `docs/` (a library limitation, a discovered ambiguity), state the deviation explicitly and link the ADR in `MEMORY/DECISIONS.md` — never silently diverge.

## When Uncertain

Ask rather than assume. `docs/` is detailed specifically so implementation doesn't require guessing; if an answer isn't there, that's a genuine gap to raise via `TASKS/BACKLOG.md`, not a decision to make silently.
