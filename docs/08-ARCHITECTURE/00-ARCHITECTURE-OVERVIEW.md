# Architecture Overview (MVP)

**Folder:** `08-ARCHITECTURE — System Architecture`
**Status:** MVP

## Prinsip arsitektur MVP

Bangun sesederhana mungkin yang cukup untuk dua pilar (Tracking + Social Share), tapi jangan buat keputusan yang menutup jalan ke arsitektur jangka panjang (lihat diagram besar di README repo). Konkretnya:

- **Monolith dulu, bukan microservices.** Satu backend service untuk auth, ride, dan social. Pemisahan service (Ride Engine, Social Engine terpisah) adalah langkah Post-MVP ketika beban benar-benar membutuhkannya.
- **Dua platform native sejak awal, bukan cross-platform.** Android (Kotlin) dan iOS (Swift) dikerjakan sebagai dua codebase terpisah — keputusan final, lihat `MEMORY/DECISIONS.md` ADR-006. Alasan utamanya: background GPS recording butuh integrasi mendalam ke foreground service (Android) dan background location mode (iOS) yang paling baik ditangani native.
- **File storage untuk raw GPS points**, bukan disimpan sebagai ribuan baris di RDBMS per ride — simpan polyline teragregasi di RDBMS untuk query cepat, raw points (untuk kebutuhan reproses nanti) di storage. Storage bersifat **driver-agnostic**: default-nya disk lokal VM tempat backend berjalan, bisa diganti ke S3-compatible lewat konfigurasi tanpa migrasi database (DB hanya menyimpan *storage key*) — lihat `MEMORY/DECISIONS.md` ADR-011.

## Diagram komponen MVP

```
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────────────┐
│   Android App      │      │     iOS App         │      │      Web App (Next.js)      │
│   (Kotlin/Compose)  │      │   (Swift/SwiftUI)    │      │  Landing (public) + Admin   │
└─────────┬─────────┘      └─────────┬─────────┘      │      dashboard (/admin/*)   │
          │                          │                └──────────────┬───────────┘
          └───────────┬──────────────┘                               │
                       │ REST/HTTPS                                  │ REST/HTTPS
                       ▼                                             │
          ┌─────────────────────┐                                    │
          │   Backend (monolith)  │◄──────────────────────────────────┘
          │  ┌─────────────────┐  │
          │  │  Auth module     │  │
          │  ├─────────────────┤  │
          │  │  Ride module     │──┼──► Storage driver (raw GPS points, share card)
          │  │                  │  │    default: disk lokal VM · opsional: S3-compatible
          │  ├─────────────────┤  │
          │  │  Social module   │  │
          │  ├─────────────────┤  │
          │  │  Admin module    │  │  (moderation, audit log — docs/01-PRD/21-ADMIN-MODERATION.md)
          │  └─────────────────┘  │
          └──────────┬───────────┘
                      ▼
                ┌───────────┐      ┌───────┐
                │ PostgreSQL │      │ Redis  │
                │ (+PostGIS) │      │        │
                └───────────┘      └───────┘
```

The landing page portion of `web/` is mostly static/server-rendered and doesn't call the backend at all for MVP (`docs/01-PRD/22-LANDING-PAGE.md`) — the arrow above is really only exercised by `/admin/*`.

## Komponen yang SENGAJA tidak ada di MVP

- Search service terpisah (Elasticsearch dsb) — pencarian belum jadi fitur MVP.
- CDN khusus untuk share card image — bisa pakai storage publik + cache header dulu; CDN dedicated adalah optimisasi Post-MVP.
- Recommendation/AI service.

## Tech stack (frozen — lihat `MEMORY/DECISIONS.md` ADR-006, ADR-008, ADR-010, ADR-011)

| Layer | Keputusan | Catatan |
|---|---|---|
| Android | Kotlin, Jetpack Compose, MVVM | Native, bukan cross-platform — ADR-006 |
| iOS | Swift, SwiftUI, MVVM | Native, bukan cross-platform — ADR-006 |
| Web (landing + admin) | Next.js (App Router), React, TypeScript, Tailwind CSS, Zustand | Satu app untuk dua kebutuhan — ADR-008, meniru pola `callibrator/frontend` |
| Backend | Node.js + TypeScript + NestJS (adapter Express default) | Module + DI bawaan, guard/filter/interceptor global — ADR-010 (menggantikan pilihan Express di ADR-007) |
| ORM | Prisma | Bukan Sequelize seperti `callibrator` — TypeScript-first, lihat ADR-007/ADR-010 |
| Validasi | Zod (via `ZodValidationPipe`) | Berbagi tipe dengan TypeScript end-to-end; bukan class-validator — ADR-010 |
| Database | PostgreSQL + PostGIS extension | PostGIS aktif sejak awal meski MVP belum query geospasial kompleks |
| Cache/session | Redis | Rate limiting, refresh token |
| Background jobs | BullMQ (Redis-backed) | Polyline simplification, share card pre-render |
| Storage | Driver-agnostic (`StorageDriver`); default `local` = disk VM, `s3` (S3-compatible) opsional | Raw GPS points & share card image — ADR-011 |
| Auth | Custom JWT (access + refresh) | Bukan Auth0/Supabase Auth — tim sudah punya pengalaman ini di `callibrator` |

Detail konvensi coding per platform ada di:
- `backend/docs/CODING_STANDARDS.md`
- `android/docs/CODING_STANDARDS.md`
- `ios/docs/CODING_STANDARDS.md`
- `web/docs/CODING_STANDARDS.md`

## Terkait

- `docs/13-GPS/00-GPS-ARCHITECTURE.md`
- `docs/07-DOMAIN/00-DOMAIN-MODEL.md`
- `CLAUDE.md`
