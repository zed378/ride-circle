# Authentication

**Folder:** `01-PRD — Product Requirements`
**Status:** MVP

## Tujuan

Rider bisa membuat akun dan masuk kembali dengan aman, sebagai prasyarat semua fitur lain (ride tersimpan ke akun, post punya penulis, follow butuh identitas).

## User stories

- Sebagai rider baru, saya bisa daftar pakai email + password.
- Sebagai rider baru, saya bisa daftar/login pakai Google (OAuth) supaya lebih cepat.
- Sebagai rider, saya bisa login kembali di perangkat yang sama tanpa harus login ulang setiap buka app (session persist).
- Sebagai rider, saya bisa logout.
- Sebagai rider, saya bisa reset password kalau lupa.

## Requirement fungsional

1. **Register (email/password)** — email unik, password minimal 8 karakter, verifikasi email dikirim (tidak blocking login pertama, tapi ditandai di profil).
2. **Login (email/password)** — rate-limited (maks 5 percobaan gagal / 15 menit per akun untuk mencegah brute force).
3. **OAuth Google** — akun baru otomatis dibuat dari data Google (nama, email, foto) jika belum ada; email dari Google dianggap sudah terverifikasi.
4. **Session** — token-based (JWT access token + refresh token). Access token umur pendek (~15 menit), refresh token disimpan aman di device (Keychain/Keystore).
5. **Logout** — invalidate refresh token di server.
6. **Reset password** — kirim link/kode ke email, link kedaluwarsa dalam 30 menit.

## Non-functional

- Password di-hash dengan bcrypt/argon2, tidak pernah disimpan plain text.
- Semua endpoint auth wajib HTTPS.
- Refresh token dapat di-revoke (untuk kasus "logout dari semua perangkat").

## Out of scope (MVP ini)

- Login dengan nomor telepon/OTP SMS.
- Multi-factor authentication.
- Login dengan Apple/Facebook (bisa ditambah pasca-MVP kalau dibutuhkan).

## Terkait

- `docs/07-DOMAIN/01-RIDER.md`
- `docs/31-SECURITY/01-AUTH-SECURITY.md` (Post-MVP, referensi hardening lanjutan)
