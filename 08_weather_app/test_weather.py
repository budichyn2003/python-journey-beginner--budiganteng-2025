import pytest
from weather_api import WeatherAPI
import os
import json
from unittest.mock import patch, MagicMock

# Sample data for mocking
SAMPLE_COORDS = {
    'lat': -6.2088,
    'lon': 106.8456,
    'name': 'Jakarta'
}

SAMPLE_WEATHER = {
    'name': 'Jakarta',
    'weather': [{'description': 'cerah berawan'}],
    'main': {
        'temp': 30.5,
        'feels_like': 32.1,
        'humidity': 75
    },
    'wind': {'speed': 3.1},
    'dt': 1636300800
}

SAMPLE_FORECAST = {
    'list': [
        {
            'dt': 1636300800,
            'main': {
                'temp': 30.5,
                'humidity': 75
            },
            'weather': [{'description': 'cerah berawan'}],
            'wind': {'speed': 3.1}
        }
    ],
    'city': {'name': 'Jakarta'}
}

@pytest.fixture
def weather_api():
    """Create WeatherAPI instance with test API key"""
    os.environ['OPENWEATHER_API_KEY'] = 'test_api_key'
    return WeatherAPI()

@pytest.fixture
def mock_responses():
    """Setup mock responses for API calls"""
    with patch('requests.get') as mock_get:
        # Configure the mock to return different responses for different URLs
        def mock_response(*args, **kwargs):
            mock = MagicMock()
            url = args[0]
            
            if 'geo' in url:
                mock.json.return_value = [SAMPLE_COORDS]
            elif 'weather' in url:
                mock.json.return_value = SAMPLE_WEATHER
            elif 'forecast' in url:
                mock.json.return_value = SAMPLE_FORECAST
            
            return mock
            
        mock_get.side_effect = mock_response
        yield mock_get

def test_init_without_api_key():
    """Test initialization without API key"""
    if 'OPENWEATHER_API_KEY' in os.environ:
        del os.environ['OPENWEATHER_API_KEY']
    
    with pytest.raises(ValueError):
        WeatherAPI()

def test_get_coordinates(weather_api, mock_responses):
    """Test getting coordinates for a city"""
    coords = weather_api.get_coordinates('Jakarta')
    
    assert coords['lat'] == SAMPLE_COORDS['lat']
    assert coords['lon'] == SAMPLE_COORDS['lon']
    assert coords['name'] == SAMPLE_COORDS['name']
    
    # Verify API was called with correct parameters
    mock_responses.assert_called_once()
    args, kwargs = mock_responses.call_args
    assert 'q=Jakarta,ID' in kwargs['params']['q']

def test_get_current_weather(weather_api, mock_responses):
    """Test getting current weather data"""
    weather = weather_api.get_current_weather('Jakarta')
    
    assert weather['city'] == 'Jakarta'
    assert 'temperature' in weather
    assert 'humidity' in weather
    assert 'wind_speed' in weather
    assert 'description' in weather
    
    # Should make two API calls (geo + weather)
    assert mock_responses.call_count == 2

def test_get_forecast(weather_api, mock_responses):
    """Test getting weather forecast"""
    forecast = weather_api.get_forecast('Jakarta', days=1)
    
    assert forecast['city'] == 'Jakarta'
    assert 'forecasts' in forecast
    assert len(forecast['forecasts']) > 0
    
    # Check forecast data structure
    first_forecast = forecast['forecasts'][0]
    assert 'datetime' in first_forecast
    assert 'temperature' in first_forecast
    assert 'humidity' in first_forecast
    assert 'wind_speed' in first_forecast
    assert 'description' in first_forecast

def test_cache_functionality(weather_api, mock_responses):
    """Test that caching works properly"""
    # First call should hit the API
    weather_api.get_current_weather('Jakarta')
    initial_calls = mock_responses.call_count
    
    # Second call should use cache
    weather_api.get_current_weather('Jakarta')
    assert mock_responses.call_count == initial_calls
    
    # Verify cache file exists
    assert os.path.exists(weather_api.cache_file)
    
    # Verify cache content
    with open(weather_api.cache_file, 'r') as f:
        cache = json.load(f)
        assert len(cache) > 0

def test_error_handling(weather_api):
    """Test error handling for API failures"""
    with patch('requests.get') as mock_get:
        # Simulate network error
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(ConnectionError):
            weather_api.get_current_weather('InvalidCity')

def test_cache_expiry(weather_api, mock_responses):
    """Test that cache entries expire correctly"""
    # Make initial request
    weather_api.get_current_weather('Jakarta')
    
    # Modify cache timestamp to be old
    with open(weather_api.cache_file, 'r') as f:
        cache = json.load(f)
    
    for key in cache:
        cache[key]['timestamp'] = 0  # Set to past timestamp
    
    with open(weather_api.cache_file, 'w') as f:
        json.dump(cache, f)
    
    # Next request should hit API again
    weather_api.get_current_weather('Jakarta')
    assert mock_responses.call_count > 1

def test_different_country_codes(weather_api, mock_responses):
    """Test using different country codes"""
    weather_api.get_current_weather('London', 'GB')
    
    args, kwargs = mock_responses.call_args_list[0]
    assert 'q=London,GB' in kwargs['params']['q']