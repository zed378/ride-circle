# Speed Calculation

**Folder:** `13-GPS — GPS & Location Engine`
**Status:** MVP

## Sumber kecepatan

Prioritaskan `speed` dari GPS fix device (biasanya lebih akurat, dihitung device dari Doppler shift) jika tersedia dan `accuracy` baik. Jika tidak tersedia, hitung dari turunan jarak/waktu antar dua titik berurutan:

```
speed_i (m/s) = distance(point_i-1, point_i) / (timestamp_i - timestamp_i-1)
```

## Filtering outlier (wajib, MVP)

GPS jump (loncatan posisi tidak wajar, umum terjadi di terowongan/gedung tinggi/multipath sinyal) dapat menghasilkan kecepatan sesaat yang mustahil. Aturan filtering MVP:

1. Buang titik dengan `low_confidence = true` (lihat `01-LOCATION-SAMPLING.md`) dari perhitungan kecepatan.
2. Kecepatan sesaat > 220 km/j dianggap noise, titik terkait diabaikan untuk perhitungan `max_speed_kmh` (tapi tidak dihapus dari track/polyline — hanya diabaikan untuk metrik kecepatan).
3. `max_speed_kmh` diambil dari nilai valid tertinggi setelah filtering di atas.
4. `avg_speed_kmh = distance_km / (riding_time_sec / 3600)` — dihitung dari total jarak dibagi riding time, **bukan** rata-rata aritmatik dari kecepatan sesaat (lebih akurat dan tidak sensitif terhadap noise per-titik).

## Kenapa cap di 220 km/j, bukan lebih rendah

Motor sport tertentu secara teknis bisa mendekati/lewat 300 km/j, tapi ini sangat jarang untuk konteks riding harian yang ditargetkan MVP. Angka 220 dipilih sebagai ambang konservatif untuk menyaring noise GPS tanpa terlalu agresif memotong kecepatan tinggi yang genuine. Nilai ini dikonfigurasi sebagai constant, bukan hardcoded di banyak tempat, supaya mudah disesuaikan.

## Out of scope (MVP ini)

- Kompensasi kecepatan berbasis map-matching (mengoreksi kecepatan berdasarkan batas kecepatan jalan).
- Grafik kecepatan interaktif per detik di UI.

## Terkait

- `docs/13-GPS/07-DISTANCE-CALCULATION.md`
- `docs/01-PRD/06-RIDE-ANALYTICS.md`
