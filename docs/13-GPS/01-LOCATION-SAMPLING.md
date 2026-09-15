# Location Sampling

**Folder:** `13-GPS — GPS & Location Engine`
**Status:** MVP

## Strategi sampling (MVP)

| Parameter | Nilai default | Alasan |
|---|---|---|
| Interval waktu | setiap 3 detik | cukup rapat untuk motor (kecepatan tinggi, belokan tajam) tanpa boros baterai berlebihan |
| Jarak minimum | 10 meter (ambil titik baru jika sudah bergerak ≥10m sejak titik terakhir, walau interval waktu belum tercapai) | menangkap perubahan arah cepat di kecepatan tinggi |
| Akurasi minimum diterima | ≤ 20 meter (horizontal accuracy dari OS) | titik dengan akurasi lebih buruk dari ini dibuang, tidak dipakai untuk perhitungan jarak/kecepatan |
| Mode GPS | High accuracy (GPS + network, bukan hanya network-based) | dibutuhkan untuk kecepatan tinggi & area non-urban |

## Perilaku saat sinyal GPS lemah/hilang

1. Titik dengan akurasi > 20m tidak langsung dibuang total dari track kasar, tapi ditandai `low_confidence = true` dan **tidak dipakai** dalam perhitungan jarak/kecepatan (lihat `07-DISTANCE-CALCULATION.md`).
2. Jika tidak ada fix valid selama > 60 detik, tampilkan indikator "sinyal GPS lemah" di UI rekaman (tidak menghentikan rekaman).
3. Rekaman tetap berjalan (status tetap `recording`) selama GPS hilang — bukan otomatis pause. Auto-pause hanya berbasis kecepatan (lihat `01-PRD/04-RIDE-RECORDING.md`), bukan berbasis ketiadaan sinyal.

## Format titik yang disimpan lokal (per titik)

```
{
  ride_id, timestamp,
  lat, lng, altitude,
  accuracy_m, speed_mps (jika device menyediakan),
  low_confidence: boolean
}
```

## Out of scope (MVP ini)

- Adaptive sampling rate berdasarkan baterai (`13-BATTERY-OPTIMIZATION.md`, Post-MVP).
- GPS map-matching ke jaringan jalan (`05-GPS-MAP-MATCHING.md`, Post-MVP).
- Sensor fusion dengan accelerometer/gyroscope untuk dead-reckoning saat GPS hilang total.

## Terkait

- `docs/13-GPS/00-GPS-ARCHITECTURE.md`
- `docs/13-GPS/07-DISTANCE-CALCULATION.md`
- `docs/09-MOBILE/03-BACKGROUND-TRACKING.md` (Post-MVP, tapi requirement background tetap berlaku — lihat `01-PRD/04-RIDE-RECORDING.md`)
