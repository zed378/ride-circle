# Non-Goals (MVP)

**Folder:** `00-PRODUCT — Product Foundation`
**Status:** MVP

Daftar ini eksplisit menyatakan apa yang **tidak** sedang dibangun di fase MVP, supaya tim (dan agent coding) tidak diam-diam memperluas scope saat implementasi.

## Non-goals eksplisit

1. **Bukan navigasi.** RideCircle tidak menggantikan Google Maps/Waze untuk turn-by-turn navigation di MVP ini.
2. **Bukan platform keselamatan real-time.** Tidak ada crash detection, SOS, atau live location sharing ke kontak darurat di MVP. Ini domain besar (`23-SAFETY`) yang sengaja ditunda.
3. **Bukan platform komunitas/klub.** Tidak ada Moto Club, Group Ride, atau Event di MVP — hanya relasi follow satu-ke-satu antar rider.
4. **Bukan platform monetisasi.** Tidak ada subscription, sponsored content, atau marketplace di MVP. Semua fitur gratis.
5. **Bukan competitive/leaderboard platform.** Tidak ada segment, KOM/QOM, atau ranking publik di MVP — sengaja, untuk menghindari mendorong ngebut sebagai kompetisi (lihat catatan safety di `17-RIDER-PERFORMANCE`).
6. **Bukan integrasi perangkat.** Tidak ada dukungan Garmin, smartwatch, atau sensor Bluetooth eksternal di MVP — GPS dari HP saja.
7. **Bukan AI product.** Tidak ada AI ride summary, coaching, atau natural language query di MVP.
8. **Bukan tiga platform sekaligus di rilis pertama.** MVP membangun Android dan iOS native secara paralel (`MEMORY/DECISIONS.md` ADR-006), tapi bukan web app sekaligus — versi web ditunda sampai ada keputusan eksplisit.

## Kenapa ini penting

Dokumentasi asli yang jadi acuan proyek ini punya 47 kategori dan ratusan dokumen potensial. Tanpa non-goals yang eksplisit, risiko terbesar MVP ini adalah scope creep — tergoda membangun Group Ride atau Safety karena dokumennya "sudah ada" di repo. Semua dokumen di luar Tracking dan Social Share statusnya **Post-MVP** dan sengaja dibiarkan sebagai kerangka kosong.

## Terkait

- `docs/00-PRODUCT/04-PRODUCT-SCOPE.md`
- `docs/47-ROADMAP/01-MVP-SCOPE.md`
