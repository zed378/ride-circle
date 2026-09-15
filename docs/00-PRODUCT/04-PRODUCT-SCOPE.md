# Product Scope

**Folder:** `00-PRODUCT — Product Foundation`
**Status:** MVP

## Scope MVP (disepakati)

MVP RideCircle = **Ride Tracking** + **Social Media Share**. Tidak lebih, tidak kurang.

### 1. Ride Tracking

| In scope | Out of scope (MVP ini) |
|---|---|
| Start/pause/resume/stop rekaman GPS | Live location sharing ke orang lain (real-time) |
| Hitung jarak, kecepatan (rata-rata & maks), durasi, elevasi dasar | Map-matching presisi jalan / road snapping |
| Simpan track sebagai polyline + ringkasan metrik | Segment leaderboard (KOM/QOM-style) |
| Riwayat ride pribadi (list + detail) | Route planning / navigasi turn-by-turn |
| Rekaman berjalan di background (mobile) | Integrasi perangkat eksternal (Garmin, sensor Bluetooth) |
| Deteksi GPS drop dasar (buang lonjakan tidak wajar) | Deteksi kecelakaan / crash detection |

### 2. Social Media Share

| In scope | Out of scope (MVP ini) |
|---|---|
| Publish ride selesai sebagai post ke feed | Direct message / chat |
| Feed berisi post dari rider yang di-follow | Algoritma rekomendasi feed (masih chronological) |
| Follow / unfollow rider lain | Moto Club / group feed |
| Like ("kudos") dan komentar pada post | Mention (@rider) di komentar |
| Generate **share card** (gambar ringkasan ride) untuk dibagikan ke luar aplikasi | Deep integration API resmi ke Instagram/WhatsApp (share pakai native share sheet OS dulu) |
| Kontrol visibilitas dasar: publik / privat per ride | Custom audience (mis. "hanya follower tertentu") |

### Cross-cutting yang tetap masuk MVP (karena jadi prasyarat dua pilar di atas)

- **Authentication** — register/login (email + password, plus opsi OAuth Google) agar ride & post bisa terikat ke akun.
- **Rider Profile** — nama, foto, bio singkat, ringkasan statistik (total jarak, total ride) yang ditampilkan di profil dan di share card.
- **Ride Analytics dasar** — ringkasan metrik per ride yang tampil di halaman detail ride dan di share card (bukan analitik performa lanjutan seperti training load).

## Eksplisit di luar MVP

Semua 47 kategori dokumentasi di repo ini di-scaffold sebagai referensi arsitektur jangka panjang, tapi kategori berikut **tidak** dikerjakan sampai ada keputusan eksplisit untuk fase berikutnya:

Motorcycle Profile & Garage, Route Planning/Discovery, Group Ride, Moto Club, Event, Challenge, Safety Beacon/Crash Detection, Gamification, Monetization, Brand Partnership, AI features, third-party device integration, marketplace.

## Terkait

- `docs/00-PRODUCT/05-NON-GOALS.md`
- `docs/47-ROADMAP/01-MVP-SCOPE.md`
- `docs/01-PRD/00-PRD-OVERVIEW.md`
