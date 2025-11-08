# Konverter Suhu dan Mata Uang

Proyek ini adalah aplikasi command-line untuk mengkonversi suhu (Celsius, Fahrenheit, Kelvin) dan mata uang dasar. Proyek ini mengajarkan tentang operasi matematika dan modularisasi dalam Python.

## Fitur

### Konverter Suhu
- Celsius ke Fahrenheit
- Celsius ke Kelvin
- Fahrenheit ke Celsius
- Fahrenheit ke Kelvin
- Kelvin ke Celsius
- Kelvin ke Fahrenheit

### Konverter Mata Uang
- IDR (Rupiah) ke USD (Dollar Amerika)
- USD ke IDR
- IDR ke EUR (Euro)
- EUR ke IDR

## Cara Penggunaan

1. Pastikan Python sudah terinstal di komputer Anda
2. Jalankan program dengan perintah:
   ```
   python converter.py
   ```
3. Pilih jenis konversi (suhu atau mata uang)
4. Ikuti instruksi yang muncul di layar
5. Lihat hasil konversi

## Konsep yang Dipelajari

- Modularisasi program
- Operasi matematika
- Fungsi dan parameter
- Pemisahan concerns (separation of concerns)
- Dokumentasi kode
- Error handling
- Unit testing

## Struktur Proyek

```
02_temperature_converter/
│   README.md              # Dokumentasi proyek
│   converter.py           # Program utama
│   temperature.py         # Modul konverter suhu
│   currency.py           # Modul konverter mata uang
│   test_converter.py     # File pengujian
```

## Formula Konversi Suhu

- Celsius ke Fahrenheit: (°C × 9/5) + 32
- Celsius ke Kelvin: °C + 273.15
- Fahrenheit ke Celsius: (°F - 32) × 5/9
- Fahrenheit ke Kelvin: (°F - 32) × 5/9 + 273.15
- Kelvin ke Celsius: K - 273.15
- Kelvin ke Fahrenheit: (K - 273.15) × 9/5 + 32

## Catatan untuk Konversi Mata Uang

Nilai tukar yang digunakan dalam program ini adalah nilai statis untuk tujuan pembelajaran. Dalam aplikasi nyata, sebaiknya menggunakan API untuk mendapatkan nilai tukar terkini.