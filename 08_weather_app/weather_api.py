import requests
from datetime import datetime
import json
import os

class WeatherAPI:
    def __init__(self, api_key=None):
        """
        Inisialisasi WeatherAPI dengan API key dari OpenWeatherMap
        """
        # Jika API key tidak diberikan, coba ambil dari environment variable
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("API key diperlukan! Set OPENWEATHER_API_KEY di environment variable")
        
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.geo_url = "http://api.openweathermap.org/geo/1.0"
        self.cache_file = "weather_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self):
        """Memuat cache dari file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                    # Bersihkan cache yang sudah expired (lebih dari 30 menit)
                    current_time = datetime.now().timestamp()
                    cache = {
                        k: v for k, v in cache.items()
                        if current_time - v['timestamp'] < 1800  # 30 menit
                    }
                    return cache
        except Exception as e:
            print(f"Error loading cache: {e}")
        return {}

    def _save_cache(self):
        """Menyimpan cache ke file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def _cache_result(self, key, data):
        """Menyimpan hasil ke cache"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now().timestamp()
        }
        self._save_cache()

    def get_coordinates(self, city_name, country_code="ID"):
        """
        Mendapatkan koordinat dari nama kota
        """
        # Cek cache dulu
        cache_key = f"geo_{city_name}_{country_code}"
        if cache_key in self.cache:
            return self.cache[cache_key]['data']

        url = f"{self.geo_url}/direct"
        params = {
            'q': f"{city_name},{country_code}",
            'limit': 1,
            'appid': self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError(f"Kota {city_name} tidak ditemukan!")
            
            result = {
                'lat': data[0]['lat'],
                'lon': data[0]['lon'],
                'name': data[0]['name']
            }
            
            # Simpan ke cache
            self._cache_result(cache_key, result)
            return result

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error saat mengambil data koordinat: {e}")

    def get_current_weather(self, city_name, country_code="ID"):
        """
        Mendapatkan cuaca saat ini untuk kota tertentu
        """
        # Dapatkan koordinat
        coords = self.get_coordinates(city_name, country_code)
        
        # Cek cache
        cache_key = f"weather_{coords['lat']}_{coords['lon']}"
        if cache_key in self.cache:
            return self.cache[cache_key]['data']

        url = f"{self.base_url}/weather"
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'appid': self.api_key,
            'units': 'metric',  # Gunakan Celsius
            'lang': 'id'  # Bahasa Indonesia
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Format data
            result = {
                'city': data['name'],
                'description': data['weather'][0]['description'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Simpan ke cache
            self._cache_result(cache_key, result)
            return result

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error saat mengambil data cuaca: {e}")

    def get_forecast(self, city_name, country_code="ID", days=5):
        """
        Mendapatkan prakiraan cuaca untuk beberapa hari ke depan
        """
        # Dapatkan koordinat
        coords = self.get_coordinates(city_name, country_code)
        
        # Cek cache
        cache_key = f"forecast_{coords['lat']}_{coords['lon']}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]['data']

        url = f"{self.base_url}/forecast"
        params = {
            'lat': coords['lat'],
            'lon': coords['lon'],
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'id',
            'cnt': days * 8  # 8 data points per day (3-hour intervals)
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Format data
            forecasts = []
            for item in data['list']:
                forecast = {
                    'datetime': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M'),
                    'description': item['weather'][0]['description'],
                    'temperature': round(item['main']['temp'], 1),
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed']
                }
                forecasts.append(forecast)
            
            result = {
                'city': data['city']['name'],
                'forecasts': forecasts
            }
            
            # Simpan ke cache
            self._cache_result(cache_key, result)
            return result

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error saat mengambil prakiraan cuaca: {e}")