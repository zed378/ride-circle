# RideCircle — Documentation & Project Scaffold

A platform for recording, discovering, riding, sharing, and managing motorcycle rides and rider communities — designed motorcycle-native, not "Strava + a motorcycle icon".

> **Current MVP = Ride Tracking + Social Media Share.** Read `docs/47-ROADMAP/01-MVP-SCOPE.md` before reading anything else in this repo.

## Repository structure

Follows the same `TASKS/`+`MEMORY/`+`CLAUDE.md`+`AGENTS.md` convention as the author's [`zed-auth`](https://github.com/zed378/zed-auth) project — `docs/` = reference (what to build), `TASKS/` = execution plan (what's next, how it's judged done), `MEMORY/` = change & decision log (what happened, and why).

```
ridecircle-docs/
├── docs/                          48 product documentation category folders (00-47)
├── backend/
│   └── docs/CODING_STANDARDS.md   NestJS + TypeScript + Prisma, driver-agnostic storage (ADR-010, ADR-011)
├── android/
│   └── docs/CODING_STANDARDS.md   Kotlin + Jetpack Compose + MVVM (ADR-006)
├── ios/
│   └── docs/CODING_STANDARDS.md   Swift + SwiftUI + MVVM (ADR-006)
├── web/
│   └── docs/CODING_STANDARDS.md   Next.js — landing page + admin dashboard (ADR-008)
├── MEMORY/
│   ├── README.md                  how to use this folder
│   ├── MEMORY-INDEX.md             one line per change record, newest first
│   ├── DECISIONS.md               ADR log — all architecture decisions
│   ├── CHANGELOG.md               chronological summary of changes
│   ├── GLOSSARY.md                RideCircle domain terms
│   ├── ARCHITECTURE-NOTES.md      informal technical notes, not yet mature enough for an ADR
│   ├── records/                   one file per task that reached DONE
│   └── templates/                 change record & phase summary templates
├── TASKS/
│   ├── README.md                  how to use this folder
│   ├── 00-TASK-CONVENTIONS.md     task ID scheme, statuses, Definition of Done
│   ├── PROGRESS.md                status board — one place to see progress
│   ├── PHASE-0-FOUNDATION.md      12 tasks: repo setup, tech stack, DB schema, storage
│   ├── PHASE-1-MVP-TRACKING.md    14 tasks: GPS, ride recording, history
│   ├── PHASE-2-MVP-SOCIAL-SHARE.md 12 tasks: auth, feed, kudos, share card
│   ├── PHASE-3-WEB.md             8 tasks: landing page + admin moderation dashboard
│   ├── specs/T3-02-landing-page.md  full design brief (pasted by the user) — T3-02 BLOCKED, see OQ-09
│   └── BACKLOG.md                 open questions & deferred items
├── CLAUDE.md                      working instructions for Claude Code
├── AGENTS.md                      equivalent instructions for other AI coding agents
└── README.md                      this file
```

## Start here

Recommended reading order for anyone (human or AI agent) joining this project:

1. `docs/00-PRODUCT/00-PRODUCT-VISION.md` — long-term vision
2. `docs/47-ROADMAP/01-MVP-SCOPE.md` — **the scope boundary currently in force**
3. `docs/00-PRODUCT/05-NON-GOALS.md` — what is deliberately NOT being built yet
4. `docs/07-DOMAIN/00-DOMAIN-MODEL.md` — core data model
5. `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` — architecture & tech stack (**frozen** — native Android/Kotlin, native iOS/Swift, Next.js web, NestJS/TypeScript backend with driver-agnostic storage (local disk by default), see `MEMORY/DECISIONS.md` ADR-006, ADR-008, ADR-010, ADR-011)
6. `backend/docs/CODING_STANDARDS.md`, `android/docs/CODING_STANDARDS.md`, `ios/docs/CODING_STANDARDS.md`, `web/docs/CODING_STANDARDS.md` — per-platform coding conventions
7. `TASKS/PROGRESS.md` — status board, start work from here
8. `MEMORY/DECISIONS.md` § Decisions Pending — things that still need deciding before some tasks can proceed

## Document status

Every file in `docs/` carries a `**Status:** MVP` or `**Status:** Post-MVP` marker at the top.

- **MVP** (57 files tagged) — 31 of them are fully written (requirements, data schema, edge cases): Authentication, Rider Profile, Ride Recording/History/Analytics, GPS engine (sampling/speed/distance/pause-resume), Ride lifecycle & sharing, Social feed/graph, Comments & Kudos, Share Card, Location compliance, Roadmap. The rest (26 files, all in the `13-GPS`, `16-RIDE`, and `24-SOCIAL` folders) are tagged MVP because their folder belongs to the Tracking/Social Share pillars, but their content is still a template stub — they need detailing before a sprint starts.
- **Post-MVP** (358 files) — placeholders/scaffolding that point at the long-term architectural direction (Motorcycle identity, Moto Club, Group Ride, Safety, Route Discovery, Event, Challenge, Gamification, Monetization, Brand Partnership, AI, etc.). **Not to be implemented yet** — see `docs/47-ROADMAP/00-ROADMAP.md` for the order of later phases.

## Index of the 47 documentation categories

```
00-PRODUCT            01-PRD                02-BUSINESS           03-MARKET
04-USER-RESEARCH      05-UX                 06-UI                 07-DOMAIN
08-ARCHITECTURE       09-MOBILE             10-BACKEND            11-API
12-DATA               13-GPS                14-MAP                15-ROUTE
16-RIDE               17-RIDER-PERFORMANCE  18-MOTORCYCLE         19-COMMUNITY
20-GROUP-RIDE         21-EVENT              22-CHALLENGE          23-SAFETY
24-SOCIAL             25-MESSAGING          26-NOTIFICATION       27-GAMIFICATION
28-MONETIZATION       29-BRAND-PARTNERSHIP  30-PRIVACY            31-SECURITY
32-MODERATION         33-ANTI-ABUSE         34-ANALYTICS          35-SEARCH
36-RECOMMENDATION     37-AI                 38-INTEGRATION        39-DEVELOPER
40-OBSERVABILITY      41-PERFORMANCE        42-SCALABILITY        43-DEVOPS
44-TESTING            45-COMPLIANCE         46-RELEASE            47-ROADMAP
```

## Current execution status

**1 / 46 tasks done.** The tech stack is frozen (`T0-01`, ADR-006 + ADR-008 + ADR-010 + ADR-011); `docs/` and the coding standards for all four platforms (backend, Android, iOS, web) are complete as scaffolding; no application code has been written yet. See `TASKS/PROGRESS.md` for per-task detail and `MEMORY/CHANGELOG.md` for a history summary.

## For AI coding agents

Read `CLAUDE.md` (if using Claude Code) or `AGENTS.md` (other agents) before starting work in this repo. The core rules are the same: **only work on tasks derived from MVP-status documents, follow `TASKS/00-TASK-CONVENTIONS.md`, write a MEMORY record before marking a task DONE, and confirm with the user before touching anything Post-MVP or any item in `TASKS/BACKLOG.md` / `MEMORY/DECISIONS.md` § Decisions Pending.**

---

*This documentation was generated from a brief recommending a documentation structure for a motorcycle-native product, narrowed to the MVP scope (Ride Tracking + Social Media Share) per the product decision. The `TASKS/`/`MEMORY/`/`CLAUDE.md`/`AGENTS.md` structure follows the conventions of the author's `zed-auth` repo.*
