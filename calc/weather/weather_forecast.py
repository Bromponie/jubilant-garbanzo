import argparse
import configparser
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Fetch weather forecasts using WeatherAPI.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.ini",
        help="Path to the configuration file (default: config.ini)"
    )
    parser.add_argument(
        "--lat",
        type=float,
        help="Latitude of the location (overrides config file)"
    )
    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude of the location (overrides config file)"
    )
    parser.add_argument(
        "--forecast",
        type=str,
        choices=["24h", "10d"],
        default="10d",
        required=False,
        help="Type of forecast: '24h' for 24-hour metric or '10d' for 10-day forecast"
    )
    return parser.parse_args()

def read_config(config_path):
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        lat = config.getfloat('weather', 'lat')
        lon = config.getfloat('weather', 'lon')
        return lat, lon
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
        print(f"Error reading config file: {e}")
        return None, None

def fetch_weather(api_key, lat, lon, forecast_type):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    
    params = {
        'key': api_key,
        'q': f"{lat},{lon}",
    }
    
    if forecast_type == "24h":
        # WeatherAPI provides hourly data; fetch 1 day to get 24-hour forecast
        params['days'] = 1
        # 'hour' is not an actual parameter; handle hours in code
    elif forecast_type == "10d":
        params['days'] = 10
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        sys.exit(1)

def display_24h_forecast(data):
    location = data.get('location', {})
    current = data.get('current', {})
    forecast = data.get('forecast', {}).get('forecastday', [])[0]
    hours = forecast.get('hour', [])

    print(f"24-Hour Forecast for {location.get('name')}, {location.get('region')}, {location.get('country')}")
    print(f"Current: {current.get('temp_c')}°C, {current.get('condition', {}).get('text')}\n")
    
    print(f"{'Time':<20}{'Temp (°C)':<12}{'Condition'}")
    print("-" * 50)
    
    now = datetime.now()
    end_time = now + timedelta(hours=24)
    
    for hour_data in hours:
        time_str = hour_data.get('time')
        time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        if time_obj < now:
            continue  # Skip past hours
        temp = hour_data.get('temp_c')
        condition = hour_data.get('condition', {}).get('text')
        print(f"{time_str:<20}{temp:<12}{condition}")
        if time_obj >= end_time:
            break

def display_10d_forecast(data):
    location = data.get('location', {})
    forecast_days = data.get('forecast', {}).get('forecastday', [])

    print(f"10-Day Forecast for {location.get('name')}, {location.get('region')}, {location.get('country')}\n")
    print(f"{'Date':<15}{'Avg Temp (°C)':<15}{'Condition'}")
    print("-" * 50)
    
    for day in forecast_days:
        date = day.get('date')
        day_info = day.get('day', {})
        avg_temp = day_info.get('avgtemp_c')
        condition = day_info.get('condition', {}).get('text')
        print(f"{date:<15}{avg_temp:<15}{condition}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    args = parse_arguments()
    config_lat, config_lon = read_config(args.config)
    
    # Get API key from environment variable
    api_key = os.getenv('WEATHER_API_KEY')
    
    if not api_key:
        print("API key is missing. Please set WEATHER_API_KEY in the .env file.")
        sys.exit(1)
    
    # Determine latitude and longitude
    lat = args.lat if args.lat is not None else config_lat
    lon = args.lon if args.lon is not None else config_lon
    
    if lat is None or lon is None:
        print("Latitude and Longitude must be provided either in the config file or via command-line arguments.")
        sys.exit(1)
    
    # Fetch weather data
    data = fetch_weather(api_key, lat, lon, args.forecast)
    
    # Display forecast
    if args.forecast == "24h":
        display_24h_forecast(data)
    elif args.forecast == "10d":
        display_10d_forecast(data)

if __name__ == "__main__":
    main()
