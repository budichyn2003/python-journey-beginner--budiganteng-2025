# Weather App

Aplikasi prakiraan cuaca sederhana yang menggunakan OpenWeatherMap API untuk menampilkan informasi cuaca saat ini dan prakiraan cuaca untuk beberapa hari ke depan.

## Fitur

- Menampilkan cuaca saat ini untuk kota tertentu
- Menampilkan prakiraan cuaca untuk beberapa hari ke depan
- Dukungan multi-bahasa (Bahasa Indonesia)
- Caching data untuk mengurangi request API
- Interface CLI yang interaktif dengan tampilan yang menarik
- Support untuk berbagai negara

## Persyaratan

- Python 3.7+
- OpenWeatherMap API key (daftar di https://openweathermap.org/api)
- Package yang diperlukan:
  - requests
  - click
  - rich
  - pytest (untuk testing)

## Instalasi

1. Clone repository ini
2. Install dependencies:
   ```bash
   pip install requests click rich pytest
   ```
3. Set API key OpenWeatherMap:
   ```bash
   python main.py set-api-key "YOUR_API_KEY"
   ```

## Penggunaan

### Melihat Cuaca Saat Ini

```bash
python main.py current Jakarta
```

Dengan kode negara spesifik:
```bash
python main.py current London --country GB
```

### Melihat Prakiraan Cuaca

```bash
python main.py forecast Jakarta
```

Dengan jumlah hari spesifik:
```bash
python main.py forecast Jakarta --days 3
```

### Set API Key

```bash
python main.py set-api-key "YOUR_API_KEY"
```

## Testing

Untuk menjalankan test suite:

```bash
pytest test_weather.py
```

## Struktur Proyek

```
weather_app/
│
├── main.py             # CLI interface
├── weather_api.py      # Implementasi WeatherAPI
├── test_weather.py     # Unit tests
└── weather_cache.json  # Cache file (auto-generated)
```

## Cache

Aplikasi menggunakan sistem cache sederhana untuk:
- Mengurangi jumlah request ke API
- Mempercepat respons untuk request yang sama
- Cache otomatis expired setelah 30 menit

## Penanganan Error

- Validasi API key
- Pengecekan koneksi internet
- Validasi input kota dan negara
- Penanganan error API

## Catatan

- API key hanya tersimpan untuk sesi saat ini
- Untuk penggunaan permanen, set environment variable `OPENWEATHER_API_KEY`
- Cache disimpan di file `weather_cache.json`