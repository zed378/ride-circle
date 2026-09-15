# Ride Post (Feature)

**Folder:** `24-SOCIAL — Social`
**Status:** MVP

## Definisi

`Post` = representasi publik dari satu `Ride` yang dipilih rider untuk dibagikan ke follower-nya. Lihat skema di `07-DOMAIN/15-SOCIAL-GRAPH.md`.

## Alur pembuatan post

1. Rider membuka halaman detail ride (`completed`).
2. Tekan "Publish".
3. (Opsional) tulis caption, maks 300 karakter.
4. Konfirmasi — jika `Ride.visibility` masih `private`, tampilkan penjelasan bahwa publish akan membuat ride ini terlihat publik.
5. `Post` dibuat, `published_at = now`.

## Aturan tampilan post

- Post menampilkan data yang **dihitung sekali saat publish** dari ride terkait (judul, jarak, durasi, kecepatan) — jika data ride kemudian berubah (misal rider edit judul di halaman history), post **mengikuti** data ride terbaru secara live (post bukan snapshot terpisah, hanya referensi ke `ride_id`) kecuali caption yang memang milik post itu sendiri.
- Caption bisa diedit setelah publish tanpa membuat post baru.

## Unpublish

- Tombol "Unpublish" di halaman detail ride/post → soft-delete `Post` (`deleted_at = now`).
- Semua `Kudos` dan `Comment` pada post tersebut ikut tidak ditampilkan (tapi tidak dihapus permanen di MVP — retensi mengikuti kebijakan soft-delete ride yang sama, 30 hari).
- `Ride.visibility` **tidak** otomatis berubah saat unpublish (lihat catatan di `16-RIDE/08-RIDE-SHARING.md`).

## Terkait

- `docs/16-RIDE/08-RIDE-SHARING.md`
- `docs/24-SOCIAL/03-FEED.md`
- `docs/01-PRD/15-COMMENTS-KUDOS.md`
