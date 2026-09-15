# Phase 3 — Web: Landing Page + Admin Dashboard

Gate to enter: Phase 0 exit checklist. May run in parallel with Phase 1/Phase 2 for the landing-page tasks (T3-01–T3-03, no backend dependency); the admin-dashboard tasks (T3-04 onward) additionally need the report/suspend endpoints they depend on, which in turn need `docs/24-SOCIAL/` (Phase 2) to exist.

Added after the initial MVP scope was locked — see `MEMORY/DECISIONS.md` ADR-008 for why a moderation path was pulled into MVP rather than left post-launch.

---

### T3-01 — Web app skeleton

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-01, T0-02 |
| **Docs refs** | `web/docs/CODING_STANDARDS.md` |
| **Surface** | web |

**Definition of Done**
- [ ] Next.js app builds and runs, matching `web/docs/CODING_STANDARDS.md` project structure
- [ ] `client.ts` implemented with envelope unwrap (§5), pointed at the local `backend/`

---

### T3-02 — Landing page sections

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T3-01 |
| **Docs refs** | `docs/01-PRD/22-LANDING-PAGE.md`, `web/docs/CODING_STANDARDS.md` §9 |
| **Spec required** | Yes — `TASKS/specs/T3-02-landing-page.md` (full design/implementation brief: copy, color system, typography, section-by-section layout, motion, image policy, component list). Product name resolved — RideCircle, not RIDELINE, per the spec's own § Product name substitutions and `MEMORY/DECISIONS.md` ADR-009. |
| **Surface** | web |

**Goal** — implement all 16 sections listed in `TASKS/specs/T3-02-landing-page.md` §6 (Page Structure), matching its copy, visual direction, and component naming exactly, applying the six RideCircle/RIDELINE substitutions listed at the end of that spec.

**Definition of Done**
- [ ] All 16 sections implemented per the spec §6–§23
- [ ] All six product-name substitutions applied (spec § Product name substitutions) — no "RIDELINE" string anywhere in shipped output
- [ ] `docs/ASSETS.md` created, every external image documented per the spec §24 before it's used — no asset with ambiguous licensing
- [ ] Component structure matches spec §27, placed per `web/docs/CODING_STANDARDS.md` §1/§3 (`src/components/landing/`, one file per section)
- [ ] Content centralized per spec §44 (no hardcoded repeated strings in JSX)
- [ ] Spec §47 "Final Implementation Checklist" fully satisfied — treat that checklist as this task's real Definition of Done, the summary above is not a substitute for it
- [ ] No client-side data fetching on `/` (`web/docs/CODING_STANDARDS.md` §9)

**Edge cases to test**
- [ ] Reduced-motion preference disables entrance/parallax/map-drawing animation (spec §31, §34)
- [ ] No horizontal overflow at any breakpoint (spec §32 checklist)
- [ ] Every image has correct alt text or is marked decorative (spec §34)

---

### T3-03 — SEO & performance

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T3-02 |
| **Docs refs** | `docs/01-PRD/22-LANDING-PAGE.md`, `TASKS/specs/T3-02-landing-page.md` §42 (SEO), §35 (Performance) |
| **Spec required** | No — covered by `TASKS/specs/T3-02-landing-page.md` |
| **Surface** | web |

**Definition of Done**
- [ ] Metadata (title/description/OG image) set via Next.js Metadata API, exact copy per spec §42
- [ ] `sitemap.xml`, `robots.txt` present
- [ ] Hero image eager-loaded, below-fold images lazy-loaded, explicit dimensions to prevent CLS (spec §35)
- [ ] Lighthouse performance score recorded

---

### T3-04 — Admin auth (separate from rider auth)

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-08, T3-01 |
| **Docs refs** | `docs/01-PRD/21-ADMIN-MODERATION.md` |
| **Surface** | backend, web |

**Goal** — an `AdminUser` model and a login flow entirely separate from `Rider`/`docs/01-PRD/01-AUTHENTICATION.md` — no shared endpoint, no role flag on the rider JWT.

**Definition of Done**
- [ ] `AdminUser` table (backend)
- [ ] `/admin/v1/auth/login` endpoint; admin routes use `@AdminAuth()` with a separate secret, never the rider JWT path (`backend/docs/CODING_STANDARDS.md` §8)
- [ ] `/login` admin page, `adminAuthStore` (web)
- [ ] `app/admin/layout.tsx` redirects unauthenticated requests to `/login`

---

### T3-05 — Report data model + rider-side report action

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-06, T2-09 |
| **Docs refs** | `docs/01-PRD/21-ADMIN-MODERATION.md` |
| **Surface** | backend, android, ios |

**Goal** — riders can report a post or comment; this is a small addition to the Social Share surface that `docs/24-SOCIAL/` didn't originally include (flagged in `TASKS/BACKLOG.md` as a gap found while scoping the admin dashboard).

**Definition of Done**
- [ ] `Report` table (`targetType`, `targetId`, `reporterId`, `reason`, `status`)
- [ ] Report endpoint (rider-facing)
- [ ] "Laporkan" action on post/comment in Android and iOS apps

---

### T3-06 — Reports queue screen

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T3-04, T3-05 |
| **Docs refs** | `docs/01-PRD/21-ADMIN-MODERATION.md`, `web/docs/CODING_STANDARDS.md` §10 |
| **Surface** | backend, web |

**Definition of Done**
- [ ] `/admin/v1/reports` endpoint (list pending, resolve)
- [ ] Reports queue screen: loading/empty/error/success states (§8)
- [ ] Resolve action requires a `reason`, has a confirmation step (§10)

---

### T3-07 — Moderation actions + audit log

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T3-06 |
| **Docs refs** | `docs/01-PRD/21-ADMIN-MODERATION.md` |
| **Surface** | backend, web |

**Definition of Done**
- [ ] Delete post/comment action (admin), reuses existing soft-delete from `docs/24-SOCIAL/`
- [ ] Suspend rider action (`Rider.status = suspended`, blocks login)
- [ ] `ModerationAuditLog` table, append-only, every action above writes a row
- [ ] Audit log view (read-only, per §10)

---

### T3-08 — Rider search screen

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T3-04 |
| **Docs refs** | `docs/01-PRD/21-ADMIN-MODERATION.md` |
| **Surface** | backend, web |

**Definition of Done**
- [ ] `/admin/v1/riders/search` endpoint (email/username)
- [ ] Rider detail view: profile, stats, report history against that rider
