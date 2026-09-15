# CLAUDE.md

Guidance for Claude Code when working in this repository. This project builds **RideCircle**, a motorcycle-native ride-tracking and social-sharing platform, following the documents in `docs/`.

**Read this file in full before writing any code.** It is shorter than `docs/` itself and tells you which document to open for any given task — don't skip straight to coding from assumptions.

## What This Repository Is

A platform for recording, sharing, and eventually managing motorcycle rides and rider communities — deliberately **not** "Strava with a motorcycle icon." `docs/` contains 48 category folders (numbered 00–47) covering the full long-term product vision. **Only two pillars are in scope right now: Ride Tracking and Social Media Share.** Nothing has been implemented yet unless a `backend/`, `android/`, or `ios/` directory already exists with code in it — check before assuming.

## Documentation Map — Read Before You Build

Every MVP requirement has already been written down. **Do not re-derive requirements, data models, or metric definitions from scratch — find the answer in `docs/` first.**

| If you're working on... | Read first |
|---|---|
| Anything at all, first time in this repo | `README.md`, `docs/47-ROADMAP/01-MVP-SCOPE.md`, `docs/00-PRODUCT/05-NON-GOALS.md` |
| Overall system design | `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` |
| Database schema | `docs/07-DOMAIN/00-DOMAIN-MODEL.md` and the entity-specific files in `docs/07-DOMAIN/` |
| Ride recording, GPS, pause/resume, metrics | `docs/13-GPS/`, `docs/16-RIDE/`, `docs/01-PRD/04-RIDE-RECORDING.md`, `docs/01-PRD/06-RIDE-ANALYTICS.md` |
| Auth / rider profile | `docs/01-PRD/01-AUTHENTICATION.md`, `docs/01-PRD/02-RIDER-PROFILE.md` |
| Feed, follow, kudos, comments, share card | `docs/24-SOCIAL/`, `docs/01-PRD/14-SOCIAL-FEED.md`, `docs/01-PRD/15-COMMENTS-KUDOS.md` |
| Landing page | `docs/01-PRD/22-LANDING-PAGE.md`, `web/docs/CODING_STANDARDS.md` |
| Admin moderation dashboard | `docs/01-PRD/21-ADMIN-MODERATION.md`, `web/docs/CODING_STANDARDS.md` |
| Location privacy / compliance | `docs/45-COMPLIANCE/03-LOCATION-DATA.md` |
| What's actually in scope right now | `docs/47-ROADMAP/01-MVP-SCOPE.md`, `TASKS/PROGRESS.md` |
| Task tracking / what to do next | `TASKS/README.md`, `TASKS/00-TASK-CONVENTIONS.md` |
| Why something was built the way it was | `MEMORY/MEMORY-INDEX.md`, `MEMORY/DECISIONS.md` |
| Domain vocabulary | `MEMORY/GLOSSARY.md` |

If a question isn't answered in `docs/`, that's a real gap — flag it to the user (and add it to `TASKS/BACKLOG.md`) rather than guessing and silently deciding.

## The MVP Scope Rule (Non-Negotiable)

**Every file in `docs/` is tagged `**Status:** MVP` or `**Status:** Post-MVP`.** Implement only what's tagged MVP. If asked to implement anything from a Post-MVP document (Moto Club, Group Ride, Safety, Route Discovery, Monetization, AI, etc.), **stop and confirm with the user first** — the document existing is not authorization to build it. See `docs/00-PRODUCT/05-NON-GOALS.md` for the explicit list of what's excluded and why.

## Mandatory Workflow for Any Task

1. Check `TASKS/PROGRESS.md` for the task's status and dependencies. Don't start a task whose dependencies aren't `DONE` (see `TASKS/00-TASK-CONVENTIONS.md` § Definition of Ready).
2. Read every document in the task's `Docs refs`.
3. Check `MEMORY/DECISIONS.md` — both the Log (decisions already made, don't re-litigate) and Decisions Pending (things you must NOT decide silently).
4. Implement, satisfying the task's own Definition of Done plus the global DoD in `TASKS/00-TASK-CONVENTIONS.md`.
5. Write a `MEMORY/records/` change record before marking the task `DONE` — this is not optional, see `MEMORY/README.md` § What Gets a Record.
6. Update `TASKS/PROGRESS.md` and the phase file checkbox in the same commit.

## Non-Negotiable Constraints

- **Location data is private by default.** A new `Ride` is always `private` until the rider explicitly publishes it (`docs/45-COMPLIANCE/03-LOCATION-DATA.md`).
- **Never build a Phase N+1 task while Phase N (Foundation) is incomplete** — see `TASKS/README.md` § The Phase Rule. Phase 1 (Tracking) and Phase 2 (Social Share) may proceed in parallel once Phase 0 is done, but neither should get ahead of documented dependencies within itself.
- **Never create database tables or code scaffolding for Post-MVP entities** (`Motorcycle`, `Club`, `Event`, `Segment`, etc.) "because they'll be needed eventually" — see `docs/07-DOMAIN/00-DOMAIN-MODEL.md` § Catatan desain for why this is deliberately avoided.
- **GPS speed/distance calculations must apply the documented filtering** (low-confidence point exclusion, GPS-jump capping at 220 km/h) — an unfiltered metric is not a minor omission, it's a wrong number shown to the rider.
- **Never log raw GPS traces, passwords, or auth tokens.**
- **All file storage goes through the `StorageDriver` interface** (`backend/docs/CODING_STANDARDS.md` §9, ADR-011) — default driver is the VM's local disk; never call `fs` or a cloud SDK directly from domain code, and store storage keys (not URLs/paths) in the database.
- **`docs/` is reference documentation, not implementation output** — don't edit it as a side effect of coding. If a requirement genuinely needs to change during implementation, that's a deliberate, separate action (update the doc, note it in a MEMORY record) — see the Deviation Protocol in `TASKS/00-TASK-CONVENTIONS.md`.

## Assumed Tech Stack (Frozen — See `MEMORY/DECISIONS.md` ADR-006, ADR-008, ADR-010, ADR-011)

| Layer | Choice |
|---|---|
| Android | Kotlin, Jetpack Compose, MVVM (native — ADR-006) |
| iOS | Swift, SwiftUI, MVVM (native — ADR-006) |
| Web (landing + admin) | Next.js, React, TypeScript, Tailwind CSS, Zustand (one app — ADR-008) |
| Backend | Node.js + TypeScript + NestJS (ADR-010, supersedes ADR-007's Express) |
| ORM | Prisma |
| Validation | Zod (via a `ZodValidationPipe`, not class-validator) |
| Database | PostgreSQL + PostGIS |
| Cache/session | Redis |
| Background jobs | BullMQ |
| Storage | Driver-agnostic `StorageDriver`; default `local` (VM disk), `s3` optional (ADR-011) |
| Auth | Custom JWT (access + refresh); admin auth is a separate flow from rider auth |

Coding-level conventions for each are in `backend/docs/CODING_STANDARDS.md`, `android/docs/CODING_STANDARDS.md`, `ios/docs/CODING_STANDARDS.md`, `web/docs/CODING_STANDARDS.md` — read the one matching your `Surface` before writing code.

## Working Conventions

- **Directory layout** (propose this if the repo is empty; keep consistent if it already exists):
  ```
  backend/   → NestJS + TypeScript API service (auth, ride, social, admin modules) — docs/CODING_STANDARDS.md
  android/   → native Android app (Kotlin, Jetpack Compose) — docs/CODING_STANDARDS.md
  ios/       → native iOS app (Swift, SwiftUI) — docs/CODING_STANDARDS.md
  web/       → Next.js: landing page + admin dashboard — docs/CODING_STANDARDS.md
  docs/      → reference documentation, amended deliberately, never as a side effect of feature work
  MEMORY/    → change records and decision log
  TASKS/     → execution plan
  ```
- **Migrations**: additive/backward-compatible by default — never a migration that breaks a running previous version mid-rollout.
- **Commits/PRs**: reference the task ID and the `docs/` sections implemented, per `TASKS/00-TASK-CONVENTIONS.md`.
- **When `docs/` and a practical constraint conflict**, stop and surface the conflict (Deviation Protocol) rather than quietly picking a different approach.

## Testing Expectations

Unit tests for pure logic (GPS filtering, metric calculations, ride state machine transitions), integration tests against a real database, manual/E2E verification for flows that are hard to automate early (live GPS recording in the field). Every documented edge case (see each task's "Edge cases to test") needs a test or an explicit manual verification note — see `TASKS/00-TASK-CONVENTIONS.md` § Global Definition of Done.

## When You're Unsure

Ask rather than assume. `docs/` is detailed specifically so implementation doesn't require guessing; if an answer isn't there, that's a genuine gap to raise — add it to `TASKS/BACKLOG.md` § Open Questions and surface it to the user, don't decide it silently.
