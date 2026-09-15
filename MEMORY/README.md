# MEMORY/ — Change Record and Decision Log

`TASKS/` is what will be done. `MEMORY/` is what **was** done, and why it ended up that way.

This folder exists because `docs/` describes the intended system, and the code describes the current system — but neither explains how one became the other. Six months from now, the question "why does `max_speed_kmh` cap at 220 km/h and not 200?" is answerable from here and nowhere else. The code shows the cap; only the record shows what it cost to get there.

---

## Structure

| Path | Purpose |
|---|---|
| [`MEMORY-INDEX.md`](./MEMORY-INDEX.md) | One line per record, newest first. The entry point. |
| [`CHANGELOG.md`](./CHANGELOG.md) | Chronological summary of what changed, at a coarser grain than the records. |
| [`DECISIONS.md`](./DECISIONS.md) | Architecture Decision Records — every choice `docs/` left open, and every deviation from it. |
| [`records/`](./records/) | One file per completed task: what changed, why, and what to watch. |
| [`templates/`](./templates/) | The change record and phase summary templates. |
| [`GLOSSARY.md`](./GLOSSARY.md) | Domain terms specific to RideCircle — not part of the base convention, added because motorcycle-domain vocabulary isn't obvious from general knowledge. |
| [`ARCHITECTURE-NOTES.md`](./ARCHITECTURE-NOTES.md) | Informal technical notes not yet mature enough for a `docs/08-ARCHITECTURE/` file or a `DECISIONS.md` ADR. |

---

## What Gets a Record

**Every task that reaches `DONE`.** That is global Definition of Done item 6 in `TASKS/00-TASK-CONVENTIONS.md`, and it is not negotiable — a task without a record is not done, however finished the code looks.

Also recorded:

- **Any deviation from `docs/`** — as an ADR, per the deviation protocol in `TASKS/00-TASK-CONVENTIONS.md`. A documented deviation is a decision; an undocumented one is a bug nobody has found yet.
- **Any decision `docs/` deliberately left open** — tech stack choices, the polyline library, GPS filtering thresholds, share card rendering approach.
- **Phase completions** — a summary of what shipped, what deviated, what was deferred, and what to watch.
- **Product-shaping events with lasting consequence** — a scope change, a privacy/compliance decision, a significant bug found in the field.

## What Does Not Get a Record

- Work in progress. Records describe completed changes.
- Anything the git history already tells you accurately. A record explains *why*, not *what changed on which line*.
- Restating a `docs/` document. Link to it instead.

---

## Writing a Record

1. Copy [`templates/CHANGE-RECORD-TEMPLATE.md`](./templates/CHANGE-RECORD-TEMPLATE.md).
2. Name it `records/YYYY-MM-DD-<task-id>-<slug>.md`.
3. Fill in every section. "Not applicable" is a valid answer; a blank section is not.
4. Add a one-line pointer to [`MEMORY-INDEX.md`](./MEMORY-INDEX.md) at the top of the list.
5. Add a `CHANGELOG.md` entry if the change is user-visible or operationally significant.
6. Add an ADR to [`DECISIONS.md`](./DECISIONS.md) if a decision was made or `docs/` was deviated from.
7. Commit all of it **with the code**, not afterward. A record written a week later is a reconstruction, and reconstructions quietly omit the parts that were confusing at the time — which are exactly the parts worth having.

## Writing an ADR

Use the format in `DECISIONS.md`. The two sections that matter most are the ones easiest to skip:

- **Alternatives considered** — the whole value of an ADR is that a future reader can tell whether their new idea was already evaluated and rejected, or genuinely never considered.
- **Consequences** — including the bad ones. An ADR that lists only benefits is marketing, and it will not be trusted when someone needs to decide whether to revisit the choice.

---

## Honesty Rules

- **Record what happened, not what was supposed to happen.** If a test was skipped, say so.
- **Record failures.** An approach abandoned after a day, a metric that didn't match real GPS data, a migration rolled back — these are the highest-value records in the folder, because they stop the same ground being covered twice.
- **Do not retroactively edit a record to look better.** Add a follow-up record instead.
- **Record open questions found during the work**, and add them to `TASKS/BACKLOG.md` so they have a consequence rather than only a mention.

---

## Relationship to Other Folders

| Folder | Direction | Nature |
|---|---|---|
| `docs/` | Reference | What was decided before building, per file (`Status: MVP` / `Status: Post-MVP`). Reference-only (`AGENTS.md` rule 6). |
| `TASKS/` | Forward | What will be built, in what order, and how it will be judged done. |
| `MEMORY/` | Backward | What was built, what it cost, and what to watch. |

A `docs/` document changing is itself an event worth a MEMORY record — it means reality taught the plan something.
