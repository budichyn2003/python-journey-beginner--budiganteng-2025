import unittest
from temperature import TemperatureConverter
from currency import CurrencyConverter

class TestTemperatureConverter(unittest.TestCase):
    def setUp(self):
        self.converter = TemperatureConverter()

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(self.converter.celsius_to_fahrenheit(-40), -40)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(self.converter.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(self.converter.celsius_to_kelvin(-273.15), 0)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(32), 0)
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(212), 100)
        self.assertAlmostEqual(self.converter.fahrenheit_to_celsius(-40), -40)

    def test_fahrenheit_to_kelvin(self):
        self.assertAlmostEqual(self.converter.fahrenheit_to_kelvin(32), 273.15)
        self.assertAlmostEqual(self.converter.fahrenheit_to_kelvin(212), 373.15)

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(self.converter.kelvin_to_celsius(273.15), 0)
        self.assertAlmostEqual(self.converter.kelvin_to_celsius(373.15), 100)

    def test_kelvin_to_fahrenheit(self):
        self.assertAlmostEqual(self.converter.kelvin_to_fahrenheit(273.15), 32)
        self.assertAlmostEqual(self.converter.kelvin_to_fahrenheit(373.15), 212)

    def test_temperature_validation(self):
        with self.assertRaises(ValueError):
            self.converter.validate_temperature(-1, 'K')
        self.assertTrue(self.converter.validate_temperature(0, 'K'))
        self.assertTrue(self.converter.validate_temperature(300, 'K'))

class TestCurrencyConverter(unittest.TestCase):
    def setUp(self):
        self.converter = CurrencyConverter()

    def test_idr_to_usd(self):
        self.assertAlmostEqual(self.converter.idr_to_usd(15500), 1)
        self.assertAlmostEqual(self.converter.idr_to_usd(31000), 2)

    def test_usd_to_idr(self):
        self.assertAlmostEqual(self.converter.usd_to_idr(1), 15500)
        self.assertAlmostEqual(self.converter.usd_to_idr(2), 31000)

    def test_idr_to_eur(self):
        self.assertAlmostEqual(self.converter.idr_to_eur(17000), 1)
        self.assertAlmostEqual(self.converter.idr_to_eur(34000), 2)

    def test_eur_to_idr(self):
        self.assertAlmostEqual(self.converter.eur_to_idr(1), 17000)
        self.assertAlmostEqual(self.converter.eur_to_idr(2), 34000)

    def test_amount_validation(self):
        with self.assertRaises(ValueError):
            self.converter.validate_amount(-100)
        self.assertTrue(self.converter.validate_amount(0))
        self.assertTrue(self.converter.validate_amount(100))

if __name__ == '__main__':
    unittest.main()