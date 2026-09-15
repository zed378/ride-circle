# Landing Page

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — ditambahkan setelah keputusan untuk membangun web app (landing + admin), lihat `MEMORY/DECISIONS.md` ADR-008

## Tujuan

Halaman publik (bukan app) yang menjelaskan RideCircle ke calon rider dan mengarahkan mereka untuk download aplikasi — kebutuhan dasar untuk bisa meluncurkan produk sama sekali (tidak ada cara lain bagi orang menemukan aplikasi selain lewat app store langsung).

## User stories

- Sebagai calon rider, saya bisa membuka website dan memahami apa itu RideCircle dalam beberapa detik.
- Sebagai calon rider, saya bisa menemukan tombol download untuk App Store / Play Store.
- Sebagai calon rider, saya bisa melihat sekilas fitur utama (rekam ride, bagikan ke feed).
- Sebagai tim, saya punya satu halaman yang bisa dibagikan di media sosial/press dengan preview (OG image) yang layak.

## Requirement fungsional (MVP)

1. **Hero section** — judul singkat, satu kalimat penjelas, tombol download (dua tombol: App Store, Play Store — link ke store listing masing-masing; jika app belum live di store, link ke halaman "coming soon"/waitlist).
2. **Fitur singkat** — 3-4 kartu fitur (Rekam ride, Lihat riwayat, Bagikan ke feed, Share card ke medsos) — bahasa sama dengan yang dipakai di `docs/00-PRODUCT/00-PRODUCT-VISION.md`, bukan istilah baru.
3. **Screenshot/preview app** — gambar statis (bukan live demo) dari layar recording/feed/share card.
4. **Footer** — link privacy policy, terms, kontak.
5. **SEO dasar** — meta title/description, Open Graph image, sitemap.xml, robots.txt.
6. **Statis / server-rendered** — tidak butuh data dinamis dari backend untuk MVP (tidak ada live stats "X rider sudah bergabung" di versi pertama — itu butuh endpoint publik baru yang tidak ada alasan kuat untuk MVP).

## Non-functional

- Lighthouse performance score tinggi (halaman ringan, sebagian besar statis) — halaman ini adalah first impression, lambat = calon rider pergi sebelum paham produknya.
- Accessible (kontras warna, alt text gambar, navigasi keyboard) — sama seperti standar aksesibilitas yang dipakai di `web/docs/CODING_STANDARDS.md`.

## Out of scope (MVP ini)

- Blog / content marketing.
- Halaman dokumentasi publik (API docs, dsb — tidak relevan, RideCircle bukan platform developer di MVP).
- Live counter/statistik dinamis dari backend.
- Waitlist form dengan database sendiri (kalau dibutuhkan, cukup embed form pihak ketiga seperti Google Form untuk MVP, jangan bangun sistem waitlist sendiri).

## Terkait

- `docs/00-PRODUCT/00-PRODUCT-VISION.md`, `docs/00-PRODUCT/06-VALUE-PROPOSITION.md` — sumber copy
- `web/docs/CODING_STANDARDS.md` — konvensi implementasi
- `TASKS/specs/T3-02-landing-page.md` — brief desain/implementasi lengkap (copy per section, warna, tipografi, motion, kebijakan aset gambar) untuk `T3-02`/`T3-03`. **Berisi konflik nama produk yang belum diselesaikan (RIDELINE vs RideCircle) — lihat `TASKS/BACKLOG.md` OQ-09 sebelum implementasi dimulai.**
