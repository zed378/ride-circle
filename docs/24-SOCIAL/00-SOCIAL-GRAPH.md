# Social Graph (Feature)

**Folder:** `24-SOCIAL — Social`
**Status:** MVP

Untuk skema data, lihat `07-DOMAIN/15-SOCIAL-GRAPH.md`. Dokumen ini fokus ke perilaku fitur yang terlihat rider.

## Follow

- Follow bersifat instan, satu arah, tanpa approval (semua profil bersifat publik di MVP — tidak ada akun privat).
- Rider bisa follow dari: halaman profil rider lain, atau langsung dari card post di feed (tombol follow di header post).
- Unfollow instan, tanpa konfirmasi tambahan.
- Tidak ada batas jumlah following/follower di MVP.

## Tampilan graph

- Halaman profil menampilkan jumlah **Following** dan **Followers** (angka), dengan list yang bisa dibuka (nama + avatar + tombol follow/unfollow cepat).
- Tidak ada rekomendasi "rider yang mungkin kamu kenal" di MVP (`36-RECOMMENDATION`, Post-MVP).

## Privasi dasar

- Semua rider yang punya akun dapat dilihat profilnya dan di-follow siapa saja (tidak ada akun privat/protected di MVP).
- Ride tetap mengikuti `visibility` masing-masing — follow tidak memberi akses ke ride privat orang lain.

## Out of scope (MVP ini)

- Block / mute.
- Akun privat (approve follower).
- Close friends / custom audience.
- Mutual friends indicator.

## Terkait

- `docs/07-DOMAIN/15-SOCIAL-GRAPH.md`
- `docs/01-PRD/02-RIDER-PROFILE.md`
- `docs/24-SOCIAL/03-FEED.md`
