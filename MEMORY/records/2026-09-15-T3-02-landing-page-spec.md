# Add landing page spec (T3-02 / T3-03)

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Task** | `TASKS/PHASE-3-WEB.md` § T3-02, T3-03 |
| **Phase** | Phase 3 |
| **Surface** | web / docs |
| **Author** | Claude (scaffolding session) |
| **Commits / PR** | — (documentation-only session, no repo/CI exists yet) |
| **Status** | Completed (spec intake) — implementation not started, T3-02 `BLOCKED` |

---

## What Changed

The user pasted a full `claude -p` execution prompt — a very detailed landing page design/implementation brief (copy, exact hex colors, typography scale, 16-section page architecture, motion timings, image sourcing policy, component list, acceptance criteria). It was stored as `TASKS/specs/T3-02-landing-page.md` rather than executed directly, following the `Spec required` pattern the task conventions already supported implicitly but hadn't formally documented until now. `TASKS/00-TASK-CONVENTIONS.md` gained a `Spec required` field on the task card template. `docs/ASSETS.md` was scaffolded (empty template) since the spec requires it. `T3-02` was set to `BLOCKED` on a real, unresolved conflict found while reading the spec: it names the product "RIDELINE" throughout, while every other document in this repo calls it "RideCircle."

## Why

Per `TASKS/README.md`'s existing rule, "nothing in this folder invents new architecture" — a large, precise, standalone brief pasted into chat is exactly the kind of input that needs to become a durable repo artifact (so a future agent picks it up correctly) rather than being executed once from chat history and then lost. The `Spec required` mechanism from the reference repos (`zed-auth`, `callibrator` both have a `specs`/`TASKS/specs` convention) was the right existing shape for this — it just hadn't been needed yet in this project until now.

## How

- Extracted the prompt content from its outer `claude -p "$(cat <<'PROMPT' ... PROMPT)"` shell-invocation wrapper (that wrapper is how the user would run it directly against a live repo; it's not part of the specification itself).
- Converted the spec's `====`-delimited ASCII section dividers into markdown `##` headers programmatically (regex, not manual retyping) to avoid transcription risk on a ~1700-line document — verified section count (50) matches before/after.
- Did **not** alter any wording, copy, hex value, or requirement inside the spec — the whole point of a spec this precise is that it's binding, not source material to paraphrase.
- Added a "Reconciliation notes" section explaining how this standalone brief relates to the rest of the repo (it doesn't reference `docs/01-PRD/22-LANDING-PAGE.md` or `web/docs/CODING_STANDARDS.md` at all, since it was authored outside this planning system) and flagging the RIDELINE/RideCircle conflict explicitly rather than silently resolving it.
- Read the spec's own instruction to the *executing* agent ("do not ask clarification questions... do not create an Open Questions section") and concluded it does not apply to *this* step — that instruction governs an agent that has been told to execute the build; nothing in the user's message to me said to execute the landing page right now, only to "insert into planning and create the document." A real, repo-wide naming inconsistency is exactly the category of thing `AGENTS.md` rule 9 says not to decide silently, regardless of what a different, narrower prompt says about its own execution.

## Files and Components Touched

| Path | Change |
|---|---|
| `TASKS/specs/T3-02-landing-page.md` | Created — full spec, reformatted, with reconciliation notes |
| `TASKS/00-TASK-CONVENTIONS.md` | Added `Spec required` field to task card template, Definition of Ready |
| `TASKS/PHASE-3-WEB.md` | `T3-02` rewritten: `BLOCKED`, spec reference, DoD expanded to point at the spec's own §47 checklist; `T3-03` updated to reference spec §42/§35 |
| `TASKS/PROGRESS.md` | `T3-02` status updated to `BLOCKED (OQ-09)` |
| `TASKS/README.md` | `specs/` added to file listing and "How to Use This Folder" steps |
| `TASKS/BACKLOG.md` | `OQ-09` added (product name conflict) |
| `docs/01-PRD/22-LANDING-PAGE.md` | Linked to the new spec, with the same conflict warning |
| `docs/ASSETS.md` | Created — empty template matching spec §24's required columns |

## Decisions Made

| Decision | Rationale | ADR |
|---|---|---|
| Store the pasted brief as a spec artifact rather than executing it immediately | A brief this detailed is meant to be implemented carefully against a real repo state (existing components, existing Tailwind config), not run blind from a single chat turn; it also needs the naming conflict resolved first | — (process decision, not architectural — no ADR) |
| Block `T3-02` on the naming conflict rather than picking one name | Renaming a product (or not) has consequences (App Store listing, domain, existing docs, brand assets already designed in this conversation) far beyond this one task — not Claude's call to make unilaterally | — |

## Deviations from the Plan

None in the sense of contradicting `docs/` — this is new spec intake, not implementation. The one thing worth naming: the spec's own §6 "Page Structure" and content are self-consistent with `docs/01-PRD/22-LANDING-PAGE.md`'s MVP scope (no blog, no dynamic waitlist, etc.), so no scope deviation was found — only the naming conflict.

## Tests Added

Not applicable — no code exists yet; this is spec intake.

## Definition of Done Verification

- [x] Spec stored in `TASKS/specs/`, referenced from the task card
- [x] Conflict found during read-through surfaced explicitly (`BACKLOG.md` OQ-09), not resolved silently
- [x] `TASKS/PROGRESS.md` and the phase file updated in this same work session
- [ ] CI green — not applicable, no repository exists yet

## What Did Not Work

Nothing abandoned. One near-miss worth recording: the spec's §50 "Execution Mode" and its repeated "do not ask questions / do not create an Open Questions section" instructions are addressed to whatever agent eventually *builds* the page from this spec — it would have been a mistake to read those instructions as applying to *this* intake step and silently pick RIDELINE or RideCircle to comply with a "don't ask" instruction that wasn't actually about this decision.

## Follow-Ups and Open Questions

- `TASKS/BACKLOG.md` OQ-09 blocks `T3-02` until answered.
- Once OQ-09 is answered, if the resolution is "keep RideCircle," `TASKS/specs/T3-02-landing-page.md`'s verbatim section should get a companion note (not a rewrite — the spec should stay historically accurate to what was pasted) listing every literal "RIDELINE" occurrence that needs substituting during implementation, so the substitution isn't done ad hoc while coding.

## What to Watch

None yet — no code has been written against this spec.
