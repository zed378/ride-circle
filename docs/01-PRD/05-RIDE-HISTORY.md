# Ride History

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — pilar utama #1 (Tracking)

## Tujuan

Rider dapat melihat kembali semua ride yang pernah direkam, baik privat maupun publik, dalam satu tempat.

## User stories

- Sebagai rider, saya bisa melihat daftar semua ride saya, terbaru di atas.
- Sebagai rider, saya bisa membuka detail satu ride (peta rute, grafik kecepatan dasar, ringkasan metrik).
- Sebagai rider, saya bisa mengganti visibilitas ride (publik ↔ privat) setelah selesai direkam.
- Sebagai rider, saya bisa menghapus ride yang saya rekam.
- Sebagai rider, saya bisa mengganti judul ride (default: otomatis dari waktu/lokasi, misal "Pagi di Jakarta").

## Requirement fungsional

1. List ride: infinite scroll/pagination, urut `started_at` descending.
2. Tiap item list menampilkan: judul, tanggal, jarak, durasi, thumbnail peta rute (static image dari polyline).
3. Detail ride menampilkan: peta rute penuh, jarak, durasi, kecepatan rata-rata & maksimum, elevasi gain (jika tersedia), waktu mulai/selesai.
4. Edit judul & visibilitas dari halaman detail.
5. Hapus ride — konfirmasi dua langkah (destructive action), soft-delete di database (retensi 30 hari sebelum hard-delete, untuk recovery kalau salah hapus).
6. Ride yang sudah pernah di-publish ke feed dan kemudian diubah jadi privat: post di feed ikut disembunyikan (lihat `24-SOCIAL/03-FEED.md`).

## Non-functional

- List history harus tetap cepat dibuka walau rider punya ratusan ride (pagination dari awal, jangan load semua sekaligus).

## Out of scope (MVP ini)

- Filter/search history (by tanggal, jarak, motor).
- Kalender/heatmap tahunan ala Strava.
- Export ride ke GPX.

## Terkait

- `docs/16-RIDE/00-RIDE-LIFECYCLE.md`
- `docs/01-PRD/06-RIDE-ANALYTICS.md`
