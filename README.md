# RideCircle — Documentation & Project Scaffold

Platform untuk merekam, menemukan, menjalankan, membagikan, dan mengelola perjalanan serta komunitas pengendara motor — dirancang motorcycle-native, bukan "Strava + ikon motor".

> **MVP saat ini = Ride Tracking + Social Media Share.** Baca `docs/47-ROADMAP/01-MVP-SCOPE.md` sebelum membaca apa pun lagi di repo ini.

## Struktur repo

Mengikuti konvensi `TASKS/`+`MEMORY/`+`CLAUDE.md`+`AGENTS.md` yang sama dengan proyek [`zed-auth`](https://github.com/zed378/zed-auth) milik penulis — `docs/` = referensi (apa yang harus dibangun), `TASKS/` = rencana eksekusi (apa selanjutnya, bagaimana dinilai selesai), `MEMORY/` = catatan perubahan & keputusan (apa yang sudah terjadi, kenapa).

```
ridecircle-docs/
├── docs/                          48 folder kategori dokumentasi produk (00-47)
├── backend/
│   └── docs/CODING_STANDARDS.md   NestJS + TypeScript + Prisma, storage driver-agnostic (ADR-010, ADR-011)
├── android/
│   └── docs/CODING_STANDARDS.md   Kotlin + Jetpack Compose + MVVM (ADR-006)
├── ios/
│   └── docs/CODING_STANDARDS.md   Swift + SwiftUI + MVVM (ADR-006)
├── web/
│   └── docs/CODING_STANDARDS.md   Next.js — landing page + admin dashboard (ADR-008)
├── MEMORY/
│   ├── README.md                  cara pakai folder ini
│   ├── MEMORY-INDEX.md             satu baris per change record, terbaru di atas
│   ├── DECISIONS.md               ADR log — semua keputusan arsitektur
│   ├── CHANGELOG.md               ringkasan kronologis perubahan
│   ├── GLOSSARY.md                istilah domain RideCircle
│   ├── ARCHITECTURE-NOTES.md      catatan teknis informal, belum matang jadi ADR
│   ├── records/                   satu file per task yang sudah DONE
│   └── templates/                 template change record & phase summary
├── TASKS/
│   ├── README.md                  cara pakai folder ini
│   ├── 00-TASK-CONVENTIONS.md     skema task ID, status, Definition of Done
│   ├── PROGRESS.md                status board — satu tempat lihat progres
│   ├── PHASE-0-FOUNDATION.md      12 task: setup repo, tech stack, skema DB, storage
│   ├── PHASE-1-MVP-TRACKING.md    14 task: GPS, ride recording, history
│   ├── PHASE-2-MVP-SOCIAL-SHARE.md 12 task: auth, feed, kudos, share card
│   ├── PHASE-3-WEB.md             8 task: landing page + admin moderation dashboard
│   ├── specs/T3-02-landing-page.md  brief desain lengkap (di-paste user) — T3-02 BLOCKED, lihat OQ-09
│   └── BACKLOG.md                 pertanyaan terbuka & item yang ditunda
├── CLAUDE.md                      instruksi kerja untuk Claude Code
├── AGENTS.md                      instruksi setara untuk AI coding agent lain
└── README.md                      file ini
```

## Mulai dari sini

Urutan baca yang disarankan untuk siapa pun (manusia atau AI agent) yang baru bergabung ke proyek ini:

1. `docs/00-PRODUCT/00-PRODUCT-VISION.md` — visi jangka panjang
2. `docs/47-ROADMAP/01-MVP-SCOPE.md` — **batas scope yang berlaku sekarang**
3. `docs/00-PRODUCT/05-NON-GOALS.md` — apa yang sengaja TIDAK dibangun dulu
4. `docs/07-DOMAIN/00-DOMAIN-MODEL.md` — model data inti
5. `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md` — arsitektur & tech stack (**sudah di-freeze** — Android/Kotlin native, iOS/Swift native, web Next.js, backend NestJS/TypeScript dengan storage driver-agnostic (default disk lokal), lihat `MEMORY/DECISIONS.md` ADR-006, ADR-008, ADR-010, ADR-011)
6. `backend/docs/CODING_STANDARDS.md`, `android/docs/CODING_STANDARDS.md`, `ios/docs/CODING_STANDARDS.md`, `web/docs/CODING_STANDARDS.md` — konvensi coding per platform
7. `TASKS/PROGRESS.md` — status board, mulai kerja dari sini
8. `MEMORY/DECISIONS.md` § Decisions Pending — hal yang masih perlu diputuskan sebelum sebagian task bisa jalan

## Status dokumen

Setiap file di `docs/` punya penanda `**Status:** MVP` atau `**Status:** Post-MVP` di bagian atas.

- **MVP** (57 file ditandai) — 31 di antaranya sudah ditulis lengkap (requirement, skema data, edge case): Authentication, Rider Profile, Ride Recording/History/Analytics, GPS engine (sampling/speed/distance/pause-resume), Ride lifecycle & sharing, Social feed/graph, Comments & Kudos, Share Card, Location compliance, Roadmap. Sisanya (26 file, seluruhnya di folder `13-GPS`, `16-RIDE`, `24-SOCIAL`) ditandai MVP karena folder-nya masuk pilar Tracking/Social Share, tapi isinya masih stub template — perlu didetailkan sebelum sprint dimulai.
- **Post-MVP** (358 file) — placeholder/scaffold untuk referensi arah arsitektur jangka panjang (Motorcycle identity, Moto Club, Group Ride, Safety, Route Discovery, Event, Challenge, Gamification, Monetization, Brand Partnership, AI, dst). **Belum untuk diimplementasikan** — lihat `docs/47-ROADMAP/00-ROADMAP.md` untuk urutan fase berikutnya.

## Index 47 kategori dokumentasi

```
00-PRODUCT            01-PRD                02-BUSINESS           03-MARKET
04-USER-RESEARCH      05-UX                 06-UI                 07-DOMAIN
08-ARCHITECTURE       09-MOBILE             10-BACKEND            11-API
12-DATA               13-GPS                14-MAP                15-ROUTE
16-RIDE               17-RIDER-PERFORMANCE  18-MOTORCYCLE         19-COMMUNITY
20-GROUP-RIDE         21-EVENT              22-CHALLENGE          23-SAFETY
24-SOCIAL             25-MESSAGING          26-NOTIFICATION       27-GAMIFICATION
28-MONETIZATION       29-BRAND-PARTNERSHIP  30-PRIVACY            31-SECURITY
32-MODERATION         33-ANTI-ABUSE         34-ANALYTICS          35-SEARCH
36-RECOMMENDATION     37-AI                 38-INTEGRATION        39-DEVELOPER
40-OBSERVABILITY      41-PERFORMANCE        42-SCALABILITY        43-DEVOPS
44-TESTING            45-COMPLIANCE         46-RELEASE            47-ROADMAP
```

## Status eksekusi saat ini

**1 / 46 task selesai.** Tech stack sudah di-freeze (`T0-01`, ADR-006 + ADR-008 + ADR-010 + ADR-011); `docs/` dan coding standards empat platform (backend, Android, iOS, web) sudah lengkap sebagai scaffold; belum ada baris kode aplikasi yang ditulis. Lihat `TASKS/PROGRESS.md` untuk detail per task, `MEMORY/CHANGELOG.md` untuk ringkasan histori.

## Untuk AI coding agent

Baca `CLAUDE.md` (jika menggunakan Claude Code) atau `AGENTS.md` (agent lain) sebelum mulai bekerja di repo ini. Aturan intinya sama: **kerjakan hanya task yang berasal dari dokumen berstatus MVP, ikuti `TASKS/00-TASK-CONVENTIONS.md`, tulis MEMORY record sebelum menandai task DONE, dan konfirmasi ke user sebelum menyentuh apa pun yang berstatus Post-MVP atau item di `TASKS/BACKLOG.md` / `MEMORY/DECISIONS.md` § Decisions Pending.**

---

*Dokumentasi ini di-generate dari brief rekomendasi struktur dokumentasi produk motorcycle-native, dipersempit ke scope MVP (Ride Tracking + Social Media Share) sesuai keputusan produk. Struktur `TASKS/`/`MEMORY/`/`CLAUDE.md`/`AGENTS.md` mengikuti konvensi dari repo `zed-auth` milik penulis.*
