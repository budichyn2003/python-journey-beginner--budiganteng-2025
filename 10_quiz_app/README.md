# Quiz App

Aplikasi kuis interaktif berbasis CLI dengan fitur manajemen pertanyaan, multiple kategori, dan tracking hasil.

## Fitur

1. Manajemen Quiz:
   - Multiple kategori quiz
   - Tambah kategori baru
   - Tambah pertanyaan baru
   - Penjelasan untuk setiap jawaban
   - Randomisasi pertanyaan

2. Mode Quiz:
   - Pilih kategori
   - Set jumlah pertanyaan
   - Timer untuk setiap sesi
   - Feedback langsung

3. Hasil & History:
   - Skor akhir
   - Persentase keberhasilan
   - Durasi pengerjaan
   - Detail jawaban
   - History quiz yang pernah diambil

4. Interface:
   - CLI yang interaktif
   - Tampilan berwarna
   - Format yang rapi
   - Progress tracking

## Persyaratan

- Python 3.7+
- Package yang diperlukan:
  - click (CLI interface)
  - rich (Formatting)
  - pytest (Testing)

## Instalasi

1. Clone repository ini
2. Install dependencies:
   ```bash
   pip install click rich pytest
   ```

## Penggunaan

### Mulai Quiz Baru

```bash
python main.py start
```

### Lihat History Quiz

```bash
python main.py history
```

### Tambah Pertanyaan Baru

```bash
python main.py add
```

## Data Quiz

Quiz disimpan dalam format JSON dengan struktur:

```json
{
    "categories": ["Python", "JavaScript", "General Knowledge"],
    "quizzes": {
        "Python": [
            {
                "question": "Pertanyaan",
                "answers": ["A", "B", "C", "D"],
                "correct_answer": 0,
                "explanation": "Penjelasan jawaban"
            }
        ]
    }
}
```

## Struktur Proyek

```
quiz_app/
├── main.py          # CLI interface
├── quiz.py          # Core functionality
├── test_quiz.py     # Unit tests
├── README.md        # Dokumentasi
├── quiz_data.json   # Data quiz
└── quiz_results.json # History hasil
```

## Testing

Jalankan unit tests:
```bash
pytest test_quiz.py
```

## Fitur Teknis

1. Data Management:
   - JSON storage
   - File handling
   - Data validation

2. Quiz Logic:
   - Score calculation
   - Answer validation
   - Progress tracking
   - Results aggregation

3. User Interface:
   - Color coding
   - Tabular display
   - Progress indicators
   - Error handling

4. History Tracking:
   - Session timing
   - Answer recording
   - Score history
   - Performance metrics