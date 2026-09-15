# PRD Overview

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP

## Cakupan PRD untuk MVP

PRD MVP terdiri dari 9 dokumen berstatus MVP di folder ini. Sisanya (Route Discovery, Group Ride, Moto Club, Event, Challenge, Rider Safety, Motorcycle Gear, Garage, Recommendation, Notification, Admin Moderation) berstatus Post-MVP dan sudah di-scaffold sebagai placeholder.

| # | Dokumen | Kenapa masuk MVP |
|---|---|---|
| 01 | Authentication | Prasyarat semua fitur — ride dan post harus terikat akun |
| 02 | Rider Profile | Ditampilkan di feed, share card, dan halaman profil |
| 03 | Motorcycle Profile | **Post-MVP** — tetap di-scaffold, tidak dikerjakan |
| 04 | Ride Recording | Pilar Tracking |
| 05 | Ride History | Pilar Tracking |
| 06 | Ride Analytics | Ringkasan metrik dasar untuk detail ride & share card |
| 14 | Social Feed | Pilar Social Share |
| 15 | Comments & Kudos | Pilar Social Share |

## Alur pengguna inti (end-to-end MVP)

```
Register/Login
     ↓
Lengkapi profil dasar (nama, foto)
     ↓
Mulai rekam ride (GPS start)
     ↓
Riding... (pause/resume jika perlu)
     ↓
Stop ride → ringkasan metrik ditampilkan
     ↓
Rider pilih: simpan privat / publish ke feed
     ↓
(jika publish) → post muncul di feed follower
     ↓
Rider generate share card → bagikan via native share sheet
     ↓
Follower lain kasih kudos / komentar di post
```

## Definition of Done untuk MVP

MVP dianggap selesai ketika seorang rider baru dapat, tanpa bantuan:

1. Daftar akun dan login kembali.
2. Merekam satu ride dari start sampai selesai, termasuk pause/resume, dan melihat ringkasan (jarak, durasi, kecepatan rata-rata/maks) setelah selesai.
3. Melihat riwayat ride miliknya sendiri.
4. Mem-publish ride tersebut ke feed sebagai post.
5. Melihat feed berisi post dari rider yang dia follow, dan memberi kudos/komentar.
6. Membuat share card dari sebuah ride dan membagikannya keluar aplikasi.

## Terkait

- `docs/00-PRODUCT/04-PRODUCT-SCOPE.md`
- `docs/07-DOMAIN/00-DOMAIN-MODEL.md`
