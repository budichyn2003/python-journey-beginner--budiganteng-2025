import string
import random
import re
from datetime import datetime

class PasswordValidator:
    def __init__(self):
        """Inisialisasi validator"""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def count_character_types(self, password):
        """Menghitung jenis karakter dalam password"""
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_symbol = any(c in self.symbols for c in password)
        return sum([has_lower, has_upper, has_digit, has_symbol])

    def check_min_chars_per_type(self, password, min_count):
        """Mengecek jumlah minimal karakter per jenis"""
        lower_count = sum(1 for c in password if c in self.lowercase)
        upper_count = sum(1 for c in password if c in self.uppercase)
        digit_count = sum(1 for c in password if c in self.digits)
        symbol_count = sum(1 for c in password if c in self.symbols)
        
        return all(count >= min_count for count in [
            lower_count, upper_count, digit_count, symbol_count
        ])

    def has_repeating_patterns(self, password):
        """Mengecek pola berulang dalam password"""
        # Cek pola berulang dengan panjang 2-4 karakter
        for i in range(2, 5):
            for j in range(len(password) - i * 2 + 1):
                pattern = password[j:j+i]
                if password.count(pattern) > 1:
                    return True
        return False

    def calculate_strength(self, password):
        """Menghitung kekuatan password (0-100)"""
        score = 0
        feedback = []

        # 1. Panjang password (maks. 40 poin)
        length = len(password)
        if length < 8:
            score += length * 2
            feedback.append("Password terlalu pendek, minimal 8 karakter")
        elif length < 10:
            score += 20
            feedback.append("Pertimbangkan untuk menambah panjang password")
        elif length < 12:
            score += 25
            feedback.append("Panjang password cukup baik")
        elif length < 14:
            score += 35
        else:
            score += 40

        # 2. Kompleksitas karakter (maks. 40 poin)
        char_types = self.count_character_types(password)
        score += char_types * 10

        if char_types < 4:
            missing = []
            if not any(c in self.lowercase for c in password):
                missing.append("huruf kecil")
            if not any(c in self.uppercase for c in password):
                missing.append("huruf besar")
            if not any(c in self.digits for c in password):
                missing.append("angka")
            if not any(c in self.symbols for c in password):
                missing.append("simbol")
            feedback.append(f"Tambahkan {', '.join(missing)}")

        # 3. Distribusi karakter (maks. 20 poin)
        if length >= 8:
            if self.check_min_chars_per_type(password, 2):
                score += 15
            elif self.check_min_chars_per_type(password, 1):
                score += 10
                feedback.append("Tambahkan lebih banyak variasi untuk setiap jenis karakter")

        # 4. Penalti untuk pola berulang
        if self.has_repeating_patterns(password):
            score -= 10
            feedback.append("Hindari penggunaan pola yang berulang")

        # Tentukan kategori
        strength = "Sangat Lemah"
        if score > 80:
            strength = "Sangat Kuat"
        elif score > 60:
            strength = "Kuat"
        elif score > 40:
            strength = "Sedang"
        elif score > 20:
            strength = "Lemah"

        return {
            'score': min(100, max(0, score)),  # Pastikan skor antara 0-100
            'strength': strength,
            'feedback': feedback
        }

    def validate_password(self, password, min_length=8, require_all_types=True):
        """Memvalidasi password sesuai kriteria minimum"""
        if len(password) < min_length:
            raise ValueError(f"Password harus minimal {min_length} karakter!")

        if require_all_types:
            if not any(c in self.lowercase for c in password):
                raise ValueError("Password harus mengandung huruf kecil!")
            if not any(c in self.uppercase for c in password):
                raise ValueError("Password harus mengandung huruf besar!")
            if not any(c in self.digits for c in password):
                raise ValueError("Password harus mengandung angka!")
            if not any(c in self.symbols for c in password):
                raise ValueError("Password harus mengandung simbol!")

        return True