# Ride Lifecycle

**Folder:** `16-RIDE — Ride Lifecycle`
**Status:** MVP

## State machine

```
              start
   (none) ────────────► recording
                            │  │
                     pause  │  │ stop
                            ▼  ▼
                        paused  completed
                            │
                    resume  │
                            ▼
                        recording

   (recording|paused) ──discard──► discarded
```

## Definisi status

| Status | Arti |
|---|---|
| `recording` | Sampling GPS aktif, ride sedang berjalan |
| `paused` | Sampling GPS dihentikan sementara, ride belum selesai |
| `completed` | Ride selesai, metrik final terhitung, tidak bisa diedit track-nya (judul & visibility masih bisa) |
| `discarded` | Rider membatalkan ride sebelum selesai (misal salah pencet start) — tidak muncul di history, tidak terhitung ke statistik |

## Transisi & aturan

| Dari | Aksi | Ke | Syarat/efek |
|---|---|---|---|
| (tidak ada) | `start` | `recording` | Buat record `Ride` baru, `started_at = now` |
| `recording` | `pause` | `paused` | Buat `RidePauseEvent` |
| `paused` | `resume` | `recording` | Isi `resumed_at` pada `RidePauseEvent` terbuka |
| `recording` / `paused` | `stop` | `completed` | `finished_at = now`, hitung metrik (lihat `01-PRD/06-RIDE-ANALYTICS.md`), update statistik agregat `Rider` |
| `recording` / `paused` | `discard` | `discarded` | Tidak ada metrik dihitung, track dihapus (atau ditandai untuk cleanup) |

Transisi selain yang tercantum di atas (misal `completed → recording`) ditolak di level backend, bukan hanya dicegah di UI.

## Efek samping saat `completed`

1. Hitung `distance_km`, `duration_sec`, `riding_time_sec`, `avg_speed_kmh`, `max_speed_kmh`, `elevation_gain_m`.
2. Update `Rider.total_distance_km`, `total_rides`, `total_duration_min` secara incremental.
3. Ride dengan jarak < 500m atau durasi < 2 menit ditandai `is_short_ride = true` — tetap `completed`, tapi UI menampilkan prompt konfirmasi sebelum rider mem-publish-nya sebagai post (mencegah feed dipenuhi ride yang sangat pendek/tidak sengaja).

## Terkait

- `docs/07-DOMAIN/03-RIDE.md`
- `docs/13-GPS/09-PAUSE-RESUME.md`
- `docs/16-RIDE/02-RIDE-RECORDING.md`
