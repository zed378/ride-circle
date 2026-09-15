# Distance Calculation

**Folder:** `13-GPS — GPS & Location Engine`
**Status:** MVP

## Metode

Jarak total = akumulasi jarak antar titik GPS berurutan yang valid, dihitung dengan formula **Haversine** (jarak great-circle di permukaan bumi):

```
distance_total = Σ haversine(point_i-1, point_i)   untuk semua titik valid berurutan
```

## Aturan validitas titik untuk perhitungan jarak

1. Titik dengan `low_confidence = true` dilewati — jarak dihitung dari titik valid sebelumnya ke titik valid berikutnya (bukan otomatis nol).
2. Lompatan jarak yang tidak wajar antar dua titik berurutan (>500m dalam <3 detik, setara >600 km/j) diabaikan sebagai GPS jump — titik tersebut ditandai `low_confidence` secara retroaktif oleh backend saat memproses upload, meski tadinya lolos filter accuracy di device.
3. Jarak yang dihitung selama periode `paused` (lihat `09-PAUSE-RESUME.md`) tidak diikutsertakan — sampling GPS memang dihentikan saat pause, sehingga tidak ada titik baru di rentang tersebut.

## Presisi & pembulatan

- Disimpan dengan presisi 3 desimal km secara internal (meter-level).
- Ditampilkan ke rider dibulatkan 1 desimal (misal "42.7 km").

## Kenapa Haversine, bukan formula Vincenty

Vincenty lebih presisi untuk elipsoid bumi tapi perbedaannya untuk jarak riding harian (puluhan-ratusan km) secara praktis tidak signifikan dibanding noise GPS itu sendiri, sementara Haversine jauh lebih murah secara komputasi. Cukup untuk MVP; bisa direvisit jika akurasi jadi masalah nyata.

## Terkait

- `docs/13-GPS/01-LOCATION-SAMPLING.md`
- `docs/13-GPS/06-SPEED-CALCULATION.md`
- `docs/07-DOMAIN/03-RIDE.md`
