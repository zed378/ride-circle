# Pause & Resume

**Folder:** `13-GPS — GPS & Location Engine`
**Status:** MVP

## Perilaku

| Aksi | Efek terhadap sampling | Efek terhadap track | Efek terhadap metrik |
|---|---|---|---|
| Pause (manual) | Sampling GPS dihentikan | Titik terakhir sebelum pause jadi penanda akhir segmen | `RidePauseEvent` baru dibuat (`paused_at` = now) |
| Resume | Sampling GPS dilanjutkan | Titik pertama setelah resume mulai segmen baru (disambung visual di peta sebagai garis lurus antar segmen, bukan garis GPS asli) | `RidePauseEvent` terkait diisi `resumed_at` = now |
| Stop saat masih paused | — | Track final = seluruh segmen sebelum pause terakhir | `riding_time_sec` dihitung sampai `paused_at` terakhir, bukan sampai `finished_at` |

## Auto-pause (opsional, MVP-lite)

Jika kecepatan terhitung < 2 km/j selama lebih dari 3 menit berturut-turut, tampilkan prompt "Sepertinya kamu berhenti — pause otomatis?" — rider harus konfirmasi (tidak auto-pause diam-diam tanpa notifikasi), untuk menghindari kejutan seperti riding time yang tiba-tiba lebih pendek dari ekspektasi rider.

## Perhitungan riding_time_sec

```
riding_time_sec = (finished_at - started_at) - Σ(resumed_at - paused_at) untuk semua RidePauseEvent
```

Jika ride di-stop saat status masih `paused` (rider lupa resume sebelum stop), `RidePauseEvent` terakhir dianggap `resumed_at = finished_at` untuk keperluan perhitungan (durasi pause terakhir dihitung sampai titik stop).

## Edge case yang perlu ditangani

- **Resume tanpa pause sebelumnya** — tidak mungkin terjadi jika state machine ride diimplementasikan dengan benar (lihat `16-RIDE/00-RIDE-LIFECYCLE.md`); validasi di backend agar transisi ilegal ditolak.
- **Pause berkali-kali berturut-turut tanpa resume** — dicegah oleh state machine (dari status `paused` hanya bisa ke `recording` via resume, atau ke `completed` via stop).
- **App di-kill paksa oleh OS saat status `recording`** — saat app dibuka kembali, tampilkan prompt untuk melanjutkan (resume) atau menganggap ride selesai di titik terakhir yang tersimpan lokal.

## Terkait

- `docs/16-RIDE/00-RIDE-LIFECYCLE.md`
- `docs/01-PRD/04-RIDE-RECORDING.md`
