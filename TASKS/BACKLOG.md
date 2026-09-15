# Backlog

Open questions, deferred items, and gaps discovered while scaffolding `docs/`. Items here block the task(s) that reference them — see each task's `Depends on` / status `BLOCKED`.

## Open Questions

Answer these before (or as part of) the referenced task — do not let an agent decide them silently, per `AGENTS.md` rule 8.

| ID | Question | Blocks | Notes |
|---|---|---|---|
| ~~OQ-01~~ | ~~Mobile platform~~ — **decided 2026-09-15**, ADR-006: native Android (Kotlin) + native iOS (Swift) | ~~T0-01, T0-09~~ | User specified both platforms explicitly; no cross-platform framework |
| OQ-02 | Privacy zone (blur ~200m start/finish on public rides) — in MVP or deferred? | T1-11, T1-12 | Recommended for MVP, not confirmed. See `MEMORY/DECISIONS.md` ADR-004 |
| ~~OQ-03~~ | ~~Auth: build vs. buy~~ — **decided 2026-09-15**, folded into ADR-007: custom JWT | ~~T0-01, T0-08, T2-01~~ | Team already operates JWT auth in `callibrator` |
| ~~OQ-04~~ | ~~Backend language~~ — **decided 2026-09-15**, ADR-007 (Express), superseded same day by ADR-010: Node.js + TypeScript + NestJS + Prisma | ~~T0-01, T0-04~~ | Storage made driver-agnostic, local disk default — ADR-011 |
| OQ-05 | Share card: ship 1:1 only, or also 9:16 Story variant at MVP launch? | T2-11 | `docs/24-SOCIAL/09-SHARE-CARD.md` says 1:1 is sufficient; confirm before scoping T2-11 |
| OQ-06 | Auto-pause: default on or off? Is the 3-minute/2km/h threshold right? | T1-05, T1-13 | |
| OQ-07 | Must email be verified before a rider can publish a post? | T2-01, T2-06 | |
| OQ-08 | Launch market: Indonesia only, or multi-country from day one? | (product-level, no task yet) | Affects which privacy law (UU PDP vs. GDPR) is the primary compliance target in `docs/45-COMPLIANCE/` |
| ~~OQ-09~~ | ~~Product name: RideCircle vs. RIDELINE~~ — **decided 2026-09-15**, ADR-009: RideCircle | ~~T3-02~~ | Substitution table added to `TASKS/specs/T3-02-landing-page.md` |

## Deferred (explicitly out of MVP, tracked so they aren't lost)

Everything in this list has a corresponding `docs/` folder already scaffolded at `Status: Post-MVP`. Do not create Phase 3+ task files for any of these without a deliberate decision — see `docs/47-ROADMAP/00-ROADMAP.md`.

- Motorcycle Profile & Garage (Fase 1 of the roadmap)
- Moto Club, Group Ride incl. live member tracking (Fase 2)
- Safety: emergency contact, SOS, crash detection (Fase 3)
- Route Discovery as a reusable entity, scenic/twisty routing (Fase 4)
- Event & Challenge, safety-conscious gamification (Fase 5)
- Monetization, Brand Partnership (Fase 6)
- AI features, recommendation engine (Fase 7)
- Third-party device integration (Garmin, Bluetooth sensors, wearables)

## Gaps Found While Scaffolding `docs/`

- `17-RIDER-PERFORMANCE` overlaps partly with `01-PRD/06-RIDE-ANALYTICS.md` (MVP) — the MVP doc defines the basic metrics; the full folder (personal bests, segment performance) stays Post-MVP. Worth a short cross-reference note in both files if this causes confusion during implementation.
- No explicit MVP decision on **data export** (GPX download) — mentioned as out-of-scope in `01-PRD/05-RIDE-HISTORY.md` but not tracked as an open question; low priority, added here for visibility rather than as a blocking OQ.
- **Rider-side "report" action was missing from `docs/24-SOCIAL/`** until the admin dashboard was scoped — a moderation queue is useless without a way for riders to actually report something. Added as `T3-05` in `TASKS/PHASE-3-WEB.md` rather than retroactively editing `docs/24-SOCIAL/03-FEED.md`/`08-RIDE-POST.md`; those documents should get a one-line addition referencing the report action next time they're touched, so the gap doesn't resurface for someone reading `docs/` in isolation.
