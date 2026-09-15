# MVP Scope

**Folder:** `47-ROADMAP — Roadmap`
**Status:** MVP — dokumen paling penting untuk dibaca sebelum mulai coding

## Satu kalimat

**MVP = Ride Tracking + Social Media Share. Titik.**

## In scope (daftar final)

- Auth: register/login email+password, OAuth Google, logout, reset password
- Rider profile: nama, foto, bio, statistik dasar
- Ride recording: start/pause/resume/stop, background tracking, ringkasan metrik
- Ride history: list & detail ride milik sendiri, edit judul/visibility, hapus ride
- Ride analytics dasar: jarak, durasi, kecepatan rata-rata/maks, elevasi gain dasar
- Social feed: chronological, dari rider yang di-follow
- Follow/unfollow
- Publish/unpublish ride ke feed
- Kudos & komentar pada post
- Share card + native share sheet ke luar aplikasi
- Privacy dasar: visibility privat/publik per ride, default privat
- **Landing page** (web) — halaman publik untuk mengarahkan calon rider ke app store, ditambahkan sebagai prasyarat peluncuran produk (`docs/01-PRD/22-LANDING-PAGE.md`, `MEMORY/DECISIONS.md` ADR-008)
- **Admin moderation dashboard** (web) — laporan konten, hapus post/komentar, suspend rider, audit log — ditambahkan karena feed publik butuh jalur moderasi sejak hari pertama (`docs/01-PRD/21-ADMIN-MODERATION.md`, ADR-008)

## Eksplisit di luar scope (lihat `00-PRODUCT/05-NON-GOALS.md` untuk daftar lengkap)

Motorcycle Profile, Route Planning/Discovery, Group Ride, Moto Club, Event, Challenge, Safety (SOS/crash detection/live sharing), Gamification, Monetization, Brand Partnership, AI, integrasi device eksternal, marketplace, messaging/DM, push notification (in-app notification saja).

## Cara membaca status di seluruh repo docs/

Setiap file di `docs/` punya baris `**Status:** MVP` atau `**Status:** Post-MVP` di bagian atas.

- **MVP** → harus diimplementasikan di rilis pertama, dokumennya sudah ditulis lengkap (requirement, edge case, model data).
- **Post-MVP** → placeholder/scaffold saja (kerangka kosong dengan judul & status), sengaja belum didetailkan. Jangan diimplementasikan sampai ada keputusan eksplisit untuk memulai fase berikutnya, dan jangan biarkan keberadaan file ini menggoda scope creep.

## Untuk agent coding (Claude Code, dsb)

Jika kamu sedang membaca ini sebagai AI coding agent: **hanya kerjakan task yang berasal dari dokumen berstatus MVP.** Jika diminta mengimplementasikan sesuatu dari dokumen Post-MVP, konfirmasi dulu ke user bahwa ini di luar scope MVP yang disepakati sebelum melanjutkan. Lihat juga `CLAUDE.md` dan `AGENTS.md` di root repo.

## Terkait

- `docs/00-PRODUCT/04-PRODUCT-SCOPE.md`
- `docs/00-PRODUCT/05-NON-GOALS.md`
- `docs/47-ROADMAP/00-ROADMAP.md`
