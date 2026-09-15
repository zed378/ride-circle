# <Task ID> — <Short Title>

| | |
|---|---|
| **Date** | YYYY-MM-DD |
| **Task** | `TASKS/PHASE-N-....md` § <task id> |
| **Phase** | Phase N |
| **Surface** | backend / android / ios / infra |
| **Author** | |
| **Commits / PR** | |
| **Status** | Completed / Partially completed / Reverted |

---

## What Changed

A factual summary of the change in two or three sentences. What exists now that did not before, or behaves differently than it did.

## Why

The reason this was done now, and the `docs/` documents it implements. Link them — `docs/13-GPS/07-DISTANCE-CALCULATION.md`, not "the GPS doc."

If the task exists because of something discovered during other work rather than because the roadmap said so, say that — it is the more useful information.

## How

The implementation approach, at the level of detail a future reader needs to orient themselves before opening the code. Not a line-by-line description; the diff already covers that.

Name anything non-obvious: a workaround, an unusual pattern, a place where the straightforward approach was wrong for a reason that is not visible locally.

## Files and Components Touched

| Path | Change |
|---|---|
| | |

## Decisions Made

Decisions taken during this work. Anything architectural, or any deviation from `docs/`, also gets a full ADR in `DECISIONS.md` — link it here.

| Decision | Rationale | ADR |
|---|---|---|
| | | |

## Deviations from `docs/`

Per the deviation protocol in `TASKS/00-TASK-CONVENTIONS.md`: state the conflict, what was chosen, whether the user approved it, and whether the `docs/` document should now be amended.

If there were none, write "None" — an empty section reads as an oversight.

## Tests Added

| Layer | What it covers |
|---|---|
| Unit | |
| Integration | |
| Manual / E2E | |

## Edge Cases Covered

Cross-referenced from the task's own "Edge cases to test" list.

| Edge case | Source | Test |
|---|---|---|
| | | |

## Definition of Done Verification

Both the task's own DoD and the global DoD from `TASKS/00-TASK-CONVENTIONS.md`. **If an item was waived, say which one, why, and who agreed.**

- [ ] Tests at the appropriate layer
- [ ] Every edge case has a test or explicit manual verification note
- [ ] Location data handling follows `docs/45-COMPLIANCE/03-LOCATION-DATA.md` (if applicable)
- [ ] Nothing sensitive logged
- [ ] CI green: build, tests, lint
- [ ] `TASKS/PROGRESS.md` and the phase file updated
- [ ] Task-specific DoD items (list them)

## What Did Not Work

Approaches tried and abandoned, and why. This is the section most likely to be skipped and most likely to save someone a day later.

## Follow-Ups and Open Questions

Anything left undone, discovered mid-work, or deferred. Every item here should also exist in `TASKS/BACKLOG.md` or as a task, so it has a consequence rather than only a mention.

## What to Watch

Things that could go wrong in production because of this change, what the symptom would look like, and which signal would show it first.
