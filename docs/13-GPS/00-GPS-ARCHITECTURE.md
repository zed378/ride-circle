# GPS Architecture

**Folder:** `13-GPS — GPS & Location Engine`
**Status:** MVP

## Alur data GPS (MVP)

```
Device GPS sensor
     │  raw fix (lat, lng, accuracy, altitude, speed, timestamp)
     ▼
Local sampling loop (mobile)          ← 13-GPS/01-LOCATION-SAMPLING.md
     │  filter fix buruk (accuracy > threshold dibuang)
     ▼
Local buffer (in-memory + periodic disk write)
     │  setiap N detik, tulis batch ke local DB (SQLite/Realm)
     ▼
[ride selesai / app kembali online]
     │
     ▼
Upload batch points ke backend
     │
     ▼
Backend: simplify + encode polyline  ← untuk Track.polyline
     │
     ├──► simpan polyline ringkas di PostgreSQL (Track)
     └──► simpan raw points lengkap di Storage — driver-agnostic, default disk lokal (untuk reproses/analitik masa depan)
     │
     ▼
Hitung ringkasan (distance, speed, elevation) → simpan ke Ride
```

## Kenapa upload di akhir, bukan streaming real-time (MVP)

Live tracking real-time (titik demi titik ke server saat riding) dibutuhkan untuk fitur seperti live location sharing di Group Ride — yang **tidak** ada di MVP. Untuk MVP, cukup: rekam lokal selama ride, upload batch saat ride selesai (atau saat koneksi tersedia jika sempat offline). Ini jauh lebih sederhana, lebih hemat baterai & data, dan cukup untuk kebutuhan Tracking + Share.

## Modul terkait di folder ini (status MVP)

- `01-LOCATION-SAMPLING.md` — interval & strategi sampling di device.
- `06-SPEED-CALCULATION.md` — turunan kecepatan dari titik GPS.
- `07-DISTANCE-CALCULATION.md` — akumulasi jarak.
- `09-PAUSE-RESUME.md` — bagaimana pause/resume memengaruhi track & metrik.

Modul lain di folder ini (map-matching, GPS smoothing lanjutan, GPS recovery kompleks, battery optimization mendalam) berstatus Post-MVP — MVP memakai pendekatan paling sederhana yang cukup akurat (filtering dasar, tanpa map-matching ke jalan).

## Terkait

- `docs/01-PRD/04-RIDE-RECORDING.md`
- `docs/07-DOMAIN/03-RIDE.md`
- `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md`
