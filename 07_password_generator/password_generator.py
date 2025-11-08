import string
import random
from datetime import datetime
from password_validator import PasswordValidator

class PasswordGenerator:
    def __init__(self):
        """Inisialisasi generator password"""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.validator = PasswordValidator()
        self.password_history = []

    def generate_password(self, length=12, use_lower=True, use_upper=True,
                        use_digits=True, use_symbols=True, min_each=1):
        """
        Generate password dengan karakteristik yang dapat dikustomisasi
        
        Args:
            length (int): Panjang password yang diinginkan
            use_lower (bool): Gunakan huruf kecil
            use_upper (bool): Gunakan huruf besar
            use_digits (bool): Gunakan angka
            use_symbols (bool): Gunakan simbol
            min_each (int): Jumlah minimal dari setiap jenis karakter
        
        Returns:
            str: Password yang dihasilkan
        """
        if length < 4 or not any([use_lower, use_upper, use_digits, use_symbols]):
            raise ValueError("Invalid password requirements!")

        # Hitung berapa jenis karakter yang akan digunakan
        char_types_count = sum([use_lower, use_upper, use_digits, use_symbols])
        
        if length < (char_types_count * min_each):
            raise ValueError(
                f"Password length too short for minimum requirements! "
                f"Need at least {char_types_count * min_each} characters."
            )

        # Inisialisasi karakter yang akan digunakan
        all_chars = ""
        required_chars = []

        if use_lower:
            all_chars += self.lowercase
            required_chars.extend(random.sample(self.lowercase, min_each))
        
        if use_upper:
            all_chars += self.uppercase
            required_chars.extend(random.sample(self.uppercase, min_each))
        
        if use_digits:
            all_chars += self.digits
            required_chars.extend(random.sample(self.digits, min_each))
        
        if use_symbols:
            all_chars += self.symbols
            required_chars.extend(random.sample(self.symbols, min_each))

        # Generate sisa karakter yang dibutuhkan
        remaining_length = length - len(required_chars)
        password_chars = required_chars + random.sample(all_chars, remaining_length)
        
        # Acak urutan karakter
        random.shuffle(password_chars)
        password = ''.join(password_chars)

        # Cek kekuatan password
        strength_info = self.validator.calculate_strength(password)
        
        # Simpan password dalam history
        self.add_to_history(password, strength_info)

        return {
            'password': password,
            'strength': strength_info
        }

    def add_to_history(self, password, strength_info):
        """Menambahkan password ke history"""
        self.password_history.append({
            'password': password,
            'strength': strength_info,
            'timestamp': datetime.now().isoformat()
        })
        # Batasi history hanya menyimpan 10 password terakhir
        if len(self.password_history) > 10:
            self.password_history.pop(0)

    def get_history(self):
        """Mendapatkan history password yang telah di-generate"""
        return self.password_history

    def generate_memorable_password(self, num_words=3, add_number=True, add_symbol=True):
        """
        Generate password yang mudah diingat
        
        Args:
            num_words (int): Jumlah kata yang digunakan
            add_number (bool): Tambahkan angka
            add_symbol (bool): Tambahkan simbol
        
        Returns:
            dict: Password dan informasi kekuatannya
        """
        # Daftar kata umum dalam Bahasa Indonesia
        common_words = [
            "merah", "biru", "hijau", "kuning", "putih", "hitam",
            "cepat", "lambat", "tinggi", "rendah", "besar", "kecil",
            "pintar", "cerdas", "ramah", "baik", "kuat", "hebat"
        ]

        # Pilih kata secara acak
        selected_words = random.sample(common_words, num_words)
        
        # Kapitalisasi kata pertama dari setiap kata
        password_parts = [word.capitalize() for word in selected_words]

        # Tambahkan angka jika diminta
        if add_number:
            password_parts.append(str(random.randint(100, 999)))

        # Tambahkan simbol jika diminta
        if add_symbol:
            password_parts.append(random.choice(self.symbols))

        # Gabungkan semua bagian
        password = ''.join(password_parts)

        # Cek kekuatan password
        strength_info = self.validator.calculate_strength(password)
        
        # Simpan ke history
        self.add_to_history(password, strength_info)

        return {
            'password': password,
            'strength': strength_info
        }

    def generate_pin(self, length=6):
        """
        Generate PIN numerik
        
        Args:
            length (int): Panjang PIN yang diinginkan
        
        Returns:
            str: PIN yang dihasilkan
        """
        if length < 4:
            raise ValueError("PIN length must be at least 4 digits!")
        
        pin = ''.join(random.choices(self.digits, k=length))
        return pin

def main():
    """Fungsi utama untuk menjalankan password generator"""
    generator = PasswordGenerator()
    
    print("=== PASSWORD GENERATOR ===")
    print("1. Generate Password Standar")
    print("2. Generate Password Mudah Diingat")
    print("3. Generate PIN")
    print("4. Lihat History")
    print("5. Keluar")
    
    while True:
        try:
            choice = input("\nPilih opsi (1-5): ").strip()
            
            if choice == '1':
                length = int(input("Panjang password (default 12): ") or 12)
                result = generator.generate_password(length=length)
                print(f"\nPassword: {result['password']}")
                print(f"Kekuatan: {result['strength']['strength']} (Score: {result['strength']['score']}/100)")
                if result['strength']['feedback']:
                    print("Saran: " + ", ".join(result['strength']['feedback']))
                
            elif choice == '2':
                num_words = int(input("Jumlah kata (default 3): ") or 3)
                result = generator.generate_memorable_password(num_words=num_words)
                print(f"\nPassword: {result['password']}")
                print(f"Kekuatan: {result['strength']['strength']} (Score: {result['strength']['score']}/100)")
                if result['strength']['feedback']:
                    print("Saran: " + ", ".join(result['strength']['feedback']))
                
            elif choice == '3':
                length = int(input("Panjang PIN (default 6): ") or 6)
                pin = generator.generate_pin(length=length)
                print(f"\nPIN: {pin}")
                
            elif choice == '4':
                history = generator.get_history()
                if not history:
                    print("\nHistory kosong")
                else:
                    print("\n=== HISTORY PASSWORD ===")
                    for i, item in enumerate(history, 1):
                        print(f"{i}. {item['password']} - {item['strength']['strength']} - {item['timestamp'][:19]}")
                        
            elif choice == '5':
                print("Terima kasih!")
                break
                
            else:
                print("Pilihan tidak valid!")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()

    # Testing sederhana - tambahkan di akhir file
if __name__ == "__main__":
    generator = PasswordGenerator()
    
    print("=== TESTING PASSWORD GENERATOR ===")
    
    # Test 1: Password standar
    print("\n1. Password Standar:")
    result1 = generator.generate_password(length=12)
    print(f"Password: {result1['password']}")
    print(f"Kekuatan: {result1['strength']['strength']} (Score: {result1['strength']['score']}/100)")
    
    # Test 2: Password mudah diingat
    print("\n2. Password Mudah Diingat:")
    result2 = generator.generate_memorable_password(num_words=4)
    print(f"Password: {result2['password']}")
    print(f"Kekuatan: {result2['strength']['strength']} (Score: {result2['strength']['score']}/100)")
    
    # Test 3: PIN
    print("\n3. PIN:")
    pin = generator.generate_pin(length=6)
    print(f"PIN: {pin}")
    
    # Test 4: History
    print("\n4. History:")
    history = generator.get_history()
    for i, item in enumerate(history, 1):
        print(f"{i}. {item['password']} - {item['strength']['strength']}")