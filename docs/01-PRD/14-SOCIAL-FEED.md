# Social Feed

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — pilar utama #2 (Social Media Share)

## Tujuan

Rider dapat melihat ride yang di-publish oleh rider lain yang mereka follow, dalam satu feed kronologis, dan berinteraksi dasar (kudos + komentar).

## User stories

- Sebagai rider, saya melihat feed berisi post ride dari rider yang saya follow, terbaru di atas.
- Sebagai rider, saya bisa memberi kudos (like) pada sebuah post.
- Sebagai rider, saya bisa menulis komentar pada sebuah post.
- Sebagai rider, saya bisa follow/unfollow rider lain dari profil mereka atau dari post di feed.
- Sebagai rider, saya bisa membuka post untuk melihat detail ride lengkap.

## Requirement fungsional

1. Publish ride ke feed = membuat `Post` yang mereferensikan `Ride` tertentu (lihat `07-DOMAIN/03-RIDE.md`). Satu ride hanya bisa jadi satu post.
2. Feed adalah **chronological**, bukan algoritmik, di MVP — urut `published_at` descending dari rider yang di-follow + post milik sendiri.
3. Follow bersifat satu arah (seperti Instagram/Strava), tidak butuh persetujuan (public account model di MVP — tidak ada akun privat).
4. Unpublish (set ride kembali ke privat) menghapus post dari feed semua follower.
5. Pagination: load 20 post per halaman, infinite scroll.
6. Post yang dihapus pemiliknya (ride dihapus) otomatis hilang dari feed beserta seluruh kudos/komentarnya.

## Non-functional

- Feed harus tetap responsif untuk rider yang follow ratusan orang — gunakan fan-out sederhana (query gabungan berdasarkan daftar following, dengan index pada `published_at`) di MVP; fan-out-on-write untuk skala besar didokumentasikan sebagai catatan arsitektur masa depan di `10-BACKEND`, tidak diimplementasikan di MVP.

## Out of scope (MVP ini)

- Algoritma ranking/rekomendasi feed.
- Akun privat / approval follow.
- Mute/block rider.
- Feed berbasis lokasi atau klub (karena klub belum ada).

## Terkait

- `docs/24-SOCIAL/03-FEED.md`
- `docs/24-SOCIAL/00-SOCIAL-GRAPH.md`
- `docs/01-PRD/15-COMMENTS-KUDOS.md`
