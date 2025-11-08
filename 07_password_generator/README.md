# Password Generator

Aplikasi command-line untuk menghasilkan password yang aman dengan berbagai konfigurasi. Proyek ini mengajarkan tentang penggunaan modul random, string, dan konsep keamanan dasar dalam pembuatan password.

## Fitur

- Generate password dengan panjang yang dapat diatur
- Pilihan karakter yang digunakan:
  - Huruf kecil (a-z)
  - Huruf besar (A-Z)
  - Angka (0-9)
  - Simbol (!@#$%^&*()_+-=[]{}|;:,.<>?)
- Pengaturan minimal karakter untuk setiap jenis
- Validasi kekuatan password
- Penyimpanan password yang dihasilkan (opsional)
- Enkripsi password yang disimpan
- Fungsi untuk mengecek apakah password sudah pernah digunakan

## Cara Penggunaan

1. Pastikan Python sudah terinstal di komputer Anda
2. Jalankan program dengan perintah:
   ```
   python password_generator.py
   ```
3. Pilih menu yang tersedia
4. Ikuti instruksi untuk menghasilkan password

## Menu Program

1. Generate Password
   - Pilih panjang password
   - Pilih jenis karakter
   - Atur jumlah minimal per jenis
   - Lihat hasil

2. Cek Kekuatan Password
   - Masukkan password
   - Lihat skor dan rekomendasi

3. Simpan Password
   - Label/keterangan
   - Password
   - Enkripsi otomatis

4. Lihat Password Tersimpan
   - Dekripsi otomatis
   - Filter berdasarkan label
   - Sort berdasarkan tanggal

## Kriteria Kekuatan Password

1. Sangat Lemah (0-20)
   - Kurang dari 8 karakter
   - Hanya satu jenis karakter

2. Lemah (21-40)
   - 8-10 karakter
   - Dua jenis karakter

3. Sedang (41-60)
   - 10-12 karakter
   - Tiga jenis karakter

4. Kuat (61-80)
   - 12-14 karakter
   - Semua jenis karakter
   - Minimal 2 karakter per jenis

5. Sangat Kuat (81-100)
   - 14+ karakter
   - Semua jenis karakter
   - Minimal 3 karakter per jenis
   - Tidak ada pola berulang

## Konsep yang Dipelajari

- Random number generation
- String manipulation
- File encryption/decryption
- Password security concepts
- JSON data handling
- Regular expressions
- Error handling

## Struktur Proyek

```
07_password_generator/
│   README.md                # Dokumentasi proyek
│   password_generator.py    # Program utama
│   password_manager.py      # Pengelola password
│   password_validator.py    # Validator password
│   encryption.py           # Modul enkripsi
│   tests/                  # Direktori pengujian
│   └── test_password.py    # File pengujian
```

## Keamanan

- Password disimpan dalam format terenkripsi
- Menggunakan Fernet (symmetric encryption) dari cryptography
- Salt unik untuk setiap password
- Tidak menyimpan password dalam plain text
- Validasi input untuk mencegah injection