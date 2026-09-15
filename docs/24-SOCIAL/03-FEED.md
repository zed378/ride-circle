# Feed (Feature)

**Folder:** `24-SOCIAL — Social`
**Status:** MVP

## Query dasar (MVP)

```sql
SELECT posts.*
FROM posts
WHERE posts.rider_id IN (
    SELECT followee_id FROM follows WHERE follower_id = :current_rider_id
    UNION SELECT :current_rider_id            -- termasuk post milik sendiri
)
AND posts.deleted_at IS NULL
ORDER BY posts.published_at DESC
LIMIT 20 OFFSET :page * 20
```

Ini pendekatan **fan-out-on-read** — sengaja dipilih untuk MVP karena jauh lebih sederhana dari fan-out-on-write (precompute feed per rider saat post dibuat), dan cukup performan untuk skala awal (ribuan rider, ratusan following per rider). Migrasi ke fan-out-on-write adalah optimisasi Post-MVP jika/ketika dibutuhkan — dicatat sebagai catatan arsitektur, bukan dikerjakan sekarang.

## Isi tiap card post di feed

- Avatar + nama + username rider
- Waktu publish (relatif, misal "2 jam lalu")
- Judul ride + thumbnail peta rute (static image dari polyline)
- Ringkasan metrik: jarak, durasi, kecepatan rata-rata
- Caption (jika diisi)
- Jumlah kudos & komentar + tombol aksi kudos/komentar

## Requirement fungsional

1. Pull-to-refresh memuat post terbaru sejak load terakhir.
2. Infinite scroll untuk memuat post lebih lama.
3. Feed kosong (rider belum follow siapa pun) menampilkan empty state dengan ajakan mencari rider untuk di-follow.
4. Post yang ride-nya dihapus atau di-unpublish langsung hilang dari feed (tidak perlu refresh manual jika masih di sesi yang sama — realtime update di luar scope MVP, cukup hilang saat feed di-refresh berikutnya).

## Out of scope (MVP ini)

- Realtime update (websocket) saat ada post baru — rider perlu pull-to-refresh manual.
- Ranking algoritmik.
- Iklan/sponsored post di feed.

## Terkait

- `docs/01-PRD/14-SOCIAL-FEED.md`
- `docs/24-SOCIAL/08-RIDE-POST.md`
