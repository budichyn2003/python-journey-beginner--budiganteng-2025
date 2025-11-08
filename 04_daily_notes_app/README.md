# Daily Notes App

Aplikasi command-line untuk mencatat dan mengelola catatan harian. Proyek ini fokus pada penggunaan file handling di Python untuk menyimpan dan mengelola data.

## Fitur

- Membuat catatan baru
- Membaca catatan yang ada
- Mencari catatan berdasarkan tanggal
- Mencari catatan berdasarkan kata kunci
- Mengedit catatan yang ada
- Menghapus catatan
- Backup catatan ke file terpisah
- Kategorisasi catatan

## Cara Penggunaan

1. Pastikan Python sudah terinstal di komputer Anda
2. Jalankan program dengan perintah:
   ```
   python notes_app.py
   ```
3. Pilih menu yang tersedia
4. Ikuti instruksi untuk mengelola catatan

## Menu Aplikasi

1. Buat Catatan Baru
   - Masukkan judul
   - Pilih kategori
   - Tulis isi catatan
   - Otomatis tersimpan dengan timestamp

2. Lihat Catatan
   - Lihat semua catatan
   - Filter berdasarkan tanggal
   - Filter berdasarkan kategori
   - Cari berdasarkan kata kunci

3. Edit Catatan
   - Pilih catatan yang akan diedit
   - Edit judul/kategori/isi
   - Simpan perubahan

4. Hapus Catatan
   - Pilih catatan yang akan dihapus
   - Konfirmasi penghapusan

5. Backup & Restore
   - Backup semua catatan ke file terpisah
   - Restore dari file backup

## Struktur Penyimpanan

Catatan disimpan dalam format berikut:
```json
{
    "id": "note_20251108_001",
    "title": "Judul Catatan",
    "category": "Personal",
    "content": "Isi catatan...",
    "created_at": "2025-11-08 10:30:00",
    "updated_at": "2025-11-08 10:30:00"
}
```

## Kategori Default

- Personal
- Pekerjaan
- Ide
- To-Do
- Lainnya

## Konsep yang Dipelajari

- File handling (read/write)
- JSON data handling
- Date/time manipulation
- String manipulation
- Exception handling
- Data struktur
- Search algorithms

## Struktur Proyek

```
04_daily_notes_app/
│   README.md           # Dokumentasi proyek
│   notes_app.py        # Program utama
│   notes_manager.py    # Modul pengelola catatan
│   test_notes.py      # File pengujian
│   notes/             # Direktori penyimpanan catatan
│   backup/            # Direktori backup
```