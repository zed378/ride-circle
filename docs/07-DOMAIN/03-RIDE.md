# Ride (Domain)

**Folder:** `07-DOMAIN — Domain Model`
**Status:** MVP — entitas sentral pilar Tracking

## Skema (MVP)

```
Ride
  id                 uuid, PK
  rider_id           uuid, FK → Rider
  title              string                       -- default auto-generated, editable
  status             enum(recording, paused, completed, discarded)
  visibility         enum(private, public), default private
  started_at         timestamp
  finished_at        timestamp, nullable
  distance_km        decimal, nullable            -- computed saat completed
  duration_sec        integer, nullable            -- total durasi (started→finished)
  riding_time_sec     integer, nullable            -- duration_sec dikurangi total waktu pause
  avg_speed_kmh       decimal, nullable
  max_speed_kmh       decimal, nullable
  elevation_gain_m    decimal, nullable
  created_at          timestamp
  updated_at          timestamp
  deleted_at          timestamp, nullable          -- soft delete, retensi 30 hari

RidePauseEvent
  id            uuid, PK
  ride_id       uuid, FK → Ride
  paused_at     timestamp
  resumed_at    timestamp, nullable

Track
  id            uuid, PK
  ride_id       uuid, FK → Ride, unique
  polyline      text                                -- encoded polyline (Google polyline algorithm)
  point_count   integer
  raw_points_ref string, nullable                    -- storage key (bukan URL/path) untuk raw GPS points di storage driver-agnostic (bukan disimpan di RDBMS langsung, lihat 08-ARCHITECTURE)
```

## State machine

```
recording ──pause──► paused
recording ──stop───► completed
paused    ──resume─► recording
paused    ──stop───► completed
(recording|paused) ──discard──► discarded
```

Detail lengkap tiap transisi ada di `16-RIDE/00-RIDE-LIFECYCLE.md`.

## Invariant

- `distance_km`, `duration_sec`, `riding_time_sec`, `avg_speed_kmh`, `max_speed_kmh` hanya diisi (non-null) setelah status `completed`.
- `riding_time_sec = duration_sec - SUM(RidePauseEvent.resumed_at - RidePauseEvent.paused_at)`.
- Ride dengan status `discarded` tidak muncul di history maupun bisa di-publish.
- Satu `Ride` maksimum punya satu `Post` (relasi 1:1, lihat `24-SOCIAL/08-RIDE-POST.md`). Meng-unpublish = menghapus `Post`, bukan mengubah `Ride`.
- Menghapus `Ride` (soft delete) harus cascade menyembunyikan `Post` terkait (jika ada) dari feed.

## Terkait

- `docs/16-RIDE/00-RIDE-LIFECYCLE.md`
- `docs/13-GPS/00-GPS-ARCHITECTURE.md`
- `docs/01-PRD/06-RIDE-ANALYTICS.md`
