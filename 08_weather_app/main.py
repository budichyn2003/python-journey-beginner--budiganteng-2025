import click
from weather_api import WeatherAPI
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime
import os

console = Console()

def display_current_weather(weather_data):
    """Menampilkan data cuaca saat ini dengan format yang bagus"""
    table = Table(title=f"Cuaca di {weather_data['city']}", box=box.ROUNDED)
    
    table.add_column("Parameter", style="cyan", no_wrap=True)
    table.add_column("Nilai", style="green")
    
    table.add_row("Waktu", weather_data['timestamp'])
    table.add_row("Deskripsi", weather_data['description'].capitalize())
    table.add_row("Suhu", f"{weather_data['temperature']}°C")
    table.add_row("Terasa seperti", f"{weather_data['feels_like']}°C")
    table.add_row("Kelembaban", f"{weather_data['humidity']}%")
    table.add_row("Kecepatan Angin", f"{weather_data['wind_speed']} m/s")
    
    console.print(table)

def display_forecast(forecast_data):
    """Menampilkan prakiraan cuaca dengan format yang bagus"""
    table = Table(
        title=f"Prakiraan Cuaca {forecast_data['city']}", 
        box=box.ROUNDED
    )
    
    table.add_column("Waktu", style="cyan", no_wrap=True)
    table.add_column("Suhu", justify="right", style="green")
    table.add_column("Deskripsi", style="yellow")
    table.add_column("Kelembaban", justify="right", style="blue")
    table.add_column("Angin", justify="right", style="magenta")
    
    for forecast in forecast_data['forecasts']:
        table.add_row(
            forecast['datetime'],
            f"{forecast['temperature']}°C",
            forecast['description'].capitalize(),
            f"{forecast['humidity']}%",
            f"{forecast['wind_speed']} m/s"
        )
    
    console.print(table)

@click.group()
def cli():
    """Aplikasi Prakiraan Cuaca"""
    pass

@cli.command()
@click.argument('city')
@click.option('--country', '-c', default='ID', help='Kode negara (default: ID)')
def current(city, country):
    """Tampilkan cuaca saat ini untuk kota tertentu"""
    try:
        api = WeatherAPI()
        weather = api.get_current_weather(city, country)
        display_current_weather(weather)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")

@cli.command()
@click.argument('city')
@click.option('--country', '-c', default='ID', help='Kode negara (default: ID)')
@click.option('--days', '-d', default=5, help='Jumlah hari (default: 5)')
def forecast(city, country, days):
    """Tampilkan prakiraan cuaca untuk beberapa hari ke depan"""
    try:
        api = WeatherAPI()
        forecast_data = api.get_forecast(city, country, days)
        display_forecast(forecast_data)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")

@cli.command()
@click.argument('api_key')
def set_api_key(api_key):
    """Set API key untuk OpenWeatherMap"""
    try:
        # Set environment variable
        os.environ['OPENWEATHER_API_KEY'] = api_key
        
        # Test the API key
        api = WeatherAPI(api_key)
        test_result = api.get_current_weather("Jakarta")
        
        console.print("[green]API key berhasil disimpan dan diverifikasi![/green]")
        console.print("Contoh data cuaca Jakarta:")
        display_current_weather(test_result)
        
        # Instruksi untuk pengguna
        console.print("\n[yellow]Catatan:[/yellow] API key hanya tersimpan untuk sesi ini.")
        console.print("Untuk penggunaan permanen, tambahkan ke environment variables sistem:")
        console.print("OPENWEATHER_API_KEY=" + api_key)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")

if __name__ == '__main__':
    cli()