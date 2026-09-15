# Memory Index

Every change record, newest first. One line each: date, task ID, title, and the hook that tells you whether this is the record you need.

Add a line here as part of writing the record — an unindexed record is a record nobody finds.

One task (`T0-01`) has reached `DONE` so far — the tech-stack freeze that made writing the platform coding standards possible. Everything else is still `TODO`.

---

## Records

| Date | Task | Record | Hook |
|---|---|---|---|
| 2026-09-15 | ADR-010, ADR-011 | [Backend to NestJS, storage driver-agnostic](./records/2026-09-15-ADR-010-011-nestjs-storage-driver.md) | Express → NestJS before any code existed; storage behind a `StorageDriver` interface with VM local disk as default (no MinIO/S3 needed); ADR-007 restored as Superseded after an earlier in-place rewrite; new task `T0-11` |
| 2026-09-15 | T3-02 | [OQ-09 resolved — product name stays RideCircle](./records/2026-09-15-OQ-09-resolved.md) | ADR-009; substitution table appended to the spec rather than editing the verbatim pasted body; `T3-02` unblocked |
| 2026-09-15 | T3-02 | [Add landing page spec](./records/2026-09-15-T3-02-landing-page-spec.md) | A precise, pasted `claude -p` brief stored as `TASKS/specs/T3-02-landing-page.md` rather than executed blind — read-through found a real product-name conflict (RIDELINE vs. RideCircle), surfaced as `BACKLOG.md` OQ-09 instead of guessed silently, even though the spec's own text says not to ask questions |
| 2026-09-15 | ADR-008 | [Add web platform (landing + admin)](./records/2026-09-15-ADR-008-web-platform.md) | One Next.js app for both, modeled on `callibrator/frontend`; surfaced a real gap (feed with no moderation path) that pulled Admin Moderation into MVP |
| 2026-09-15 | T0-01 | [Freeze the tech stack](./records/2026-09-15-T0-01-tech-stack-freeze.md) | Native Android+iOS (ADR-006) and Node.js/TypeScript/Prisma (ADR-007), decided by cloning and reading `callibrator`'s actual conventions rather than guessing; three `CODING_STANDARDS.md` written as the detail-level reference |

---

## By Phase

### Phase 0 — Foundation
- [Freeze the tech stack](./records/2026-09-15-T0-01-tech-stack-freeze.md) — `T0-01`, unblocks `T0-02` onward
- [Backend to NestJS, storage driver-agnostic](./records/2026-09-15-ADR-010-011-nestjs-storage-driver.md) — amends `T0-01`'s result; adds `T0-11`

### Phase 1 — MVP: Ride Tracking
_(no records yet)_

### Phase 2 — MVP: Social Media Share
_(no records yet)_

### Phase 3 — Web: Landing Page + Admin Dashboard
- [Add web platform (landing + admin)](./records/2026-09-15-ADR-008-web-platform.md) — scoping/ADR record, phase created but no implementation tasks started
- [Add landing page spec](./records/2026-09-15-T3-02-landing-page-spec.md) — `T3-02` set `BLOCKED` on OQ-09
- [OQ-09 resolved — product name stays RideCircle](./records/2026-09-15-OQ-09-resolved.md) — `T3-02` unblocked, ready for `T3-01` to complete first
