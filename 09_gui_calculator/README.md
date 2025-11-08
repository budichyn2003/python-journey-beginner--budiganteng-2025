# GUI Calculator

Aplikasi kalkulator dengan antarmuka grafis (GUI) menggunakan Tkinter. Kalkulator ini memiliki fitur scientific dan history operasi.

## Fitur

1. Operasi Dasar:
   - Penjumlahan (+)
   - Pengurangan (-)
   - Perkalian (×)
   - Pembagian (÷)

2. Fungsi Scientific:
   - Akar kuadrat (√)
   - Pangkat dua (x²)
   - Trigonometri (sin, cos, tan)
   - Logaritma (log)
   - Konstanta matematika (π, e)

3. Fitur Tambahan:
   - History operasi (4 operasi terakhir)
   - Clear button (C)
   - Support angka desimal
   - Format hasil otomatis
   - Error handling

## Persyaratan

- Python 3.7+
- Tkinter (biasanya sudah terinstall dengan Python)
- Pytest (untuk testing)

## Instalasi

1. Clone repository ini
2. Install dependencies:
   ```bash
   pip install pytest
   ```

## Penggunaan

Jalankan program dengan:
```bash
python calculator.py
```

### Operasi Dasar

1. Klik angka untuk input
2. Klik operator (+, -, ×, ÷)
3. Input angka kedua
4. Klik = untuk hasil

### Fungsi Scientific

- Klik tombol fungsi (√, x², sin, cos, tan, log)
- Hasil akan langsung ditampilkan
- Konstanta π dan e dapat langsung digunakan

## Testing

Jalankan unit tests dengan:
```bash
pytest test_calculator.py
```

## Struktur Proyek

```
gui_calculator/
├── calculator.py      # Implementasi kalkulator
├── test_calculator.py # Unit tests
└── README.md         # Dokumentasi
```

## Implementasi

### GUI Components

1. Display Area:
   - Input/output display
   - History display (4 baris)

2. Button Layout:
   - Scientific functions (2 baris)
   - Angka 0-9 dengan decimal
   - Operator matematika
   - Clear dan Equal buttons

### Fitur Teknis

1. Error Handling:
   - Pembagian dengan nol
   - Akar kuadrat angka negatif
   - Log angka non-positif
   - Input validation

2. Format Hasil:
   - Otomatis remove trailing zeros
   - Round hasil desimal (8 angka)
   - Support scientific notation

3. History:
   - Format operasi yang mudah dibaca
   - Scroll otomatis ke operasi terbaru
   - Batasan 4 operasi terakhir