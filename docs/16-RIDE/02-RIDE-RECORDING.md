# Ride Recording (Technical)

**Folder:** `16-RIDE — Ride Lifecycle`
**Status:** MVP

Dokumen ini adalah spesifikasi teknis pelengkap `01-PRD/04-RIDE-RECORDING.md` — PRD menjelaskan *apa* dan *kenapa*, dokumen ini menjelaskan *bagaimana*.

## Komponen mobile

```
RecordingService (background service / foreground service dengan notifikasi persisten)
  ├── LocationSampler         → 13-GPS/01-LOCATION-SAMPLING.md
  ├── LocalPointBuffer        → tulis batch ke local DB tiap ~10 detik
  ├── RideStateMachine        → 16-RIDE/00-RIDE-LIFECYCLE.md (state lokal, disinkronkan ke server saat online)
  └── UploadManager           → upload batch points saat ride completed & koneksi tersedia
```

## Kenapa foreground service dengan notifikasi persisten (Android) / background location (iOS)

Motor riding = layar terkunci, HP di holder/kantong, durasi bisa berjam-jam. OS (khususnya Android) akan mematikan background process yang tidak punya foreground service. Requirement ini **wajib** untuk MVP meski detail implementasi platform-spesifik didokumentasikan di `09-MOBILE` (Post-MVP folder, tapi requirement fungsionalnya tetap berlaku untuk MVP — lihat catatan di `01-PRD/04-RIDE-RECORDING.md`).

## Resilience

1. **App crash saat recording** — local buffer sudah tertulis ke disk secara periodik (bukan hanya in-memory), sehingga saat app dibuka kembali, ride bisa di-recover sampai titik terakhir yang tersimpan, ditawarkan opsi untuk menyelesaikan (stop) ride tersebut.
2. **Kehilangan koneksi internet saat ride** — tidak masalah, karena upload baru terjadi saat ride `completed`. Jika masih offline saat itu, upload di-retry otomatis (dengan backoff) saat koneksi kembali; ride tetap tersimpan lokal sampai berhasil upload.
3. **Device restart di tengah ride** — di luar scope MVP untuk di-recover otomatis; ride yang belum di-`stop` sebelum restart dianggap perlu di-review manual oleh rider saat app dibuka lagi (ditawarkan opsi stop dengan data sampai titik terakhir, atau discard).

## Terkait

- `docs/01-PRD/04-RIDE-RECORDING.md`
- `docs/13-GPS/00-GPS-ARCHITECTURE.md`
- `docs/16-RIDE/00-RIDE-LIFECYCLE.md`
