# Rider (Domain)

**Folder:** `07-DOMAIN — Domain Model`
**Status:** MVP

## Skema (MVP)

```
Rider
  id                    uuid, PK
  email                 string, unique
  password_hash         string, nullable (null jika daftar via OAuth)
  oauth_provider         enum(none, google), default none
  username              string, unique
  display_name          string
  avatar_url            string, nullable
  bio                   string, nullable, maks 160 char
  home_city             string, nullable
  email_verified_at     timestamp, nullable
  total_distance_km     decimal, default 0     -- denormalized, incremental update
  total_rides           integer, default 0     -- denormalized, incremental update
  total_duration_min    integer, default 0     -- denormalized, incremental update
  created_at            timestamp
  updated_at            timestamp
```

## Invariant

- `email` dan `username` harus unik case-insensitive.
- `total_distance_km`, `total_rides`, `total_duration_min` adalah agregat yang diupdate secara incremental setiap kali sebuah `Ride` milik rider tersebut berpindah status ke `completed` (lihat `16-RIDE/00-RIDE-LIFECYCLE.md`) — bukan dihitung ulang (`SUM`) setiap request, demi performa halaman profil.
- Statistik menghitung **semua** ride (termasuk privat) milik rider sendiri; hanya daftar ride yang ditampilkan ke publik yang difilter berdasarkan `visibility`.

## State terkait auth

`password_hash` nullable karena rider bisa mendaftar murni via Google OAuth tanpa pernah membuat password — dalam kasus ini `oauth_provider = google`. Rider seperti ini bisa menambahkan password nanti (opsional, di luar MVP) untuk login manual sebagai alternatif.

## Terkait

- `docs/01-PRD/01-AUTHENTICATION.md`
- `docs/01-PRD/02-RIDER-PROFILE.md`
- `docs/07-DOMAIN/15-SOCIAL-GRAPH.md`
