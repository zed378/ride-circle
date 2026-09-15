# Phase 0 — Foundation

Gate to enter: none — this is the first phase. Gate to exit: all tasks below `DONE`.

Nothing in Phase 1 or Phase 2 should start until the tech stack is frozen (`T0-01`) and the base schema exists (`T0-07`) — both phases build directly on them.

---

### T0-01 — Confirm and freeze the tech stack

| | |
|---|---|
| **Status** | **DONE** — see `MEMORY/DECISIONS.md` ADR-006 (mobile), ADR-007 (backend, framework superseded by ADR-010), ADR-011 (storage) |
| **Depends on** | — |
| **Docs refs** | `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` |
| **Surface** | infra |

**Goal** — every open tech-stack question in `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` is answered and recorded as an ADR, not left as "usulan."

**Result** — Android (Kotlin/Compose) + iOS (Swift/SwiftUI), both native (ADR-006). Backend: Node.js + TypeScript + Prisma + Zod + PostgreSQL/PostGIS + Redis + BullMQ + custom JWT (ADR-007), on **NestJS** rather than the originally chosen Express (ADR-010, changed same day before any code existed). Storage is driver-agnostic with the VM's local disk as the default driver (ADR-011). `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` updated to reflect the frozen choice.

**Definition of Done**
- [x] Mobile platform decision recorded (ADR-006)
- [x] Backend language/framework decision recorded (ADR-007)
- [x] Auth build-vs-buy decision recorded (folded into ADR-007)
- [x] `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` updated

**Note** — per the global DoD (`00-TASK-CONVENTIONS.md`), a task isn't truly `DONE` without a `MEMORY/records/` change record. One should be added (`records/2026-09-15-T0-01-tech-stack-freeze.md`) before this checkbox is trusted in `PROGRESS.md` — flagged here rather than silently skipped.

---

### T0-02 — Initialize repository structure

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-01 |
| **Docs refs** | `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` |
| **Surface** | infra |

**Goal** — a repo skeleton exists matching the frozen architecture (`backend/`, `android/`, `ios/`), with `docs/`, `MEMORY/`, `TASKS/`, `CLAUDE.md`, `AGENTS.md` already in place from this scaffold.

**Definition of Done**
- [ ] `backend/` directory created with the NestJS/TypeScript standard layout (see `backend/docs/CODING_STANDARDS.md` §1)
- [ ] `android/` directory created with a standard Gradle/Kotlin project layout (see `android/docs/CODING_STANDARDS.md`)
- [ ] `ios/` directory created with a standard Xcode/Swift project layout (see `ios/docs/CODING_STANDARDS.md`)
- [ ] Root `README.md` updated with real setup instructions (replacing any placeholder)

---

### T0-03 — Git conventions, branch strategy, CI skeleton

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-02 |
| **Docs refs** | `TASKS/00-TASK-CONVENTIONS.md` § Branch, Commit, PR |
| **Surface** | infra |

**Goal** — CI runs on every push/PR (build + lint at minimum; tests once T0-04+ exist).

**Definition of Done**
- [ ] Branch naming enforced/documented per `00-TASK-CONVENTIONS.md`
- [ ] PR template references task ID and `docs/` sections implemented
- [ ] CI pipeline defined (build + lint), green on an empty/skeleton commit

---

### T0-04 — Backend service skeleton

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-02 |
| **Docs refs** | `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` |
| **Surface** | backend |

**Goal** — a running NestJS backend with a health-check endpoint, following the monolith-with-modules shape from the architecture doc (auth, ride, social as separate Nest modules, one deployable).

**Definition of Done**
- [ ] `GET /health` returns 200 (marked `@Public()`)
- [ ] Module boundaries (auth/ride/social) exist as separate Nest modules even though one service — matches `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` diagram
- [ ] Global `ResponseEnvelopeInterceptor`, `AllExceptionsFilter`, and Zod-validated `ConfigModule` wired (`backend/docs/CODING_STANDARDS.md` §4, §5, §13)
- [ ] Vitest configured with `unplugin-swc`; one `@nestjs/testing` test and one Supertest e2e test pass

---

### T0-05 — Local dev environment

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-04 |
| **Docs refs** | `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md`, `MEMORY/ARCHITECTURE-NOTES.md` |
| **Surface** | infra |

**Goal** — `docker-compose up` gives a working local stack: backend, PostgreSQL with PostGIS extension enabled, Redis, and a named volume for the `local` storage driver (ADR-011 — no MinIO/object-storage container needed).

**Definition of Done**
- [ ] `docker-compose.yml` starts backend + Postgres(PostGIS) + Redis
- [ ] Storage volume mounted at `STORAGE_LOCAL_ROOT`; data survives `docker-compose down` / `up`
- [ ] PostGIS extension confirmed enabled (per `MEMORY/ARCHITECTURE-NOTES.md` — enabled from day one even though unused by MVP queries)

---

### T0-06 — Migration tooling and baseline migration

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-05 |
| **Docs refs** | `docs/07-DOMAIN/00-DOMAIN-MODEL.md` |
| **Surface** | backend |

**Definition of Done**
- [ ] Migration tool chosen and wired into CI
- [ ] Baseline (empty) migration runs cleanly against a fresh database

---

### T0-07 — Core MVP schema

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-06 |
| **Docs refs** | `docs/07-DOMAIN/01-RIDER.md`, `docs/07-DOMAIN/03-RIDE.md`, `docs/07-DOMAIN/15-SOCIAL-GRAPH.md` |
| **Surface** | backend |

**Goal** — every table listed in the three domain documents above exists, matching column types and constraints exactly (including the `UNIQUE`/`CHECK` constraints called out in `07-DOMAIN/15-SOCIAL-GRAPH.md`).

**Definition of Done**
- [ ] Tables: `Rider`, `Ride`, `RidePauseEvent`, `Track`, `Follow`, `Post`, `Kudos`, `Comment`
- [ ] All constraints from the domain docs present (unique email/username, self-follow CHECK, unique ride↔post, unique kudos per rider/post)
- [ ] **No tables created for Post-MVP entities** (`Motorcycle`, `Club`, `Event`, `Segment`, etc.) — per `docs/07-DOMAIN/00-DOMAIN-MODEL.md` § Catatan desain

**Edge cases to test**
- [ ] Self-follow insert rejected at DB level
- [ ] Duplicate kudos (same rider, same post) rejected at DB level

---

### T0-08 — Auth scaffolding

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-07 |
| **Docs refs** | `docs/01-PRD/01-AUTHENTICATION.md` |
| **Surface** | backend |

**Goal** — JWT issuing/verification and the global `AuthGuard` exist and protect every endpoint built in Phase 1/2 by default, even before login itself is implemented (`T2-01`). See `backend/docs/CODING_STANDARDS.md` §8.

**Definition of Done**
- [ ] Access/refresh token issuing function
- [ ] Global `AuthGuard` rejects requests with missing/invalid/expired access token; `@Public()` opts a route out
- [ ] A route with no auth decorator is protected (test: fails closed)
- [ ] Password hashing utility (argon2) wired in, unused until `T2-01`

---

### T0-11 — Storage module (driver-agnostic) + local disk driver

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-04 |
| **Docs refs** | `backend/docs/CODING_STANDARDS.md` §9, `MEMORY/DECISIONS.md` ADR-011, `docs/45-COMPLIANCE/03-LOCATION-DATA.md` |
| **Surface** | backend |

**Goal** — every later task that stores files (`T1-06` raw points, `T1-12` purge, share card / map thumbnails) writes through one `StorageDriver` interface, with the VM's local disk as the default driver and no domain code aware of which driver is active.

**Definition of Done**
- [ ] `StorageDriver` interface + `STORAGE_DRIVER` injection token; `StorageModule` selects the driver from `STORAGE_DRIVER` (default `local`)
- [ ] `storage-keys.ts` is the only place keys are built; `private/` vs `public/` prefix enforced
- [ ] `LocalStorageDriver`: root from `STORAGE_LOCAL_ROOT`, created on boot, boot fails if not writable; atomic writes (temp file + rename)
- [ ] `PublicFilesController` serves only `public/*` keys at `/files/public/*` with `Content-Type` and cache headers; 404 when the active driver isn't `local`
- [ ] Storage env vars added to the Zod env schema (driver-specific vars as a discriminated union)
- [ ] Shared storage contract test suite written and passing for `local` — ready to run unchanged against a future `s3` driver
- [ ] **No `s3` driver built in this task** (ADR-011: built when a deployment needs it)

**Edge cases to test**
- [ ] Path traversal (`../`, absolute path, encoded `%2e%2e`) rejected before touching the filesystem
- [ ] `GET /files/public/...` cannot reach any `private/` object
- [ ] `publicUrl()` throws for a `private/` key
- [ ] `delete()` on a missing key succeeds (idempotent purge retries)
- [ ] Concurrent overwrite of the same key never leaves a partial file readable

---

### T0-09 — Android app skeleton

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-01, T0-02 |
| **Docs refs** | `android/docs/CODING_STANDARDS.md` |
| **Surface** | android |

**Definition of Done**
- [ ] App builds and runs (Kotlin, Jetpack Compose)
- [ ] Navigation shell exists with placeholder screens for: Record, History, Feed, Profile
- [ ] Project structure matches `android/docs/CODING_STANDARDS.md`

---

### T0-09B — iOS app skeleton

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-01, T0-02 |
| **Docs refs** | `ios/docs/CODING_STANDARDS.md` |
| **Surface** | ios |

**Definition of Done**
- [ ] App builds and runs (Swift, SwiftUI)
- [ ] Navigation shell exists with placeholder screens for: Record, History, Feed, Profile
- [ ] Project structure matches `ios/docs/CODING_STANDARDS.md`

---

### T0-10 — CI: full pipeline

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-07, T0-09, T0-09B |
| **Docs refs** | `TASKS/00-TASK-CONVENTIONS.md` § Global Definition of Done |
| **Surface** | infra |

**Definition of Done**
- [ ] Backend: build, test, lint run on every push
- [ ] Android: build, test, lint run on every push
- [ ] iOS: build, test run on every push
- [ ] All three required to pass before merge
