# Ride Sharing

**Folder:** `16-RIDE — Ride Lifecycle`
**Status:** MVP — titik temu antara pilar Tracking dan pilar Social Share

## Alur

```
Ride (status = completed)
     │
     │  rider pilih "Publish"
     ▼
Post dibuat (rider_id, ride_id, caption opsional)
     │
     ├──► muncul di feed follower           → 24-SOCIAL/03-FEED.md
     └──► generate Share Card               → 24-SOCIAL/09-SHARE-CARD.md
                │
                ▼
        native OS share sheet
     (WhatsApp, Instagram Story, dll — di luar app)
```

## Dua jenis "share" yang berbeda (penting untuk tidak tercampur di implementasi)

1. **Publish ke feed (in-app)** — membuat `Post`, terlihat oleh follower di dalam RideCircle. Diatur di `01-PRD/14-SOCIAL-FEED.md`.
2. **Share keluar aplikasi (out-of-app)** — generate gambar share card dari sebuah ride (publik maupun privat — rider tetap boleh share ride privat ke luar tanpa mem-publish-nya ke feed in-app), lalu memanggil native share sheet OS. Ini **tidak** membuat `Post` dan tidak butuh ride berstatus publik.

Kedua alur ini independen: rider bisa publish ke feed tanpa share keluar, share keluar tanpa publish ke feed, atau keduanya.

## Requirement fungsional

1. Tombol "Publish" hanya muncul untuk ride berstatus `completed`.
2. Tombol "Share" (keluar aplikasi) tersedia untuk ride `completed` apa pun visibility-nya.
3. Publish mengubah `Ride.visibility` menjadi `public` secara otomatis jika sebelumnya `private` (rider tidak bisa publish post dari ride yang tetap privat — ini kontradiktif; UI perlu menjelaskan ini dengan jelas sebelum konfirmasi).
4. Unpublish (hapus Post) tidak otomatis mengubah `Ride.visibility` kembali ke privat — dua aksi terpisah, rider yang mengontrol keduanya secara eksplisit.

## Terkait

- `docs/24-SOCIAL/08-RIDE-POST.md`
- `docs/24-SOCIAL/09-SHARE-CARD.md`
- `docs/07-DOMAIN/03-RIDE.md`
