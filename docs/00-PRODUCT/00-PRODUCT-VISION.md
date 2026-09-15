# Product Vision

**Folder:** `00-PRODUCT — Product Foundation`
**Status:** MVP

## Pernyataan Visi

> Platform untuk merekam, menemukan, menjalankan, membagikan, dan mengelola perjalanan serta komunitas pengendara motor.

RideCircle bukan "Strava versi motor". Ia dirancang dari domain model yang motorcycle-native sejak awal: Ride, Rider, Motorcycle, Moto Club, Group Ride, Route, Safety — bukan Activity/Athlete generik yang dipaksakan ke konteks motor.

## Kenapa sekarang

Komunitas motor di Indonesia (dan banyak negara lain) sudah punya perilaku sosial yang kuat — grup WhatsApp, konvoi, touring, klub daerah — tapi belum punya satu platform yang menyatukan **tracking perjalanan** dan **berbagi cerita perjalanan itu** secara native untuk motor. Strava dan aplikasi sejenis dibangun untuk lari/sepeda dan tidak menangani kebutuhan spesifik motor (jarak tempuh jauh, multi-hari, grup besar, keselamatan berkendara, identitas motor).

## Lingkup fase ini (MVP)

Dokumen ini adalah visi jangka panjang. **Untuk rilis pertama, scope dipersempit secara sengaja menjadi dua pilar:**

1. **Ride Tracking** — rekam perjalanan motor (GPS, jarak, kecepatan, durasi, rute) dari mulai sampai selesai.
2. **Social Media Share** — bagikan ride yang sudah selesai sebagai post ke feed, lengkap dengan share card yang bisa disebar ke luar aplikasi (WhatsApp, Instagram Story, dll).

Semua pilar lain di visi ini (Moto Club, Group Ride, Safety Beacon, Marketplace, AI Assistant, dsb) **didokumentasikan sebagai placeholder** di `docs/` agar arsitektur tidak buntu saat pilar-pilar itu ditambahkan nanti, tapi **tidak dibangun di MVP**. Lihat `docs/47-ROADMAP/01-MVP-SCOPE.md` untuk batas scope yang eksplisit.

## Diferensiasi jangka panjang (di luar MVP, sebagai konteks arah)

Empat pilar yang akan membedakan RideCircle dari sekadar "Strava + ikon motor" setelah MVP:

- Group Ride + live member tracking
- Safety (crash detection, SOS, emergency escalation)
- Motorcycle sebagai identity layer (bukan cuma metadata)
- Route discovery yang motorcycle-native (scenic, twisty, fuel planning)

Dokumen di domain-domain tersebut (`19-COMMUNITY`, `20-GROUP-RIDE`, `23-SAFETY`, `18-MOTORCYCLE`, `15-ROUTE`, dst) sudah di-scaffold di repo ini sebagai referensi arah, berstatus Post-MVP.

## Terkait

- `docs/00-PRODUCT/04-PRODUCT-SCOPE.md`
- `docs/00-PRODUCT/05-NON-GOALS.md`
- `docs/47-ROADMAP/01-MVP-SCOPE.md`
