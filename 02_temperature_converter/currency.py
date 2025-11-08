class CurrencyConverter:
    # Nilai tukar statis untuk tujuan pembelajaran
    RATES = {
        'USD_TO_IDR': 15500,  # 1 USD = 15500 IDR
        'EUR_TO_IDR': 17000,  # 1 EUR = 17000 IDR
    }

    @staticmethod
    def idr_to_usd(idr):
        """Mengkonversi Rupiah ke Dollar Amerika"""
        return idr / CurrencyConverter.RATES['USD_TO_IDR']

    @staticmethod
    def usd_to_idr(usd):
        """Mengkonversi Dollar Amerika ke Rupiah"""
        return usd * CurrencyConverter.RATES['USD_TO_IDR']

    @staticmethod
    def idr_to_eur(idr):
        """Mengkonversi Rupiah ke Euro"""
        return idr / CurrencyConverter.RATES['EUR_TO_IDR']

    @staticmethod
    def eur_to_idr(eur):
        """Mengkonversi Euro ke Rupiah"""
        return eur * CurrencyConverter.RATES['EUR_TO_IDR']

    @staticmethod
    def validate_amount(amount):
        """Memvalidasi jumlah mata uang"""
        if amount < 0:
            raise ValueError("Jumlah mata uang tidak boleh negatif!")
        return True