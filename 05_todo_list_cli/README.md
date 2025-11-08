# To-Do List CLI dengan JSON

Aplikasi command-line untuk mengelola daftar tugas dengan penyimpanan JSON. Proyek ini fokus pada penggunaan struktur data (list, dictionary) dan serialisasi JSON di Python.

## Fitur

- Tambah tugas baru dengan prioritas
- Lihat semua tugas
- Filter tugas berdasarkan status
- Filter tugas berdasarkan prioritas
- Tandai tugas selesai/belum
- Edit detail tugas
- Hapus tugas
- Kategorisasi tugas
- Due date untuk tugas
- Progress tracking

## Cara Penggunaan

1. Pastikan Python sudah terinstal di komputer Anda
2. Jalankan program dengan perintah:
   ```
   python todo_app.py
   ```
3. Ikuti menu yang tersedia untuk mengelola tugas

## Struktur Data

Tugas disimpan dalam format JSON:
```json
{
    "id": "task_001",
    "title": "Judul tugas",
    "description": "Deskripsi tugas",
    "category": "Pekerjaan",
    "priority": "Tinggi",
    "status": "Pending",
    "due_date": "2025-12-31",
    "created_at": "2025-11-08",
    "completed_at": null,
    "progress": 0
}
```

## Menu Aplikasi

1. Tambah Tugas
   - Judul
   - Deskripsi
   - Kategori
   - Prioritas
   - Due date

2. Lihat Tugas
   - Semua tugas
   - Filter status
   - Filter prioritas
   - Filter kategori
   - Tampilan kalender

3. Update Tugas
   - Status
   - Progress
   - Detail tugas

4. Hapus Tugas
   - Hapus satu tugas
   - Hapus semua tugas selesai

## Kategori

- Pekerjaan
- Pribadi
- Belanja
- Belajar
- Lainnya

## Prioritas

- Tinggi (Merah)
- Sedang (Kuning)
- Rendah (Hijau)

## Status

- Pending
- In Progress
- Completed
- Cancelled

## Konsep yang Dipelajari

- Struktur data Python (list, dict)
- JSON serialization/deserialization
- File handling
- Date/time manipulation
- Color formatting di terminal
- Data filtering dan sorting
- Error handling

## Struktur Proyek

```
05_todo_list_cli/
│   README.md           # Dokumentasi proyek
│   todo_app.py         # Program utama
│   todo_manager.py     # Pengelola data todo
│   test_todo.py       # File pengujian
│   tasks.json         # File penyimpanan tugas
```