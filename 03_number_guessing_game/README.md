# Game Tebak Angka

Sebuah permainan tebak angka sederhana di mana pemain harus menebak angka yang dipilih secara acak oleh komputer. Proyek ini mengajarkan tentang penggunaan kondisi, perulangan, dan fungsi random di Python.

## Fitur

- Generate angka acak antara 1-100
- Sistem hint (lebih besar/lebih kecil)
- Perhitungan skor berdasarkan jumlah tebakan
- Sistem level kesulitan (mudah, sedang, sulit)
- Sistem high score
- Opsi untuk bermain ulang

## Cara Penggunaan

1. Pastikan Python sudah terinstal di komputer Anda
2. Jalankan program dengan perintah:
   ```
   python number_game.py
   ```
3. Pilih level kesulitan
4. Ikuti petunjuk untuk menebak angka
5. Dapatkan skor tertinggi!

## Level Kesulitan

1. Mudah
   - Range angka: 1-50
   - Maksimal tebakan: 10
   - Hint: Lebih besar/lebih kecil
   
2. Sedang
   - Range angka: 1-100
   - Maksimal tebakan: 7
   - Hint: Lebih besar/lebih kecil
   
3. Sulit
   - Range angka: 1-200
   - Maksimal tebakan: 5
   - Hint: "Panas/Dingin"

## Sistem Skor

- Skor awal: 100
- Setiap tebakan mengurangi skor sebesar:
  - Mudah: -10 poin
  - Sedang: -14 poin
  - Sulit: -20 poin
- Skor minimum: 0

## Konsep yang Dipelajari

- Random number generation
- Kondisi (if/elif/else)
- Loop (while/for)
- Input/output handling
- File handling (untuk menyimpan high score)
- Fungsi dan parameter
- Exception handling

## Struktur Proyek

```
03_number_guessing_game/
│   README.md            # Dokumentasi proyek
│   number_game.py       # Program utama
│   highscores.json     # File penyimpanan skor tertinggi
│   test_game.py        # File pengujian
```