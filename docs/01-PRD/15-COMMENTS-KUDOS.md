# Comments & Kudos

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — pilar utama #2 (Social Media Share)

## Tujuan

Bentuk interaksi paling dasar di feed: apresiasi cepat (kudos) dan diskusi ringan (komentar).

## User stories

- Sebagai rider, saya bisa memberi satu kudos per post (toggle on/off).
- Sebagai rider, saya bisa melihat siapa saja yang memberi kudos (daftar sederhana).
- Sebagai rider, saya bisa menulis komentar teks pada post.
- Sebagai rider, saya bisa menghapus komentar saya sendiri.
- Sebagai pemilik post, saya bisa menghapus komentar orang lain di post saya (moderasi dasar).
- Sebagai rider, saya mendapat notifikasi in-app saat post saya dapat kudos/komentar (lihat catatan notifikasi di bawah).

## Requirement fungsional

1. **Kudos** — satu rider hanya bisa kudos satu post satu kali (unique constraint rider_id+post_id). Toggle: tap lagi untuk membatalkan.
2. **Komentar** — teks bebas, maks 500 karakter, urut kronologis (bukan threaded/nested di MVP).
3. **Hapus komentar** — soft delete, boleh oleh penulis komentar atau pemilik post.
4. **Counter** — jumlah kudos dan komentar ditampilkan di card post pada feed (angka teragregasi, bukan render seluruh list setiap kali).

## Notifikasi (MVP-lite)

Notifikasi in-app dasar (bukan push notification — itu di `26-NOTIFICATION`, Post-MVP) saat:
- Post kita dapat kudos baru.
- Post kita dapat komentar baru.
- Seseorang mulai follow kita.

Ditampilkan sebagai badge count sederhana + list notifikasi, tanpa preferensi granular.

## Out of scope (MVP ini)

- Reaction selain kudos (love, haha, dst).
- Mention (@rider) di komentar.
- Reply berjenjang (threaded comments).
- Push notification (hanya in-app).

## Terkait

- `docs/24-SOCIAL/04-KUDOS.md`
- `docs/24-SOCIAL/05-COMMENT.md`
- `docs/26-NOTIFICATION/00-NOTIFICATION-MODEL.md` (Post-MVP, referensi arah)
