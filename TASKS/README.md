# TASKS/ — Execution Plan

`docs/` describes **what** to build and **why** (47 categories, each file tagged `Status: MVP` or `Status: Post-MVP`). This folder describes **what to do next, in what order, and how to know it's finished** — for the MVP scope only.

Nothing in this folder invents new product decisions. Every task points back to the `docs/` document that already decided the requirement. If a task needs a decision `docs/` doesn't contain, it is not a task — it is an entry in [`BACKLOG.md`](./BACKLOG.md) under "Open Questions," to be raised with the user.

## Files in This Folder

| File | Purpose |
|---|---|
| [`00-TASK-CONVENTIONS.md`](./00-TASK-CONVENTIONS.md) | Task ID scheme, status values, task card anatomy, global Definition of Done |
| [`PROGRESS.md`](./PROGRESS.md) | The single status board — phase-level and task-level completion at a glance |
| [`PHASE-0-FOUNDATION.md`](./PHASE-0-FOUNDATION.md) | Repo setup, tech stack freeze, CI, base schema |
| [`PHASE-1-MVP-TRACKING.md`](./PHASE-1-MVP-TRACKING.md) | Ride recording, GPS engine, ride history & analytics |
| [`PHASE-2-MVP-SOCIAL-SHARE.md`](./PHASE-2-MVP-SOCIAL-SHARE.md) | Auth, profile, feed, follow, kudos/comments, share card |
| [`PHASE-3-WEB.md`](./PHASE-3-WEB.md) | Landing page + admin moderation dashboard (Next.js) |
| [`specs/`](./specs/) | Full implementation briefs for tasks marked `Spec required: Yes` — one file per task, named `<task-id>-<slug>.md` |
| [`BACKLOG.md`](./BACKLOG.md) | Open questions, deferred items, and gaps discovered while scaffolding `docs/` |

## How to Use This Folder

1. **Before starting work**, open [`PROGRESS.md`](./PROGRESS.md) and find the lowest-numbered task in the current phase that is `TODO` and whose dependencies are all `DONE`.
2. **Read every document listed in that task's `Docs refs` row.** These are not decoration — they contain the requirement the task implements.
3. **If `Spec required: Yes`**, read the spec in [`specs/`](./specs/) in full before writing code, and resolve any "Reconciliation notes" it flags — don't implement around an unresolved conflict.
4. **Implement**, satisfying every line of the task's Definition of Done plus the inherited global DoD in [`00-TASK-CONVENTIONS.md`](./00-TASK-CONVENTIONS.md).
5. **Record the change** in [`../MEMORY/`](../MEMORY/README.md) — a change record per task, an index line, a changelog entry, and an ADR if a decision was made or deviated from `docs/`.
6. **Update `PROGRESS.md`** and tick the checkbox in the phase file.

## The Phase Rule

From `CLAUDE.md` and `docs/47-ROADMAP/00-ROADMAP.md`:

> **Never build a Phase N+1 task while Phase N is incomplete.**

Phase 0 (Foundation) gates Phase 1, Phase 2, and Phase 3. Phase 1 (Tracking), Phase 2 (Social Share), and Phase 3's landing-page tasks may run **in parallel** by different people once Phase 0 is done — they touch mostly disjoint surfaces. Phase 3's admin-dashboard tasks (`T3-04` onward) additionally need `T2-06`/`T2-09` from Phase 2, since moderation has nothing to moderate until posts and comments exist.

**There is no Phase 4 in this repo yet.** Everything past MVP (Motorcycle identity, Community, Safety, Route Discovery, Event, Monetization, etc.) is deliberately left as `docs/` placeholders with no task breakdown — see `docs/47-ROADMAP/00-ROADMAP.md`. Do not create phase files for them without an explicit decision to start that phase.

## Relationship to MEMORY/

`TASKS/` is forward-looking (what will be done). `MEMORY/` is backward-looking (what was done, and why it ended up that way). They are updated in the same commit: a task is not `DONE` until its MEMORY record exists.
