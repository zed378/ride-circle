# Rider Profile

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP

## Tujuan

Setiap rider punya identitas publik minimal yang tampil di feed, komentar, dan share card.

## User stories

- Sebagai rider, saya bisa mengisi/mengedit nama tampilan, foto profil, dan bio singkat.
- Sebagai rider, saya bisa melihat profil rider lain (ringkasan statistik + daftar ride publik mereka).
- Sebagai rider, saya bisa melihat total statistik saya sendiri (total jarak, total ride, total waktu riding) di profil saya.

## Field profil (MVP)

| Field | Wajib | Catatan |
|---|---|---|
| display_name | Ya | 3–30 karakter |
| username | Ya | unik, dipakai di URL profil |
| avatar_url | Tidak | default avatar jika kosong |
| bio | Tidak | maks 160 karakter |
| home_city | Tidak | teks bebas, bukan geocoded (MVP) |
| joined_at | Otomatis | tanggal registrasi |
| stats_total_distance_km | Terhitung | agregat dari semua ride publik+privat milik sendiri |
| stats_total_rides | Terhitung | jumlah ride yang sudah completed |
| stats_total_duration_min | Terhitung | agregat durasi riding |

## Requirement fungsional

1. Edit profil (nama, foto, bio) dari halaman pengaturan.
2. Statistik dihitung dari ride milik sendiri yang berstatus `completed` (lihat `16-RIDE/00-RIDE-LIFECYCLE.md`), termasuk ride privat — statistik pribadi tetap menghitung ride privat, yang disembunyikan hanya ride itu sendiri dari publik.
3. Halaman profil publik hanya menampilkan ride yang visibility-nya `public`.
4. Username tidak bisa diganti lebih dari 1x per 30 hari (mencegah spoofing/impersonation berulang).

## Out of scope (MVP ini)

- Verifikasi identitas / badge terverifikasi.
- Custom cover photo.
- Statistik lanjutan (per bulan, per motor — motor belum ada di MVP).

## Terkait

- `docs/07-DOMAIN/01-RIDER.md`
- `docs/24-SOCIAL/00-SOCIAL-GRAPH.md`
