# Location Data (Compliance)

**Folder:** `45-COMPLIANCE — Compliance`
**Status:** MVP — wajib dipikirkan sejak awal karena core product adalah tracking lokasi

## Kenapa ini tidak bisa ditunda

RideCircle mengumpulkan data lokasi presisi tinggi (jejak GPS lengkap tiap ride) sejak fitur pertama (Ride Tracking). Ini kategori data sensitif di hampir semua regulasi privasi (GDPR, dan regulasi lokal seperti UU PDP di Indonesia) — tidak bisa diperlakukan sama seperti data non-sensitif.

## Prinsip MVP

1. **Consent eksplisit saat pertama kali meminta izin lokasi** — jelaskan di layar (bukan hanya dialog permission OS generik) kenapa lokasi dibutuhkan, sebelum memicu prompt permission OS.
2. **Default visibility = privat.** Ride baru selalu `private` secara default; rider harus secara aktif memilih publish. Ini prinsip "privacy by default", bukan opt-out.
3. **Data lokasi tidak dibagikan ke pihak ketiga** di MVP (tidak ada iklan berbasis lokasi, tidak ada penjualan data lokasi — itu topik B2B data Post-MVP yang perlu proses consent terpisah jika pernah dilakukan).
4. **Titik start/finish yang sensitif** — untuk ride publik, pertimbangkan menyembunyikan ~200m pertama & terakhir dari track yang ditampilkan ke publik (privacy zone di sekitar rumah rider), meski jarak/durasi tetap dihitung dari data lengkap. *(Catatan: fitur privacy zone ini idealnya ada di MVP karena risikonya nyata — rider publik yang share ride dari rumah ke kantor secara tidak sengaja membocorkan alamat rumah. Direkomendasikan masuk MVP meski tidak eksplisit disebut di brief awal — flag sebagai keputusan produk yang perlu dikonfirmasi.)*

## Retensi & penghapusan

- Ride yang di-soft-delete: raw GPS points tetap ada 30 hari (untuk recovery), lalu dihapus permanen dari storage (driver apa pun yang dipakai — disk lokal atau S3-compatible).
- Penghapusan akun (di luar scope MVP untuk dibangun, tapi harus dirancang agar memungkinkan): semua data lokasi milik rider tersebut harus bisa dihapus permanen.

## Out of scope (MVP ini, tapi wajib dicatat sebagai utang desain)

- Data Processing Agreement formal dengan vendor cloud/storage.
- Data residency requirement spesifik region.
- Automated data subject access request (DSAR) tooling.

## Terkait

- `docs/13-GPS/00-GPS-ARCHITECTURE.md`
- `docs/01-PRD/05-RIDE-HISTORY.md`
- `docs/30-PRIVACY/00-PRIVACY-MODEL.md` (Post-MVP, referensi lebih luas)
