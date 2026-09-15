# Domain Model

**Folder:** `07-DOMAIN — Domain Model`
**Status:** MVP (entitas inti) + Post-MVP (entitas lanjutan, ditandai)

## Prinsip

Domain model dirancang motorcycle-native dan dibuat cukup luas agar tidak perlu migrasi besar saat fitur Post-MVP (Motorcycle, Club, Group Ride, Event, Safety) ditambahkan — tapi **hanya entitas MVP yang diimplementasikan sekarang**.

## Entitas inti MVP

```
Rider
 ├── has_many → Ride
 ├── has_many → Post          (satu Post = satu Ride yang di-publish)
 ├── has_many → Follow (as follower)
 ├── has_many → Follow (as followee)
 ├── has_many → Kudos
 └── has_many → Comment

Ride
 ├── belongs_to → Rider
 ├── has_one   → Track        (polyline + raw GPS points)
 ├── has_one   → RideSummary  (jarak, durasi, kecepatan — computed)
 └── has_one   → Post         (opsional — hanya jika di-publish)

Post
 ├── belongs_to → Rider
 ├── belongs_to → Ride
 ├── has_many   → Kudos
 └── has_many   → Comment

Follow
 ├── belongs_to → Rider (follower_id)
 └── belongs_to → Rider (followee_id)

Kudos
 ├── belongs_to → Rider
 └── belongs_to → Post

Comment
 ├── belongs_to → Rider
 ├── belongs_to → Post
 └── text
```

## Entitas Post-MVP (referensi arah, belum diimplementasikan)

Motorcycle, Segment, RideGroup, Club, Event, Challenge, Location, Waypoint, Garage, Gear, SafetyContact, SocialGraph yang diperluas (Brand, Dealer, Workshop) — lihat dokumen masing-masing di folder ini, semua berstatus Post-MVP.

Relasi jangka panjang yang perlu diantisipasi di desain skema (tanpa membangunnya sekarang):

```
Rider
 ├── owns → Motorcycle        (Post-MVP)
 ├── joins → Club             (Post-MVP)
 ├── joins → Group Ride       (Post-MVP)
 ├── participates → Event     (Post-MVP)
 └── performs → Ride          (MVP)
                    │
                    ├── Route      (Post-MVP — MVP hanya simpan track mentah, belum ada Route sebagai entitas reusable)
                    ├── Segment    (Post-MVP)
                    └── Waypoints  (Post-MVP)
```

## Catatan desain untuk implementasi MVP

- `Ride.motorcycle_id` **tidak** dibuat di MVP (kolom nullable bisa disiapkan di skema untuk memudahkan migrasi nanti, tapi tidak ada UI/logic terkait).
- `Ride` MVP tidak mereferensikan `Route` sebagai entitas terpisah — track GPS disimpan langsung sebagai polyline milik ride itu sendiri. Ekstraksi `Route` sebagai entitas reusable (untuk fitur Route Discovery) adalah pekerjaan Post-MVP.

## Terkait

- `docs/07-DOMAIN/01-RIDER.md`
- `docs/07-DOMAIN/03-RIDE.md`
- `docs/07-DOMAIN/15-SOCIAL-GRAPH.md`
- `docs/08-ARCHITECTURE/00-ARCHITECTURE-OVERVIEW.md`
