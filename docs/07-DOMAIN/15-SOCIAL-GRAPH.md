# Social Graph (Domain)

**Folder:** `07-DOMAIN — Domain Model`
**Status:** MVP (Follow, Kudos, Comment) — graph yang diperluas (Brand, Dealer, Club) Post-MVP

## Skema (MVP)

```
Follow
  id            uuid, PK
  follower_id   uuid, FK → Rider
  followee_id   uuid, FK → Rider
  created_at    timestamp
  UNIQUE(follower_id, followee_id)
  CHECK(follower_id != followee_id)

Post
  id            uuid, PK
  rider_id      uuid, FK → Rider
  ride_id       uuid, FK → Ride, unique
  caption       string, nullable, maks 300 char
  published_at  timestamp
  deleted_at    timestamp, nullable

Kudos
  id            uuid, PK
  rider_id      uuid, FK → Rider
  post_id       uuid, FK → Post
  created_at    timestamp
  UNIQUE(rider_id, post_id)

Comment
  id            uuid, PK
  rider_id      uuid, FK → Rider
  post_id       uuid, FK → Post
  text          string, maks 500 char
  created_at    timestamp
  deleted_at    timestamp, nullable
```

## Model graph MVP: sederhana, satu arah

Di MVP, social graph hanya `Rider —follows→ Rider`. Model jangka panjang (lihat dokumen asli rekomendasi struktur) membayangkan graph yang jauh lebih kaya:

```
Rider ↔ Motorcycle ↔ Club ↔ Brand ↔ Dealer ↔ Workshop ↔ Event ↔ Route ↔ Destination
```

Node-node selain Rider ini **tidak** dibangun di MVP. Skema di atas sengaja tidak mengantisipasi mereka secara prematur (tidak ada tabel kosong untuk Club/Brand dll) — akan didesain ulang saat fase itu benar-benar dikerjakan, mengacu ke dokumen Post-MVP terkait (`19-COMMUNITY`, `29-BRAND-PARTNERSHIP`).

## Invariant

- `Follow` tidak bisa self-follow (`follower_id != followee_id`), dicegah di level database (CHECK constraint) dan aplikasi.
- `Post.ride_id` unik — satu ride hanya boleh dipublish sekali. Rider yang ingin "publish ulang" harus unpublish dulu (hapus Post), lalu publish lagi (buat Post baru) — histori kudos/komentar lama hilang, ini disengaja untuk MVP demi kesederhanaan.
- Menghapus `Rider` (jika ada fitur delete account, di luar MVP) harus mempertimbangkan cascade ke seluruh graph ini — didokumentasikan di `45-COMPLIANCE/06-DATA-DELETION.md` (Post-MVP) sebagai catatan untuk nanti.

## Terkait

- `docs/24-SOCIAL/00-SOCIAL-GRAPH.md`
- `docs/01-PRD/14-SOCIAL-FEED.md`
- `docs/01-PRD/15-COMMENTS-KUDOS.md`
