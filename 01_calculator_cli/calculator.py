def add(x, y):
    """Fungsi untuk menambahkan dua angka"""
    return x + y

def subtract(x, y):
    """Fungsi untuk mengurangkan dua angka"""
    return x - y

def multiply(x, y):
    """Fungsi untuk mengalikan dua angka"""
    return x * y

def divide(x, y):
    """Fungsi untuk membagi dua angka"""
    if y == 0:
        return "Error: Pembagian dengan nol tidak diperbolehkan!"
    return x / y

def power(x, y):
    """Fungsi untuk perpangkatan"""
    return x ** y

def modulus(x, y):
    """Fungsi untuk mendapatkan sisa pembagian"""
    if y == 0:
        return "Error: Modulus dengan nol tidak diperbolehkan!"
    return x % y

def main():
    """Fungsi utama program kalkulator"""
    print("=== Kalkulator Sederhana ===")
    print("Operasi yang tersedia:")
    print("1. Penjumlahan (+)")
    print("2. Pengurangan (-)")
    print("3. Perkalian (*)")
    print("4. Pembagian (/)")
    print("5. Perpangkatan (**)")
    print("6. Modulus (%)")
    print("7. Keluar")

    while True:
        try:
            # Meminta input dari pengguna
            choice = input("\nPilih operasi (1-7): ")
            
            # Cek apakah pengguna ingin keluar
            if choice == '7':
                print("Terima kasih telah menggunakan kalkulator ini!")
                break

            # Memastikan pilihan valid
            if choice not in ['1', '2', '3', '4', '5', '6']:
                print("Error: Pilihan tidak valid!")
                continue

            # Meminta input angka
            num1 = float(input("Masukkan angka pertama: "))
            num2 = float(input("Masukkan angka kedua: "))

            # Melakukan operasi sesuai pilihan
            if choice == '1':
                print(f"Hasil: {num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"Hasil: {num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"Hasil: {num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"Hasil: {num1} / {num2} = {result}")
            elif choice == '5':
                print(f"Hasil: {num1} ** {num2} = {power(num1, num2)}")
            elif choice == '6':
                result = modulus(num1, num2)
                print(f"Hasil: {num1} % {num2} = {result}")

        except ValueError:
            print("Error: Masukkan angka yang valid!")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()