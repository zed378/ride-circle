# Admin Moderation Dashboard

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — ditambahkan setelah keputusan untuk membangun web app (landing + admin), lihat `MEMORY/DECISIONS.md` ADR-008

## Kenapa ini masuk MVP (bukan Post-MVP seperti draf awal)

Begitu Social Media Share hidup (feed publik, komentar, rider bisa saling follow), tim butuh cara untuk menghapus post/komentar yang dilaporkan dan menonaktifkan akun bermasalah — tanpa ini, tim tidak punya jalan operasional untuk menangani penyalahgunaan sejak hari pertama rilis. Ini bukan fitur produk baru untuk rider, tapi prasyarat operasional untuk MVP yang sudah disepakati (Social Share) bisa dijalankan dengan aman.

## Siapa penggunanya

Tim internal RideCircle (bukan rider) — admin/moderator dengan akun terpisah dari akun rider biasa.

## User stories

- Sebagai admin, saya bisa login ke dashboard terpisah dari app rider.
- Sebagai admin, saya bisa melihat daftar laporan (reported post/comment/rider) yang masuk.
- Sebagai admin, saya bisa melihat detail sebuah post/komentar yang dilaporkan beserta konteksnya (siapa yang lapor, kapan, alasan).
- Sebagai admin, saya bisa menghapus post atau komentar yang melanggar.
- Sebagai admin, saya bisa menonaktifkan (suspend) akun rider.
- Sebagai admin, saya bisa melihat daftar rider (basic search by email/username) untuk investigasi.
- Sebagai admin, setiap aksi moderasi yang saya lakukan tercatat di audit log (siapa, kapan, aksi apa, terhadap apa).

## Requirement fungsional

1. **Login admin terpisah** — admin punya role (`AdminUser` model, terpisah dari `Rider`), tidak bisa login lewat endpoint auth rider biasa.
2. **Report** — rider bisa melaporkan post/komentar (tombol "Laporkan" di app mobile — ini menambah satu requirement kecil ke `docs/24-SOCIAL/`, dicatat sebagai gap di `TASKS/BACKLOG.md`). Report tersimpan sebagai `Report { targetType, targetId, reporterId, reason, status }`.
3. **Queue laporan** — dashboard menampilkan daftar `Report` berstatus `pending`, diurutkan terbaru dulu.
4. **Aksi moderasi**: hapus post/komentar (soft-delete, sama seperti mekanisme yang sudah ada di `docs/24-SOCIAL/`), suspend rider (`Rider.status = suspended` — field baru, rider yang di-suspend tidak bisa login).
5. **Audit log** — setiap aksi moderasi menulis baris ke `ModerationAuditLog { adminId, action, targetType, targetId, reason, createdAt }`. Ini tabel append-only, tidak pernah di-update/delete.
6. **Pencarian rider dasar** — cari by email atau username, lihat profil + statistik + riwayat laporan terhadap rider tersebut.

## Non-functional

- Semua endpoint admin (`/admin/v1/*`) terpisah dari endpoint rider (`/v1/*`), dengan middleware auth yang berbeda — bukan sekadar role-check di atas JWT rider yang sama, supaya tidak ada jalur di mana bug di auth rider tidak sengaja membocorkan akses admin.
- Rate limiting untuk aksi bulk (mis. suspend banyak akun sekaligus) — di luar scope MVP untuk fitur bulk-nya sendiri, tapi endpoint suspend individual harus tetap dilindungi audit log agar penyalahgunaan oleh admin sendiri juga terlihat.

## Out of scope (MVP ini)

- Automated moderation (deteksi otomatis konten melanggar) — lihat `docs/32-MODERATION/`, tetap Post-MVP.
- Role granular untuk admin (misal admin vs super-admin) — MVP cukup satu role admin.
- Appeal flow untuk rider yang di-suspend (rider yang merasa salah suspend menghubungi tim secara manual di luar sistem untuk MVP).

## Terkait

- `docs/24-SOCIAL/03-FEED.md`, `docs/24-SOCIAL/08-RIDE-POST.md` — konten yang dimoderasi
- `docs/32-MODERATION/` (Post-MVP) — otomasi lanjutan
- `web/docs/CODING_STANDARDS.md` — konvensi implementasi dashboard-nya
