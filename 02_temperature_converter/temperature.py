class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        """Mengkonversi Celsius ke Fahrenheit"""
        return (celsius * 9/5) + 32

    @staticmethod
    def celsius_to_kelvin(celsius):
        """Mengkonversi Celsius ke Kelvin"""
        return celsius + 273.15

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        """Mengkonversi Fahrenheit ke Celsius"""
        return (fahrenheit - 32) * 5/9

    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit):
        """Mengkonversi Fahrenheit ke Kelvin"""
        return (fahrenheit - 32) * 5/9 + 273.15

    @staticmethod
    def kelvin_to_celsius(kelvin):
        """Mengkonversi Kelvin ke Celsius"""
        return kelvin - 273.15

    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        """Mengkonversi Kelvin ke Fahrenheit"""
        return (kelvin - 273.15) * 9/5 + 32

    @staticmethod
    def validate_temperature(value, scale):
        """Memvalidasi nilai suhu"""
        if scale == 'K' and value < 0:
            raise ValueError("Suhu Kelvin tidak boleh di bawah 0!")
        return True