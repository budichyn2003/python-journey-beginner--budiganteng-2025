# Mini Library App

Aplikasi perpustakaan sederhana dengan konsep OOP (Object-Oriented Programming) di Python. Proyek ini mengajarkan tentang konsep dasar OOP dan CRUD (Create, Read, Update, Delete) operations.

## Fitur

- Manajemen Buku
  - Tambah buku baru
  - Edit informasi buku
  - Hapus buku
  - Cari buku
  - Lihat daftar buku

- Manajemen Anggota
  - Daftar anggota baru
  - Edit data anggota
  - Hapus anggota
  - Cari anggota
  - Lihat daftar anggota

- Sistem Peminjaman
  - Pinjam buku
  - Kembalikan buku
  - Lihat riwayat peminjaman
  - Cek keterlambatan
  - Hitung denda

## Cara Penggunaan

1. Pastikan Python sudah terinstal di komputer Anda
2. Jalankan program dengan perintah:
   ```
   python library_app.py
   ```
3. Pilih menu yang tersedia
4. Ikuti instruksi untuk mengelola perpustakaan

## Struktur Data

### Buku
```python
class Book:
    def __init__(self, id, title, author, year, quantity):
        self.id = id                # ID unik buku
        self.title = title          # Judul buku
        self.author = author        # Penulis
        self.year = year           # Tahun terbit
        self.quantity = quantity   # Jumlah copy tersedia
```

### Anggota
```python
class Member:
    def __init__(self, id, name, email, phone):
        self.id = id              # ID unik anggota
        self.name = name          # Nama anggota
        self.email = email        # Email
        self.phone = phone        # Nomor telepon
```

### Peminjaman
```python
class Borrowing:
    def __init__(self, id, member_id, book_id, borrow_date):
        self.id = id                  # ID peminjaman
        self.member_id = member_id    # ID anggota
        self.book_id = book_id        # ID buku
        self.borrow_date = borrow_date # Tanggal pinjam
        self.return_date = None        # Tanggal kembali
```

## Aturan Perpustakaan

1. Peminjaman
   - Maksimal 3 buku per anggota
   - Durasi pinjam: 14 hari
   - Perlu verifikasi ketersediaan buku

2. Pengembalian
   - Hitung keterlambatan
   - Denda: Rp 1.000/hari keterlambatan
   - Update stok buku

3. Keanggotaan
   - ID unik per anggota
   - Data lengkap wajib diisi
   - Validasi format email

## Konsep OOP yang Dipelajari

- Class dan Object
- Inheritance
- Encapsulation
- Properties dan Methods
- Error Handling
- Data Validation
- File Handling (JSON)

## Struktur Proyek

```
06_mini_library_app/
│   README.md              # Dokumentasi proyek
│   library_app.py         # Program utama
│   models/
│   ├── book.py           # Class untuk Buku
│   ├── member.py         # Class untuk Anggota
│   └── borrowing.py      # Class untuk Peminjaman
│   data/
│   ├── books.json        # Data buku
│   ├── members.json      # Data anggota
│   └── borrowings.json   # Data peminjaman
│   tests/
│   └── test_library.py   # File pengujian
```