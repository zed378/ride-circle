# Coding Standards & Guidelines — Web (Landing Page + Admin Dashboard)

Modeled on [`callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md`](https://github.com/zed378/callibrator/blob/main/docs/FRONTEND/00-FRONTEND-STANDARDS.md) — same team, same stack, same hard-won rules. One Next.js app serves both the public landing page and the authenticated admin dashboard, per `MEMORY/DECISIONS.md` ADR-008.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Naming Conventions](#2-naming-conventions)
3. [Project Structure](#3-project-structure)
4. [API Access Layering](#4-api-access-layering)
5. [The Response Envelope](#5-the-response-envelope)
6. [State (Zustand)](#6-state-zustand)
7. [Authorization Is Not a Frontend Concern](#7-authorization-is-not-a-frontend-concern)
8. [Errors Are a UI State](#8-errors-are-a-ui-state)
9. [Landing Page Standards](#9-landing-page-standards)
10. [Admin Dashboard Standards](#10-admin-dashboard-standards)
11. [Styling](#11-styling)
12. [Accessibility](#12-accessibility)
13. [Testing Standards](#13-testing-standards)
14. [Git & Commit Conventions](#14-git--commit-conventions)

---

## 1. Project Overview

### Technology Stack

| Component | Technology | Notes |
|---|---|---|
| Framework | Next.js (App Router) | Same major version family as `callibrator/frontend` |
| UI library | React | |
| Language | TypeScript | `any` banned — same rule as `callibrator` |
| Styling | Tailwind CSS | Semantic tokens only, never raw color primitives (§11) |
| State | Zustand | One store per concern that outlives a page (§6) |
| HTTP client | axios, wrapped in a single `client.ts` | Never called directly from a component |
| Icons | lucide-react | |
| Animation | framer-motion | Landing page polish only — the admin dashboard should not animate for its own sake |
| Testing | Jest + React Testing Library | Component tests; service contract tests (§4) |

Per `docs/47-ROADMAP/01-MVP-SCOPE.md`: only build routes/screens backed by a `Status: MVP` document. `docs/01-PRD/21-ADMIN-MODERATION.md` and `docs/01-PRD/22-LANDING-PAGE.md` are what this app implements — not a general-purpose admin panel or marketing CMS beyond what those documents describe.

### Project Structure

```
web/
├── docs/
│   └── CODING_STANDARDS.md
├── public/
│   ├── marketing/                 # landing page images, OG image
│   └── brand/                     # logo, favicon — from the RideCircle brand assets
├── src/
│   ├── app/
│   │   ├── page.tsx                # landing page ("/")
│   │   ├── layout.tsx              # root layout — public, no auth check
│   │   ├── privacy/page.tsx
│   │   ├── terms/page.tsx
│   │   ├── login/page.tsx          # admin login — separate from rider auth
│   │   └── admin/
│   │       ├── layout.tsx          # auth-gated layout, redirects to /login if no session
│   │       ├── page.tsx            # dashboard home (report queue count, etc.)
│   │       ├── reports/
│   │       │   ├── page.tsx
│   │       │   ├── components/     # local to this domain
│   │       │   └── hooks/          # local to this domain
│   │       ├── riders/
│   │       │   ├── page.tsx
│   │       │   ├── [id]/page.tsx
│   │       │   ├── components/
│   │       │   └── hooks/
│   │       └── audit-log/
│   │           └── page.tsx
│   ├── api/
│   │   ├── client.ts                # base URL, auth header, envelope unwrap
│   │   └── services/
│   │       ├── reports.service.ts
│   │       ├── riders.service.ts
│   │       └── auditLog.service.ts
│   ├── components/
│   │   ├── landing/                 # HeroSection.tsx, FeaturesSection.tsx, CtaSection.tsx, ...
│   │   ├── admin/                   # shared admin UI: DataTable, EmptyState, ErrorState
│   │   └── ui/                      # generic primitives (Button, Card) shared by both surfaces
│   ├── stores/
│   │   ├── adminAuthStore.ts
│   │   └── toastStore.ts
│   ├── hooks/                       # cross-domain hooks only (rare) — most hooks live with their domain
│   ├── types/                       # hand-written API response types, PascalCase
│   ├── lib/                         # generic helpers (date formatting, etc.)
│   └── tests/
├── next.config.ts
├── tsconfig.json
└── package.json
```

**Local by default**, same rule as `callibrator`: a component moves to `src/components/` only when a *second* route needs it, not in anticipation. `src/app/admin/reports/components/` stays local to Reports until Riders also needs the same component.

---

## 2. Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Component files | `PascalCase.tsx` | `HeroSection.tsx`, `ReportsTable.tsx` |
| Hooks | `useThing.ts` | `useReportsQueue.ts` |
| Services | `<domain>.service.ts` | `reports.service.ts` |
| Stores | `<domain>Store.ts` | `adminAuthStore.ts` |
| Types | `PascalCase` in `src/types/` | `Report`, `RiderSummary` |
| Tests | `<name>.test.ts(x)` beside the subject | `reports.service.test.ts` |
| Routes (folders under `app/`) | `kebab-case` | `app/admin/audit-log/` |

---

## 3. Project Structure

See §1's tree. Two additional rules specific to this project (beyond `callibrator`'s, which has no public marketing side sharing a codebase with its dashboard in quite the same proportion):

- **`components/landing/` and `components/admin/` never import from each other.** They're different audiences with different trust levels and different performance budgets (landing must be fast and mostly static; admin can afford more client-side JS). A shared need goes in `components/ui/`, not a cross-import.
- **The admin dashboard is small at MVP** (`docs/01-PRD/21-ADMIN-MODERATION.md`: reports, riders, audit log — three sections). Resist building out a generic "admin panel framework" with configurable tables/forms ahead of need — three real screens, built directly, per `docs/07-DOMAIN/00-DOMAIN-MODEL.md` § Catatan desain's general "don't build for entities that don't exist yet" principle.

---

## 4. API Access Layering

Never call `axios` from a component. Same layering as `callibrator/frontend`:

```
page → hook → service (src/api/services/) → client.ts → API
```

| Layer | Owns |
|---|---|
| `client.ts` | base URL, auth header (admin JWT, separate from any rider token), envelope unwrap, error normalization |
| service | one module per backend domain, one function per endpoint |
| hook | loading, error, and empty state for one screen |
| page | layout and composition |

```typescript
// api/services/reports.service.ts
import { apiClient } from "../client";
import type { Report } from "@/types/Report";

export async function fetchPendingReports(page: number): Promise<{ data: Report[]; meta: PageMeta }> {
  return apiClient.get("/admin/v1/reports", { params: { status: "pending", page } });
}

export async function resolveReport(reportId: string, action: "delete_content" | "dismiss", reason: string) {
  return apiClient.post(`/admin/v1/reports/${reportId}/resolve`, { action, reason });
}
```

```typescript
// app/admin/reports/hooks/useReportsQueue.ts
export function useReportsQueue(page: number) {
  const [state, setState] = useState<"loading" | "success" | "error" | "empty">("loading");
  const [reports, setReports] = useState<Report[]>([]);

  useEffect(() => {
    fetchPendingReports(page)
      .then((res) => {
        setReports(res.data);
        setState(res.data.length === 0 ? "empty" : "success");
      })
      .catch(() => setState("error"));
  }, [page]);

  return { state, reports };
}
```

**Every service gets a contract test.** Per `callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md`: a mock test proves the client calls what the developer *believed* the API looked like — it does not prove the endpoint exists or behaves that way. That gap has burned this exact team before (`callibrator`'s QMS/SOP screens shipped against endpoints that returned data in a shape the mocked tests didn't catch). At minimum, run each admin service function against the real backend (`backend/` running locally, per `TASKS/PHASE-0-FOUNDATION.md` T0-05) once before considering the task done — see `TASKS/00-TASK-CONVENTIONS.md` § Global Definition of Done.

---

## 5. The Response Envelope

```
{ success, status, message, data, meta? }
```

Matches `backend/docs/CODING_STANDARDS.md` §4 exactly — **rows are in `data`, pagination is in a top-level `meta`**, never `data.rows` or `data.items`. `client.ts` unwraps `data` and surfaces `meta` separately; a service reaching past the unwrap is doing it wrong.

Getting this wrong renders an empty list with **no error** — exactly the failure mode `callibrator` hit in production. Test the unwrap explicitly, including what happens on an empty `data: []` and on a malformed response.

---

## 6. State (Zustand)

One store per concern, **only for state that outlives a page**. Data fetched for one screen belongs in that screen's hook (§4), not a store.

| Legitimate stores for this app | |
|---|---|
| `adminAuthStore` | admin session, current admin user |
| `toastStore` | transient feedback across the admin dashboard |

That's it for MVP — this app doesn't need `callibrator`'s `menuStore` (no dynamic RBAC menu tree, one admin role) or `tenantBrandingStore` (no multi-tenant branding). Don't add a store "for consistency" with `callibrator` if nothing here actually needs one — an unused store is dead weight, not a pattern worth copying reflexively.

---

## 7. Authorization Is Not a Frontend Concern

The admin dashboard shows only what the admin's session allows, but **the backend enforces on every `/admin/v1/*` route regardless** — a hidden button in the UI is not a security control. `docs/01-PRD/21-ADMIN-MODERATION.md` specifies a single admin role for MVP, so this matters less acutely than in `callibrator`'s multi-role RBAC system, but the principle still applies: don't let "the UI didn't show the button" stand in for a real server-side check, even with one role, because that assumption breaks the moment a second role is added later.

---

## 8. Errors Are a UI State

Every list (reports queue, riders search, audit log) has three states: loading, empty, **failed** — as distinct components (`EmptyState`, `ErrorState` in `components/admin/`), never collapsed into one "no data" rendering.

Rendering an empty list when the request actually failed is a lie about what's happening — in this app specifically, it could mean a moderator believes there are no pending reports when the reports endpoint is actually erroring. This is the single most important rule carried over from `callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md`, and it matters here for the same reason it mattered there.

---

## 9. Landing Page Standards

Per `docs/01-PRD/22-LANDING-PAGE.md`:

- **Static/server-rendered by default.** No client-side data fetching on the landing page for MVP — everything is either static JSX or Next.js server-rendered at build/request time. No spinner should ever appear on `/`.
- **`components/landing/` sections are self-contained**: `HeroSection.tsx`, `FeaturesSection.tsx`, `CtaSection.tsx`, etc. — one file per visual section, composed in `app/page.tsx`, mirroring `callibrator/frontend`'s landing structure.
- **SEO**: `metadata` export in `app/layout.tsx`/`app/page.tsx` (Next.js Metadata API) for title/description/OG image — not a manually-managed `<head>`.
- **Performance budget**: landing page ships minimal client JS. `framer-motion` is fine for section entrance animation; avoid pulling heavy client-side libraries onto this route that the admin dashboard needs but the landing page doesn't (bundle analysis should show the two route groups aren't sharing unnecessary weight).

---

## 10. Admin Dashboard Standards

- **Every moderation action requires a `reason` field**, submitted with the request and rendered later in the audit log view (`docs/01-PRD/21-ADMIN-MODERATION.md` requirement 5) — the UI should not allow submitting delete/suspend actions without one.
- **Destructive actions get a confirmation step** — deleting a post, suspending a rider. A single accidental click on a moderation dashboard has real consequences for a real person's account.
- **The audit log view is read-only** — no edit or delete affordance anywhere near it, reflecting that the underlying table is append-only (`docs/01-PRD/21-ADMIN-MODERATION.md`).
- **`DataTable` component** (`components/admin/DataTable.tsx`) is the one shared table implementation for Reports, Riders, and Audit Log — don't hand-roll three separate table layouts for what is structurally the same list-with-pagination pattern.

---

## 11. Styling

Tailwind, with semantic tokens defined once in `globals.css` (e.g. `--color-danger`, `--color-surface`) — components reference the semantic token, never a raw Tailwind color primitive directly. This is what let `callibrator` re-skin per-tenant without touching component code; RideCircle doesn't need multi-tenant theming at MVP, but the discipline still pays off for dark-mode support and any future rebrand.

No CSS-in-JS. No component-scoped stylesheets except where a third-party library requires one.

`--color-danger` (or equivalent) is reserved for destructive actions only (delete post, suspend rider) — never reused for merely "important" or "warning" UI, so its meaning stays reliable at a glance in a moderation context where that distinction matters.

---

## 12. Accessibility

Semantic HTML first, ARIA second. Every control labelled, every focus state visible, `prefers-reduced-motion` honored (relevant specifically for the landing page's `framer-motion` sections). Run `axe` (or equivalent) in the component test suite — not optional, per `callibrator/docs/FRONTEND/00-FRONTEND-STANDARDS.md`'s same rule.

---

## 13. Testing Standards

| Layer | Tool | Covers |
|---|---|---|
| Component | Jest + React Testing Library | Landing sections render correctly; admin screens render loading/empty/error/success states correctly |
| Service contract | Jest | Each `*.service.ts` has a matching `*.service.test.ts` asserting exact path, method, payload shape, and envelope unwrap (§4) |
| Manual | — | At least one real (non-mocked) call per admin service against a locally running `backend/`, before considering a `TASKS/PHASE-3-WEB.md` task done |

---

## 14. Git & Commit Conventions

Follow `TASKS/00-TASK-CONVENTIONS.md` exactly:

- Branch: `feat/T3-04-reports-queue-screen`
- Commit subject: `T3-04: implement admin reports queue screen`
- PR body: task ID, `docs/` sections implemented, test layers added/run, any deviation with its ADR link.
