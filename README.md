# Python Journey Beginner 2025

Halo semua, aku cahyo. aku lagi belajar python pemula dengan langsung membuat projek. dan berikut kumpulan 10 proyek Python untuk pembelajaran tingkat menengah hingga lanjut. Proyek ini menggunakan Python 3.10 dengan virtual environment.

## Daftar Proyek

1. [Calculator CLI](01_calculator_cli/) - Kalkulator command line sederhana
2. [Temperature Converter](02_temperature_converter/) - Konverter suhu dan mata uang
3. [Number Guessing Game](03_number_guessing_game/) - Game tebak angka dengan sistem scoring
4. [Daily Notes App](04_daily_notes_app/) - Aplikasi catatan harian dengan JSON storage
5. [Todo List CLI](05_todo_list_cli/) - Aplikasi todo list berbasis CLI
6. [Mini Library App](06_mini_library_app/) - Sistem manajemen perpustakaan sederhana
7. [Password Generator](07_password_generator/) - Generator & validator password
8. [Weather App](08_weather_app/) - Aplikasi cuaca dengan OpenWeatherMap API
9. [GUI Calculator](09_gui_calculator/) - Kalkulator scientific dengan GUI
10. [Quiz App](10_quiz_app/) - Aplikasi kuis interaktif

## Persyaratan Sistem

- Python 3.10
- Virtual Environment
- Git (untuk version control)

## Setup Environment

1. Clone repository:
```bash
git clone <repository-url>
cd python-journey-beginner-2025
```

2. Buat virtual environment:
```bash
python -m venv .venv
```

3. Aktifkan virtual environment:
- Windows:
```bash
.venv\Scripts\activate
```
- Unix/MacOS:
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Struktur Proyek

```
python-journey-beginner-2025/
├── 01_calculator_cli/          # Basic Calculator
├── 02_temperature_converter/   # Temperature & Currency Converter
├── 03_number_guessing_game/   # Number Guessing Game
├── 04_daily_notes_app/        # Notes Application
├── 05_todo_list_cli/          # Todo List Manager
├── 06_mini_library_app/       # Library Management System
├── 07_password_generator/     # Password Tools
├── 08_weather_app/           # Weather Application
├── 09_gui_calculator/        # GUI Calculator
├── 10_quiz_app/             # Interactive Quiz
├── .gitignore               # Git ignore file
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Dependencies

- click: CLI interface
- rich: Terminal formatting
- requests: HTTP client
- pytest: Testing framework
- tkinter: GUI (included in Python)

## Testing

Setiap proyek memiliki file test sendiri. Untuk menjalankan test:

```bash
cd <nama-proyek>
pytest test_*.py
```

## Virtual Environment

Proyek ini menggunakan Python virtual environment untuk mengisolasi dependencies:

- Python version: 3.10
- venv location: `.venv/`
- Activation script: `.venv/Scripts/activate` (Windows) or `.venv/bin/activate` (Unix)

## Git Configuration

Repository ini menggunakan Git untuk version control dengan konfigurasi:
- Ignore patterns untuk Python, venv, dan IDE files
- Branch utama: main
- Commit style: Conventional Commits

## Kontribusi

1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Lisensi

Distributed under the MIT License. See `LICENSE` for more information.
