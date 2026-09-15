# ADR-008 — Add web platform (landing page + admin dashboard)

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Task** | New Phase 3 (`TASKS/PHASE-3-WEB.md`); extends `docs/01-PRD/` |
| **Phase** | Phase 0 → Phase 3 scoping |
| **Surface** | web / backend / docs |
| **Author** | Claude (scaffolding session) |
| **Commits / PR** | — (documentation-only session, no repo/CI exists yet) |
| **Status** | Completed |

---

## What Changed

Added a fourth platform, `web/`, to the project: one Next.js app serving the public landing page and an internal admin moderation dashboard. `docs/01-PRD/21-ADMIN-MODERATION.md` was promoted from a Post-MVP stub to a full MVP document; a new `docs/01-PRD/22-LANDING-PAGE.md` was written. `web/docs/CODING_STANDARDS.md` was written, and a new `TASKS/PHASE-3-WEB.md` (8 tasks) was added.

## Why

The user asked to add landing page and admin dashboard, and to write conventions for them. Separately, scoping the admin dashboard surfaced a real gap: MVP's Social Media Share pillar ships a public feed with no moderation path, which is an operational risk from day one of launch, not a nice-to-have — that's why `21-ADMIN-MODERATION.md` moved into MVP rather than staying deferred.

## How

- Cloned `callibrator` (the team's other project) again, this time to read `frontend/` and `docs/FRONTEND/00-FRONTEND-STANDARDS.md` — confirmed it already solves exactly this problem (one Next.js app, `app/` for public marketing + `app/dashboard/` for the authenticated console) and is documented in detail.
- Wrote `web/docs/CODING_STANDARDS.md` as a direct adaptation of that document: same envelope-unwrap discipline, same "errors are a UI state" rule, same Zustand "only for state that outlives a page" rule — reusing rules this team already paid to learn rather than reinventing them.
- Added a small new requirement to the Social Share surface (rider-side "report" action, `T3-05`) that the admin dashboard depends on but that wasn't in the original `docs/24-SOCIAL/` scope — logged as a gap in `TASKS/BACKLOG.md` rather than silently editing the existing Phase 2 documents.

## Files and Components Touched

| Path | Change |
|---|---|
| `MEMORY/DECISIONS.md` | Added ADR-008 |
| `docs/01-PRD/21-ADMIN-MODERATION.md` | Rewritten: Post-MVP stub → full MVP document |
| `docs/01-PRD/22-LANDING-PAGE.md` | Created (new, MVP) |
| `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` | Diagram and tech stack table updated to include `web/` and the admin module |
| `docs/00-PRODUCT/05-NON-GOALS.md` | Non-goal #8 reworded (previously implied choosing one mobile OS as primary, now stale given ADR-006) |
| `web/docs/CODING_STANDARDS.md` | Created |
| `TASKS/PHASE-3-WEB.md` | Created, 8 tasks |
| `TASKS/PROGRESS.md`, `TASKS/README.md`, `TASKS/00-TASK-CONVENTIONS.md`, `TASKS/BACKLOG.md` | Updated for the new phase and `web` surface |
| `CLAUDE.md`, `AGENTS.md`, `README.md` | Directory layout, tech stack table, and doc map updated |

## Decisions Made

| Decision | Rationale | ADR |
|---|---|---|
| One Next.js app for landing + admin, not two apps | `callibrator/frontend` already proves this pattern works and is documented | ADR-008 |
| Admin moderation pulled into MVP (was Post-MVP) | A public feed with no moderation path is an operational risk, not a deferrable feature | — (see `docs/01-PRD/21-ADMIN-MODERATION.md` intro) |
| Admin auth is a fully separate flow from rider auth | Prevents a rider-auth bug from ever becoming an admin-access bug | `AGENTS.md` hard rule 10 |

## Deviations from the Plan

`docs/47-ROADMAP/01-MVP-SCOPE.md` originally defined MVP as exactly two pillars (Tracking, Social Share) with everything else Post-MVP. Adding Admin Moderation to MVP is a scope change to that document, made at the user's direction when they asked to add the admin dashboard — `docs/47-ROADMAP/01-MVP-SCOPE.md` itself has **not** yet been edited to reflect this and should be, as a follow-up, so it doesn't silently drift from `docs/01-PRD/21-ADMIN-MODERATION.md`'s actual status.

## Tests Added

Not applicable — no code exists yet.

## Definition of Done Verification

- [x] `docs/` updated to reflect the new scope
- [x] `TASKS/PROGRESS.md` and phase files updated
- [x] `docs/47-ROADMAP/01-MVP-SCOPE.md` updated (done later in the same session, after initially being flagged as outstanding below)
- [ ] CI green — waived, no repository exists yet

## What Did Not Work

Nothing abandoned this session.

## Follow-Ups and Open Questions

- `docs/24-SOCIAL/03-FEED.md` and `08-RIDE-POST.md` should get a one-line pointer to the new report action (`T3-05`) next time either file is touched, per the note already in `TASKS/BACKLOG.md`.

## What to Watch

None yet — no code has been written against these decisions.
