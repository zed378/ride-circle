# Ride Recording

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP — pilar utama #1 (Tracking)

## Tujuan

Rider dapat merekam perjalanan motornya secara akurat dari titik berangkat sampai selesai, termasuk saat berhenti sejenak (isi bensin, istirahat), tanpa harus menjaga app tetap di foreground.

## User stories

- Sebagai rider, saya tekan "Mulai" sebelum berangkat dan app mulai merekam posisi GPS saya.
- Sebagai rider, saya bisa pause rekaman saat berhenti lama (misal istirahat) supaya waktu berhenti tidak dihitung sebagai riding time.
- Sebagai rider, saya bisa resume setelah pause.
- Sebagai rider, saya bisa tekan "Selesai" dan langsung melihat ringkasan ride (jarak, durasi, kecepatan).
- Sebagai rider, rekaman tetap jalan walau saya kunci layar HP atau pindah ke app lain.

## Requirement fungsional

1. **Start** — membuat `Ride` baru berstatus `recording`, mulai sampling GPS (lihat `13-GPS/01-LOCATION-SAMPLING.md`).
2. **Pause** — hentikan sampling & akumulasi waktu, status jadi `paused`. Titik pause dicatat sebagai penanda di track (bukan dihapus).
3. **Resume** — lanjutkan sampling, status kembali `recording`. Segmen setelah pause disambung dengan segmen sebelumnya sebagai track yang sama, tapi gap waktu tidak dihitung ke riding time.
4. **Auto-pause (opsional, MVP-lite)** — jika kecepatan < 2 km/j selama > 3 menit berturut-turut, tawarkan pause otomatis (bukan paksa) untuk membantu rider yang lupa pause manual.
5. **Stop** — status jadi `completed`, hitung ringkasan akhir (lihat `17-RIDER-PERFORMANCE` untuk definisi metrik, meski folder itu sendiri Post-MVP — definisi dasar dipakai di sini juga).
6. **Background recording** — rekaman berjalan walau app di-background (lihat `09-MOBILE/03-BACKGROUND-TRACKING.md`, Post-MVP tapi requirement ini tetap berlaku untuk MVP karena krusial untuk use-case motor).
7. **Crash-safety data** — titik GPS ditulis ke local storage secara berkala (bukan hanya di memory), supaya kalau app crash pertengahan ride, data sampai titik terakhir tidak hilang total.

## Non-functional

- Sampling interval default: setiap 3–5 detik atau setiap pergerakan >10m (ambil yang lebih sering), untuk balance akurasi vs baterai (detail di `13-GPS`).
- Ride yang direkam < 500 meter atau < 2 menit ditandai sebagai "ride terlalu pendek" — tetap disimpan, tapi diberi prompt konfirmasi sebelum publish (mencegah post feed berisi noise).

## Out of scope (MVP ini)

- Multi-day ride (pause lintas hari) — MVP asumsikan satu ride = satu sesi dalam satu hari.
- Import ride dari GPX file pihak ketiga.
- Auto-detect jenis kendaraan (motor vs mobil).

## Terkait

- `docs/16-RIDE/00-RIDE-LIFECYCLE.md`
- `docs/13-GPS/00-GPS-ARCHITECTURE.md`
- `docs/01-PRD/05-RIDE-HISTORY.md`
