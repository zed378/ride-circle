# Ride Analytics (dasar)

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — versi dasar saja; analitik lanjutan ada di `17-RIDER-PERFORMANCE` (Post-MVP)

## Tujuan

Menyajikan ringkasan metrik yang dapat dipahami sekilas, dipakai di tiga tempat: halaman detail ride, share card, dan agregat statistik profil.

## Metrik yang dihitung (MVP)

| Metrik | Definisi | Sumber |
|---|---|---|
| Jarak (km) | Jumlah jarak antar titik GPS berurutan (haversine), setelah filtering | `13-GPS/07-DISTANCE-CALCULATION.md` |
| Durasi total | `finished_at - started_at` | timestamp ride |
| Riding time | Durasi total dikurangi akumulasi waktu pause | event pause/resume |
| Kecepatan rata-rata | Jarak ÷ riding time | turunan |
| Kecepatan maksimum | Nilai tertinggi dari kecepatan sesaat setelah filtering outlier | `13-GPS/06-SPEED-CALCULATION.md` |
| Elevasi gain (opsional) | Jumlah kenaikan elevasi positif antar titik, dengan smoothing dasar | GPS altitude, akurasi terbatas di MVP |

## Requirement fungsional

1. Metrik dihitung sekali saat ride di-`stop`, disimpan sebagai kolom teragregasi di record `Ride` (bukan dihitung ulang setiap kali dibuka, untuk performa).
2. Jika rider mengedit track (di luar scope MVP), metrik harus dihitung ulang — dicatat sebagai catatan desain untuk fase depan, tidak diimplementasikan sekarang.
3. Statistik agregat profil (`total_distance`, `total_rides`, `total_duration`) diupdate secara incremental setiap ride baru selesai — bukan full recompute setiap request.

## Non-functional

- Kecepatan maksimum tidak boleh ditampilkan sebagai angka mentah tanpa filtering — GPS jump bisa menghasilkan angka tidak masuk akal (misal 300 km/j). Nilai di atas ambang wajar (misal >220 km/j) di-cap/di-flag sebagai kemungkinan noise, bukan langsung ditampilkan sebagai personal best.

## Out of scope (MVP ini)

- Personal best per segmen/rute.
- Grafik kecepatan/elevasi interaktif per detik.
- Perbandingan performa antar ride.
- Estimasi konsumsi bahan bakar.

## Terkait

- `docs/13-GPS/06-SPEED-CALCULATION.md`
- `docs/13-GPS/07-DISTANCE-CALCULATION.md`
- `docs/24-SOCIAL/09-SHARE-CARD.md`
