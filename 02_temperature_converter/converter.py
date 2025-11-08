from temperature import TemperatureConverter
from currency import CurrencyConverter

def display_temperature_menu():
    """Menampilkan menu konversi suhu"""
    print("\n=== Menu Konversi Suhu ===")
    print("1. Celsius ke Fahrenheit")
    print("2. Celsius ke Kelvin")
    print("3. Fahrenheit ke Celsius")
    print("4. Fahrenheit ke Kelvin")
    print("5. Kelvin ke Celsius")
    print("6. Kelvin ke Fahrenheit")
    print("7. Kembali ke menu utama")

def display_currency_menu():
    """Menampilkan menu konversi mata uang"""
    print("\n=== Menu Konversi Mata Uang ===")
    print("1. Rupiah (IDR) ke Dollar (USD)")
    print("2. Dollar (USD) ke Rupiah (IDR)")
    print("3. Rupiah (IDR) ke Euro (EUR)")
    print("4. Euro (EUR) ke Rupiah (IDR)")
    print("5. Kembali ke menu utama")

def handle_temperature_conversion():
    """Menangani konversi suhu"""
    temp_converter = TemperatureConverter()
    
    while True:
        display_temperature_menu()
        choice = input("\nPilih konversi (1-7): ")

        if choice == '7':
            break

        try:
            if choice == '1':
                celsius = float(input("Masukkan suhu dalam Celsius: "))
                temp_converter.validate_temperature(celsius + 273.15, 'K')
                result = temp_converter.celsius_to_fahrenheit(celsius)
                print(f"{celsius}°C = {result}°F")

            elif choice == '2':
                celsius = float(input("Masukkan suhu dalam Celsius: "))
                result = temp_converter.celsius_to_kelvin(celsius)
                temp_converter.validate_temperature(result, 'K')
                print(f"{celsius}°C = {result}K")

            elif choice == '3':
                fahrenheit = float(input("Masukkan suhu dalam Fahrenheit: "))
                celsius = temp_converter.fahrenheit_to_celsius(fahrenheit)
                temp_converter.validate_temperature(celsius + 273.15, 'K')
                print(f"{fahrenheit}°F = {celsius}°C")

            elif choice == '4':
                fahrenheit = float(input("Masukkan suhu dalam Fahrenheit: "))
                result = temp_converter.fahrenheit_to_kelvin(fahrenheit)
                temp_converter.validate_temperature(result, 'K')
                print(f"{fahrenheit}°F = {result}K")

            elif choice == '5':
                kelvin = float(input("Masukkan suhu dalam Kelvin: "))
                temp_converter.validate_temperature(kelvin, 'K')
                result = temp_converter.kelvin_to_celsius(kelvin)
                print(f"{kelvin}K = {result}°C")

            elif choice == '6':
                kelvin = float(input("Masukkan suhu dalam Kelvin: "))
                temp_converter.validate_temperature(kelvin, 'K')
                result = temp_converter.kelvin_to_fahrenheit(kelvin)
                print(f"{kelvin}K = {result}°F")

            else:
                print("Pilihan tidak valid!")

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: Terjadi kesalahan - {str(e)}")

def handle_currency_conversion():
    """Menangani konversi mata uang"""
    currency_converter = CurrencyConverter()
    
    while True:
        display_currency_menu()
        choice = input("\nPilih konversi (1-5): ")

        if choice == '5':
            break

        try:
            if choice == '1':
                idr = float(input("Masukkan jumlah Rupiah (IDR): "))
                currency_converter.validate_amount(idr)
                result = currency_converter.idr_to_usd(idr)
                print(f"IDR {idr:,.2f} = USD {result:,.2f}")

            elif choice == '2':
                usd = float(input("Masukkan jumlah Dollar (USD): "))
                currency_converter.validate_amount(usd)
                result = currency_converter.usd_to_idr(usd)
                print(f"USD {usd:,.2f} = IDR {result:,.2f}")

            elif choice == '3':
                idr = float(input("Masukkan jumlah Rupiah (IDR): "))
                currency_converter.validate_amount(idr)
                result = currency_converter.idr_to_eur(idr)
                print(f"IDR {idr:,.2f} = EUR {result:,.2f}")

            elif choice == '4':
                eur = float(input("Masukkan jumlah Euro (EUR): "))
                currency_converter.validate_amount(eur)
                result = currency_converter.eur_to_idr(eur)
                print(f"EUR {eur:,.2f} = IDR {result:,.2f}")

            else:
                print("Pilihan tidak valid!")

        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: Terjadi kesalahan - {str(e)}")

def main():
    """Fungsi utama program"""
    print("=== Program Konverter Suhu dan Mata Uang ===")
    
    while True:
        print("\nMenu Utama:")
        print("1. Konversi Suhu")
        print("2. Konversi Mata Uang")
        print("3. Keluar")
        
        choice = input("\nPilih menu (1-3): ")
        
        if choice == '3':
            print("Terima kasih telah menggunakan program ini!")
            break
        elif choice == '1':
            handle_temperature_conversion()
        elif choice == '2':
            handle_currency_conversion()
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()