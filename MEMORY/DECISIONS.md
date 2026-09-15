# Decision Log (ADRs)

Every architectural decision `docs/` left open, and every deviation from what `docs/` decided.

**When to write one**: a decision `docs/` does not contain; a deviation from `docs/` (mandatory, per the deviation protocol in `TASKS/00-TASK-CONVENTIONS.md`); a choice that will be questioned later; or a decision **not** to build something.

**When not to**: an implementation detail that is obvious from the code and would not be questioned.

## Format

```
## ADR-NNN — <Title>

| | |
|---|---|
| **Date** | YYYY-MM-DD |
| **Status** | Proposed / Accepted / Superseded by ADR-NNN / Rejected |
| **Task** | <task id or —> |
| **Deciders** | |

**Context** — the situation forcing a choice, and the constraints on it.

**Decision** — what was chosen, stated plainly.

**Alternatives considered** — each option, and the specific reason it was not chosen.

**Consequences** — what this makes easier, what it makes harder, and what it forecloses. Include the drawbacks.

**Plan impact** — none, or: which `docs/` document should be amended, and whether it has been.
```

Numbers are sequential and permanent. A superseded ADR stays in place with its status updated and a pointer forward.

---

## Decisions Pending

Decisions `TASKS/` has identified as needing an ADR, listed here so they are not discovered late. Each moves into the log below when made. Full context for each is in `TASKS/BACKLOG.md` § Open Questions.

| Task | Decision needed | Why it matters |
|---|---|---|
| ~~T0-01~~ | ~~Mobile platform (OQ-01)~~ — **decided 2026-09-15**, ADR-006: native Android (Kotlin) + native iOS (Swift), no cross-platform framework | User specified native Android+iOS explicitly when requesting coding standards |
| ~~T0-01, T0-08~~ | ~~Auth build vs. buy (OQ-03)~~ — **decided 2026-09-15**, folded into ADR-007: custom JWT, not a third-party auth provider | Keeps the auth flow inside the same service as ride/social data, avoids a second vendor for an MVP-scale user base |
| ~~T0-01, T0-04~~ | ~~Backend language/framework (OQ-04)~~ — **decided 2026-09-15**, ADR-007 (Express), superseded same day by ADR-010: Node.js + TypeScript + NestJS + Prisma + PostgreSQL/PostGIS + Redis | User changed the framework to NestJS before any backend code existed; storage made driver-agnostic in ADR-011 |
| T1-11, T1-12 | Privacy zone at MVP or deferred (OQ-02) | See ADR-004 below — currently a recommendation, not yet Accepted |
| T2-11 | Share card variants at launch (OQ-05) | 1:1 only vs. also 9:16 Story |
| T1-05, T1-13 | Auto-pause default and threshold (OQ-06) | Affects riding-time accuracy vs. false-positive pause prompts |
| T2-01, T2-06 | Email verification required before publish (OQ-07) | Affects onboarding friction vs. spam risk |
| ~~T3-02~~ | ~~Product name: RideCircle vs. RIDELINE (OQ-09)~~ — **decided 2026-09-15**, ADR-009: RideCircle. Substitution table added to `TASKS/specs/T3-02-landing-page.md` | The pasted landing-page spec used a different name throughout; resolving it unblocked `T3-02` |

---

## Log

### ADR-001 — Establish `TASKS/` and `MEMORY/` as the execution layer

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | — |
| **Deciders** | Product owner (user), Claude (scaffolding session) |

**Context** — The source brief recommended 47 categories of product documentation for a motorcycle-native "Strava clone." Without an execution layer, `docs/` would describe intent forever without a mechanism for tracking what's actually built, why implementation diverged from the plan, or what's left. The user's own existing project (`zed-auth`) already has a proven `TASKS/`/`MEMORY/`/`CLAUDE.md`/`AGENTS.md` convention; this project adopts the same shape rather than inventing a new one.

**Decision** — Use the same three-layer structure: `docs/` (reference, what to build), `TASKS/` (forward, what's next and how it's judged done), `MEMORY/` (backward, what happened and why). Task IDs follow `T<phase>-<nn>`. Every `DONE` task requires a MEMORY record — no exceptions.

**Alternatives considered**
- A single flat `TODO.md` — rejected, no record of *why* decisions were made, becomes unreadable past a few dozen items.
- GitHub Issues/Projects as the source of truth — rejected for this phase; markdown-in-repo keeps the history alongside the code and doesn't require external tooling for an AI agent to read the full context in one pass.

**Consequences** — More overhead per task (a change record is mandatory) than a lighter process would require. In exchange, six months from now the reasoning behind any non-obvious choice is recoverable from the repo itself, not from someone's memory of a conversation. This matters more for RideCircle's location-privacy decisions than it would for a typical CRUD app.

**Plan impact** — None; this ADR documents the meta-decision, not a `docs/` deviation.

---

### ADR-002 — MVP scope limited to Ride Tracking + Social Media Share

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | — |
| **Deciders** | Product owner (user) |

**Context** — The recommended documentation structure covers 47 categories spanning Motorcycle identity, Community, Group Ride, Safety, Route Discovery, Monetization, AI, and more. Building against the full structure invites scope creep in a product area that is already unusually broad for a first release.

**Decision** — MVP = Ride Tracking + Social Media Share only, explicitly. All other categories are scaffolded in `docs/` as `Status: Post-MVP` placeholders with no task breakdown in `TASKS/`.

**Alternatives considered**
- Build a thinner slice of every pillar (a little bit of Safety, a little bit of Community) — rejected; produces a product that's shallow everywhere and differentiated nowhere, and multiplies the surface area needing compliance/safety review before anything ships.
- Start with Motorcycle Identity instead of Social Share, since it's cheaper — rejected by the user; Tracking + Share is the minimum loop that produces user-visible value (record a ride, show it off) without requiring a second user's device (unlike Group Ride) or ongoing operational safety guarantees (unlike Safety features).

**Consequences** — Faster to a working product; smaller compliance/security surface to get right before launch. Forecloses, for this release, any of the "killer feature" differentiators identified in the source brief (Group Ride, Safety, Motorcycle identity) — those remain paper plans until a deliberate Phase 3 decision.

**Plan impact** — `docs/00-PRODUCT/04-PRODUCT-SCOPE.md` and `docs/47-ROADMAP/01-MVP-SCOPE.md` already encode this; no further amendment needed.

---

### ADR-003 — GPS upload is batched at ride completion, not streamed live

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T1-06 |
| **Deciders** | Claude (scaffolding session), pending product owner confirmation |

**Context** — Live, real-time location streaming is only genuinely needed by Group Ride's live-member-tracking feature, which is Post-MVP. Building a realtime pipeline (WebSocket/event bus) for MVP would add backend complexity with no MVP-facing benefit.

**Decision** — The mobile client buffers GPS points locally for the duration of a ride and uploads them as a batch once the ride reaches `completed`. No realtime location transmission exists in MVP.

**Alternatives considered**
- Stream points to the backend as they're sampled — rejected for MVP; requires realtime infrastructure (`docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` explicitly excludes a message queue from MVP) that only pays off once Group Ride exists.

**Consequences** — Simpler backend, lower data usage, works offline for the whole ride. The cost: this is a real architectural debt for Phase 2 of the roadmap (Group Ride) — live tracking will need new infrastructure, not an extension of this pipeline. Documented so it isn't a surprise later.

**Plan impact** — Reflected in `docs/13-GPS/00-GPS-ARCHITECTURE.md` and `MEMORY/ARCHITECTURE-NOTES.md` already.

---

### ADR-004 — Recommend a privacy zone around ride start/finish points (Proposed, not yet Accepted)

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Proposed |
| **Task** | T1-11, T1-12 (blocked pending this decision — see `TASKS/BACKLOG.md` OQ-02) |
| **Deciders** | Pending product owner |

**Context** — A public ride's full track, by default, reveals the rider's exact start and end points — commonly home and/or workplace. This was not explicitly requested in the source brief, but it's a foreseeable privacy risk once "publish ride to feed" ships, given `docs/45-COMPLIANCE/03-LOCATION-DATA.md`'s framing of location as sensitive data requiring privacy-by-default.

**Decision (proposed)** — Hide the first/last ~200m of a publicly visible ride's displayed track (distance/duration/speed metrics still computed from the full, unmodified track — only the displayed map geometry is truncated).

**Alternatives considered**
- Do nothing, rely on rider judgement — rejected as the default; visible in feed by default is opt-out privacy, which conflicts with the "private by default" principle already adopted elsewhere in `docs/45-COMPLIANCE/03-LOCATION-DATA.md`.
- Let the rider manually crop their own track before publishing — more rider control, more implementation and UX cost; worth reconsidering if the automatic 200m rule proves too aggressive or too weak in practice.

**Consequences** — Meaningfully reduces address-inference risk for the common "ride starts/ends at home" case. Costs: slightly more complex track-rendering logic (two code paths: full track for the owner, truncated for public viewers), and 200m is a somewhat arbitrary constant that may need tuning.

**Plan impact** — If accepted, `docs/45-COMPLIANCE/03-LOCATION-DATA.md` and `docs/01-PRD/05-RIDE-HISTORY.md` should both be amended to state this as a firm requirement rather than a recommendation, and `TASKS/PHASE-1-MVP-TRACKING.md` tasks T1-11/T1-12 should gain an explicit DoD line for it.

---

### ADR-005 — Feed uses fan-out-on-read for MVP

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T2-07 |
| **Deciders** | Claude (scaffolding session) |

**Context** — Two standard approaches exist for generating a social feed: fan-out-on-write (precompute each follower's feed when a post is created) and fan-out-on-read (query across followees at request time). Fan-out-on-write scales better at very large follower counts but adds write-path complexity and a new data structure.

**Decision** — MVP uses fan-out-on-read: a single query joining `Follow` and `Post` at request time, per `docs/24-SOCIAL/03-FEED.md`.

**Alternatives considered**
- Fan-out-on-write from day one — rejected for MVP; premature optimization for a launch-scale user base, adds a write-path failure mode (partial fan-out on crash) that has no payoff yet.

**Consequences** — Simple to implement and reason about now. Will need revisiting (documented in `MEMORY/ARCHITECTURE-NOTES.md`) once any rider accumulates a very large following count — the query cost grows with the number of people followed, not a fixed cost.

**Plan impact** — None; matches `docs/24-SOCIAL/03-FEED.md` as written.

---

### ADR-006 — Mobile: native Android (Kotlin) + native iOS (Swift), not cross-platform

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T0-01, T0-09 |
| **Deciders** | User |

**Context** — `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` had left this as an open "usulan" between native and cross-platform (React Native/Flutter), leaning cross-platform for MVP speed. The user has since specified Android and iOS as the target platforms explicitly, in the context of requesting platform-specific coding standards — read as a decision for native, not a cross-platform framework targeting both OSes.

**Decision** — Two native codebases: Android in Kotlin (Jetpack Compose, MVVM), iOS in Swift (SwiftUI, MVVM). No React Native, Flutter, or other cross-platform layer.

**Alternatives considered**
- Cross-platform (React Native/Flutter) — would have meant one codebase and faster initial delivery, but background GPS recording (`docs/16-RIDE/02-RIDE-RECORDING.md`) is exactly the category of feature where cross-platform frameworks add friction: foreground services on Android and background location modes on iOS both need platform-specific handling regardless, which erodes much of the "write once" benefit for this specific feature.
- Native Android only, iOS later — rejected; user asked for both platforms now.

**Consequences** — Two codebases to maintain, two sets of platform conventions (this ADR is why `android/docs/CODING_STANDARDS.md` and `ios/docs/CODING_STANDARDS.md` are separate documents rather than one). In exchange, full access to each platform's background-location and foreground-service APIs without a compatibility-layer workaround, which matters directly for `docs/13-GPS/00-GPS-ARCHITECTURE.md`'s resilience requirements.

**Plan impact** — `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` tech stack table and directory layout updated to `android/` + `ios/` in place of the earlier `mobile/` placeholder. `CLAUDE.md`/`AGENTS.md` directory layout sections updated to match.

---

### ADR-007 — Backend: Node.js + TypeScript + Express + Prisma + PostgreSQL/PostGIS + Redis

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | **Superseded by ADR-010** (framework) — the Prisma, PostgreSQL/PostGIS, Redis, BullMQ, Zod, and custom-JWT parts of this decision still stand, carried forward into ADR-010. Object-storage choice superseded by ADR-011. |
| **Task** | T0-01, T0-04, T0-08 |
| **Deciders** | User (instruction to decide: "putuskan saja yang terbaik untuk platform ini"), Claude (scaffolding session) |

**Context** — `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` left the backend language, framework, database, and auth approach open. The team's other project, `callibrator`, runs Express + Sequelize + PostgreSQL + Redis in plain JavaScript, with a documented `CODING_STANDARDS.md`.

**Decision**
- **Language/framework**: Node.js with TypeScript, Express — same shape as `callibrator`, so its conventions (layered controller/service/route, `success()` response envelope) carry over directly.
- **ORM**: Prisma instead of Sequelize — first-class TypeScript support (generated types from schema) and a simpler migration workflow.
- **Database**: PostgreSQL with the PostGIS extension enabled from the start.
- **Cache**: Redis, for rate limiting and the JWT refresh-token/session layer.
- **Background jobs**: BullMQ (Redis-backed), for polyline simplification and share-card pre-rendering.
- **Validation**: Zod — one schema is both the runtime validator and the static type.
- **Object storage**: S3-compatible (AWS S3 / Cloudflare R2 / MinIO).
- **Auth**: custom JWT (access + refresh), not a third-party provider.

**Alternatives considered**
- **Go** — better raw throughput, but no team experience and MVP workload doesn't justify the learning curve.
- **Plain JavaScript (as in `callibrator`)** — rejected; GPS/metric code benefits specifically from static types.
- **Auth0 / Supabase Auth** — rejected; team already operates JWT auth successfully in `callibrator`.

**Consequences** — Maximum reuse of `callibrator` conventions. Express provides no module system or DI, so structure is enforced by convention and review only.

**Plan impact** — `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` tech stack table updated. `backend/docs/CODING_STANDARDS.md` created.

---

### ADR-008 — Web: one Next.js app for landing page + admin dashboard, not two

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T0-01 (extended scope), T3-* (new Phase 3) |
| **Deciders** | Claude (scaffolding session), per user's request to add landing page + admin dashboard |

**Context** — The user asked to add a landing page and an admin dashboard, and to write coding conventions for them. Both are web surfaces the mobile-focused architecture hadn't accounted for. `callibrator` (the team's other project) already solves this exact problem: one Next.js app (`frontend/`) serves both the public marketing site (`app/`, `components/landing/`) and the authenticated admin console (`app/dashboard/`), documented in `docs/FRONTEND/00-FRONTEND-STANDARDS.md`.

**Decision** — One `web/` app, Next.js (App Router), React, TypeScript, Tailwind CSS, Zustand for state that outlives a page. Public routes (`/`, marketing) and admin routes (`/admin/*`, behind auth) live in the same Next.js project, same as `callibrator/frontend`. API access goes through a layered `client → service → hook → page` structure with the same `{success, status, message, data, meta}` envelope the backend already returns (`backend/docs/CODING_STANDARDS.md` §4) — no translation layer needed since `backend/docs/CODING_STANDARDS.md` was already written to match this envelope shape.

**Alternatives considered**
- Two separate apps (a static marketing site + a separate admin SPA) — rejected; doubles build/deploy/hosting setup for no MVP-stage benefit, and this team has a working, documented single-app pattern already (`callibrator/frontend`) that handles the traffic-shape difference (public/cacheable vs. authenticated/dynamic) fine via Next.js route segments.
- A dashboard framework/admin-panel generator (Retool, Refine, etc.) — rejected; the team already has hand-rolled admin UI conventions (RBAC-in-UI, audit-log-aware actions) documented and working in `callibrator`, and a generator would fight those conventions rather than reuse them.

**Consequences** — One more codebase (`web/`) alongside `backend/`, `android/`, `ios/`. Reuses a stack and a set of hard-won rules (`callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md` — envelope unwrap bugs, RBAC "absent not hidden," error-as-UI-state) the team has already paid the cost to learn, rather than rediscovering them. The landing page inherits some admin-dashboard machinery (auth-aware routing, the API client) it doesn't need, which is a minor complexity tax justified by not maintaining a second app.

**Plan impact** — `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` updated: `web/` added to the component diagram and tech stack table. `docs/01-PRD/21-ADMIN-MODERATION.md` promoted from Post-MVP to MVP (a public social feed needs a moderation path from day one — see that document for the full reasoning). `docs/01-PRD/22-LANDING-PAGE.md` created (new, MVP). `TASKS/PHASE-3-WEB.md` created. `web/docs/CODING_STANDARDS.md` created, modeled directly on `callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md`.

---

### ADR-009 — Product name stays RideCircle (not RIDELINE)

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T3-02 |
| **Deciders** | User |

**Context** — `TASKS/specs/T3-02-landing-page.md`, a detailed landing-page brief the user pasted, names the product "RIDELINE" in six places (wordmark, hero activity card, footer brand line, footer copyright, SEO page title). Every other document in this repo — `docs/00-PRODUCT/00-PRODUCT-VISION.md`, the brand identity work done earlier in this project, `backend/`/`android/`/`ios/`/`web/` naming — uses "RideCircle." This was flagged rather than resolved silently (`MEMORY/records/2026-09-15-T3-02-landing-page-spec.md`, `TASKS/BACKLOG.md` OQ-09).

**Decision** — The product name is **RideCircle**. The landing-page spec's six RIDELINE occurrences are implemented as RideCircle; a substitution table was added to the end of `TASKS/specs/T3-02-landing-page.md` rather than editing the pasted spec's verbatim body, so the document stays an accurate record of what was actually provided.

**Alternatives considered**
- Rename the product to RIDELINE — was the literal content of the pasted spec, but nothing else in this session indicated an actual rename decision; treating a design brief's placeholder name as a de facto rebrand would have been exactly the kind of silent decision `AGENTS.md` rule 9 exists to prevent.

**Consequences** — No rename churn across `docs/`, the brand identity assets already designed, or the four platform codebases' naming. The landing-page spec needed a small addendum (the substitution table) rather than being usable completely as-is — a minor implementation-time cost, paid once, documented in one place.

**Plan impact** — `TASKS/PHASE-3-WEB.md` `T3-02` unblocked (`TODO`). `TASKS/BACKLOG.md` OQ-09 marked resolved. `TASKS/PROGRESS.md` updated.

---

### ADR-010 — Backend framework: NestJS (supersedes ADR-007's Express choice)

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T0-01 (amends), T0-04, T0-08 |
| **Deciders** | User |

**Context** — ADR-007 chose Express to mirror `callibrator`. Before any backend code existed (`T0-04` still `TODO`), the user decided to use NestJS instead. Changing now costs only documentation; changing after `T0-04` would cost a rewrite.

**Decision**
- **Framework**: NestJS on its default HTTP adapter (`@nestjs/platform-express`). One Nest module per domain module (`auth`, `rider`, `ride`, `social`, later `admin`), plus `infra/` modules for Prisma, Redis, BullMQ, and storage.
- **Carried forward unchanged from ADR-007**: TypeScript, Prisma, PostgreSQL + PostGIS, Redis, BullMQ (now via `@nestjs/bullmq`), custom JWT (now via `@nestjs/jwt`, no Passport), the `{success, status, message, data, meta}` response envelope.
- **Validation stays Zod**, applied through a small custom `ZodValidationPipe` — **not** class-validator/class-transformer, so HTTP input, env config, and job payloads share one validation system and one error format.
- **Envelope and errors** are produced by one global interceptor and one global exception filter, not by per-controller helpers.
- **Auth is secure by default**: a global guard requires a rider JWT on every route unless marked `@Public()`; `@AdminAuth()` routes verify a separate admin secret (keeps `AGENTS.md` hard rule 10).
- **Testing**: Vitest (with `unplugin-swc` for decorator metadata) + `@nestjs/testing` + Supertest.

Detail: `backend/docs/CODING_STANDARDS.md`.

**Alternatives considered**
- **Express (ADR-007)** — maximum reuse of `callibrator` conventions, but no DI or module system; architectural boundaries are enforced only by review.
- **NestJS + class-validator DTOs (Nest's default)** — idiomatic and integrates with `@nestjs/swagger`, but would introduce a second validation system alongside Zod (still needed for env and job payloads). OpenAPI generation is Post-MVP anyway (`docs/39-DEVELOPER/`).
- **NestJS on Fastify** — faster, but the MVP workload doesn't need it, and some Nest ecosystem middleware assumes Express. Can be revisited later without touching domain code.

**Consequences** — DI makes services testable with overridden providers, and module `exports` make cross-module dependencies explicit. Global guard/filter/interceptor remove a class of "forgot the middleware" bugs. Costs: more boilerplate per feature (module + decorators), a steeper learning curve than Express, decorator metadata requiring SWC in the test toolchain, and less direct copy-paste from `callibrator`'s Express code.

**Plan impact** — `backend/docs/CODING_STANDARDS.md` rewritten. `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` tech stack table amended. `CLAUDE.md`, `AGENTS.md`, `README.md`, `TASKS/PHASE-0-FOUNDATION.md`, `TASKS/PHASE-3-WEB.md`, `TASKS/BACKLOG.md` updated. Record: `MEMORY/records/2026-09-15-ADR-010-011-nestjs-storage-driver.md`.

---

### ADR-011 — Storage is driver-agnostic; default driver is the VM's local disk

| | |
|---|---|
| **Date** | 2026-09-15 |
| **Status** | Accepted |
| **Task** | T0-11 (new), T0-05, T1-06, T1-12 |
| **Deciders** | User |

**Context** — ADR-007 assumed S3-compatible object storage (AWS S3 / R2 / MinIO) for raw GPS points and generated images. The user wants the storage backend to be swappable, with the default being the disk of the VM the backend runs on — no object-storage service required to deploy.

**Decision**
- All file storage goes through a `StorageDriver` interface (`put`, `get`, `exists`, `delete`, `publicUrl`), injected via the `STORAGE_DRIVER` token. The driver is selected at boot by the `STORAGE_DRIVER` env var.
- **`local` is the default and the only driver built for MVP.** It stores under `STORAGE_LOCAL_ROOT` with path-traversal protection and atomic writes; public files are served by the backend at `/files/public/*`.
- An **`s3` driver (S3-compatible)** is the documented second implementation, built when a deployment needs it — not speculatively.
- **The database stores storage keys, never URLs or filesystem paths** (`Track.raw_points_ref`). Visibility is encoded in the key prefix (`private/…`, `public/…`); raw GPS points are always `private/` and never served over HTTP.
- Every driver must pass one shared contract test suite.

**Alternatives considered**
- **S3-compatible only (ADR-007)** — scales horizontally and offloads backups/durability, but forces an extra service (or MinIO container) on every environment, including a single small VM.
- **MinIO on the VM as the "local" option** — keeps one code path (S3 API), but adds a stateful service to operate for what is, at MVP scale, a directory of files.
- **Store raw points in Postgres** — rejected already by `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` (thousands of rows per ride).
- **Building both `local` and `s3` drivers now** — rejected; the second driver would be untested against a real deployment. The interface + contract suite is what keeps it a drop-in.

**Consequences** — Simplest possible deployment: one VM, one volume, no object-storage vendor or credentials. Switching later is a data copy with identical keys plus an env change — no schema migration. Costs, stated plainly:
- **Single-instance ceiling**: with `local`, the API and BullMQ workers must share one filesystem. Running more than one backend instance requires a shared volume or switching to `s3` first.
- **Durability is the VM's**: the storage directory must be included in VM backups/snapshots; disk-full becomes an operational risk to monitor.
- **The backend serves public images** (share cards, map thumbnails) itself, instead of a bucket/CDN — acceptable at MVP scale; a CDN is already Post-MVP per `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md`.
- The interface is intentionally minimal: presigned direct uploads, lifecycle rules, and listing are unavailable until a task needs them and every driver implements them.

**Plan impact** — `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` (principle, diagram, tech table), `docs/07-DOMAIN/03-RIDE.md` (`raw_points_ref` comment), `docs/13-GPS/00-GPS-ARCHITECTURE.md`, and `docs/45-COMPLIANCE/03-LOCATION-DATA.md` wording amended from "object storage (S3-compatible)" to driver-agnostic storage — no requirement changed. New task `T0-11` added to `TASKS/PHASE-0-FOUNDATION.md`; `T0-05`, `T1-06`, `T1-12` updated. `backend/docs/CODING_STANDARDS.md` §9 written.
