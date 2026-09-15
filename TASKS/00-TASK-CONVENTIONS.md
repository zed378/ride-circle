# 00 — Task Conventions

How every task in this folder is written, tracked, and closed. Read once; then it applies to all phases.

## Task IDs

```
T<phase>-<nn>[.<sub>]
```

| Example | Meaning |
|---|---|
| `T0-04` | Phase 0, task 4 |
| `T1-12.3` | Phase 1, task 12, sub-task 3 |
| `T2-02` | Phase 2, task 2 |

IDs are **permanent and never reused**. If a task is dropped, its ID is retired with a `DROPPED` status and a one-line reason — a gap in the numbering is a lost trail.

Task IDs are the join key across the repo: they appear in branch names (`feat/T1-04-ride-recording-state-machine`), commit messages, PR titles, MEMORY change records, and `PROGRESS.md`.

## Status Values

| Status | Meaning |
|---|---|
| `TODO` | Not started. Dependencies may or may not be met. |
| `BLOCKED` | Cannot start — a dependency is incomplete or an open question in `BACKLOG.md` must be answered first. The blocker is always named. |
| `WIP` | Implementation in progress. |
| `REVIEW` | Implementation complete, under review / awaiting test results. |
| `DONE` | Every line of the task's DoD and the global DoD below is satisfied, **and** a MEMORY record exists. |
| `DROPPED` | Deliberately abandoned. Requires a one-line reason and a MEMORY decision record. |

## Task Card Anatomy

Every task in a phase file uses this structure:

```
### T1-04 — Ride recording state machine (start/pause/resume/stop)

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-02, T1-03 |
| **Docs refs** | docs/16-RIDE/00-RIDE-LIFECYCLE.md, docs/13-GPS/09-PAUSE-RESUME.md |
| **Spec required** | No |
| **Surface** | backend / android / ios / web |

**Goal** — one sentence stating the observable outcome.

**Steps** — the ordered implementation sequence.

**Definition of Done** — checkable, objective conditions.

**Edge cases to test** — cross-referenced from the docs above.
```

Field meanings:

- **Depends on** — task IDs that must be `DONE` first. Empty means it can start as soon as the phase starts.
- **Docs refs** — the authoritative documents in `docs/`. If implementation and these documents disagree, the documents win unless the deviation is escalated (see below).
- **Spec required** — `Yes` when a task is large, visually/behaviorally precise, or detailed enough that undocumented judgment calls would materially change the outcome (a full landing page brief, a complex multi-screen flow). The spec lives in `TASKS/specs/<task-id>-<slug>.md`, written (or received from the user, as with `TASKS/specs/T3-02-landing-page.md`) *before* the task moves to `WIP`. Default `No` — only mark `Yes` when the task card's own Goal/Steps/DoD genuinely wouldn't be enough to implement consistently.
- **Surface** — `backend`, `android`, `ios`, `web`, `infra`, or a combination. A task listing both `android` and `ios` means the feature must be implemented on **both** native codebases before the task is `DONE` — it is one task card, not an implicit license to ship one platform and call it done. If the two platforms diverge enough to need separately-tracked work (one ships first, or the implementations differ substantially), split into `T<id>` and `T<id>B` as was done for `T0-09`/`T0-09B`.

## Global Definition of Done

Inherited by **every** task. A task's own DoD is *in addition* to this, never instead of it.

1. **Tests exist at the right layer** — unit for pure logic (metric calculations, state machine transitions), integration against a real database, manual/E2E for user-visible flows that are hard to automate early (GPS recording in the field).
2. **Every edge case listed on the task has a test or an explicit manual verification note**, per the relevant `docs/13-GPS/`, `docs/16-RIDE/`, or `docs/24-SOCIAL/` document. A tracking feature with no GPS-jump/pause edge case test is not done, regardless of how well the happy path works.
3. **Location data handling follows `docs/45-COMPLIANCE/03-LOCATION-DATA.md`** for anything touching GPS points — default-private visibility, no third-party sharing, retention rule respected.
4. **Nothing sensitive is logged** — no raw GPS traces, no auth tokens, no passwords in application logs.
5. **CI is green**: build, tests, lint.
6. **A MEMORY change record exists** (`MEMORY/records/`), the index and changelog are updated, and any architectural decision or deviation from `docs/` has an ADR in `MEMORY/DECISIONS.md`.
7. **`PROGRESS.md` and the phase file checkbox are updated** in the same commit as the work.

## Definition of Ready

A task should not move to `WIP` unless:

- All `Depends on` tasks are `DONE`.
- Every document in `Docs refs` has actually been read for this task (not remembered from a previous one).
- If `Spec required: Yes`, the spec exists in `TASKS/specs/` and its "Reconciliation notes" (if any) are resolved, not just acknowledged.
- No unanswered `BACKLOG.md` open question blocks it.

## Deviation Protocol

`AGENTS.md` rule 6 makes `docs/` reference documentation, not implementation output. So when reality and the docs conflict — a library can't do what `docs/13-GPS/00-GPS-ARCHITECTURE.md` assumed, a metric definition doesn't survive contact with real GPS data, a share card format doesn't fit a platform's share sheet:

1. **Stop.** Do not silently pick a different approach.
2. Write an ADR in `MEMORY/DECISIONS.md` describing the conflict, the options, and the recommendation.
3. Raise it with the user.
4. Only after a decision: implement, and note in the ADR whether the `docs/` document itself should be amended (a separate, deliberate action).

A deviation that is documented is a decision. A deviation that is not documented is a bug that nobody has found yet.

## Estimation

Tasks carry **relative size**, not calendar dates, because staffing is unknown:

| Size | Rough meaning |
|---|---|
| `S` | Under half a day for someone familiar with the area |
| `M` | One to two days |
| `L` | Several days; consider splitting into sub-tasks |
| `XL` | Too large — must be split before it enters `WIP` |

Sizes are recorded in `PROGRESS.md`, not repeated on every card.

## Branch, Commit, PR

- Branch: `feat/T1-04-ride-state-machine`, `fix/T1-09-max-speed-filter`, `chore/T0-03-ci-pipeline`.
- Commit message subject: `T1-04: implement ride recording state machine`.
- Commit trailer: reference the `docs/` sections implemented.
- PR body must state: the task ID, the `docs/` sections implemented, which test layers were added and run, and any deviation (with its ADR link).
