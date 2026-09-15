# Share Card

**Folder:** `24-SOCIAL — Social`
**Status:** MVP — komponen kunci pilar Social Media Share

## Tujuan

Menghasilkan satu gambar (image) ringkasan ride yang dirancang untuk dibagikan ke luar aplikasi (WhatsApp, Instagram Story/Feed, dll) via native share sheet OS — bukan hanya screenshot manual.

## Konten share card (MVP)

- Peta rute (static image dari polyline, dengan styling brand)
- Judul ride
- Jarak, durasi, kecepatan rata-rata (3 metrik utama, besar & jelas terbaca)
- Nama & avatar rider kecil di pojok
- Logo/watermark RideCircle kecil di pojok (brand recall saat dibagikan ke luar app)

## Format & ukuran

| Varian | Rasio | Kegunaan |
|---|---|---|
| Story | 9:16 | Instagram/WhatsApp Story |
| Post | 1:1 | Feed Instagram, WhatsApp chat |

MVP cukup sediakan **satu varian** dulu (rekomendasi: 1:1, paling universal untuk chat & feed) — varian Story bisa ditambah cepat setelah MVP jika prioritas, tapi tidak wajib di rilis pertama.

## Alur teknis

1. Rider tekan "Buat Share Card" dari halaman detail ride.
2. Backend (atau client-side rendering, lihat catatan di bawah) generate image PNG/JPEG dari data ride + template.
3. Image di-cache (tidak di-generate ulang setiap kali dibuka untuk ride yang sama, kecuali data ride berubah).
4. Rider tekan "Bagikan" → panggil native share sheet OS (`Share` API React Native / `UIActivityViewController` iOS / `Intent.ACTION_SEND` Android) dengan image tersebut.

### Client-side vs server-side rendering

Rekomendasi MVP: **client-side rendering** (render langsung di device menggunakan komponen native/canvas dari data ride yang sudah ada di client) — lebih cepat untuk rider (tidak perlu round-trip ke server), dan menghindari kebutuhan infrastruktur image-generation di backend untuk MVP. Server-side rendering (misal untuk konsistensi cross-platform yang sempurna, atau watermark dinamis kompleks) adalah optimisasi Post-MVP jika dibutuhkan.

## Out of scope (MVP ini)

- Kustomisasi template/warna oleh rider.
- Integrasi API resmi Instagram/Strava-style "share to Instagram Stories" deep link khusus (cukup native share sheet umum dulu).
- Share card untuk Group Ride/Event (karena fitur tersebut belum ada).

## Terkait

- `docs/16-RIDE/08-RIDE-SHARING.md`
- `docs/01-PRD/06-RIDE-ANALYTICS.md`
- `docs/06-UI/04-MAP-UI.md` (Post-MVP folder, referensi styling peta)
