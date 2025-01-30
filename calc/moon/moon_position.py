from skyfield.api import load, wgs84
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Tuple
import argparse
import configparser
import sys

def parse_arguments() -> Tuple[dict, str]:
    """Parse command-line arguments and config file."""
    parser = argparse.ArgumentParser(description='Get current Moon position')
    parser.add_argument('--lat', type=float, help='Latitude in degrees')
    parser.add_argument('--lon', type=float, help='Longitude in degrees')
    parser.add_argument('--tz', type=str, help='Timezone name (e.g. America/New_York)')
    parser.add_argument('--config', type=str, help='Path to config file')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    params = {'latitude': None, 'longitude': None, 'timezone_str': 'UTC'}

    # Load config file if specified and no CLI arguments
    if args.config and not any([args.lat, args.lon, args.tz]):
        try:
            config.read(args.config)
            params.update({
                'latitude': config.getfloat('location', 'lat', fallback=None),
                'longitude': config.getfloat('location', 'lon', fallback=None),
                'timezone_str': config.get('location', 'tz', fallback='UTC')
            })
        except Exception as e:
            print(f"Error reading config file: {e}")
            sys.exit(1)

    # Override with command-line arguments
    if args.lat is not None:
        params['latitude'] = args.lat
    if args.lon is not None:
        params['longitude'] = args.lon
    if args.tz is not None:
        params['timezone_str'] = args.tz

    return params, args.config

def validate_input(params: dict) -> Tuple[float, float, str]:
    """Validate and collect required parameters."""
    def get_float(prompt: str, min_val: float, max_val: float) -> float:
        while True:
            try:
                value = float(input(prompt))
                if min_val <= value <= max_val:
                    return value
                print(f"Value must be between {min_val} and {max_val}")
            except ValueError:
                print("Please enter a valid number")

    # Validate latitude
    while params['latitude'] is None or not (-90 <= params['latitude'] <= 90):
        params['latitude'] = get_float("Enter latitude (-90 to 90): ", -90, 90)

    # Validate longitude
    while params['longitude'] is None or not (-180 <= params['longitude'] <= 180):
        params['longitude'] = get_float("Enter longitude (-180 to 180): ", -180, 180)

    # Validate timezone
    while True:
        try:
            ZoneInfo(params['timezone_str'])
            break
        except Exception:
            print(f"Invalid timezone: {params['timezone_str']}")
            params['timezone_str'] = input("Enter valid timezone (e.g. America/New_York): ")

    return params['latitude'], params['longitude'], params['timezone_str']

def get_moon_position(latitude: float, longitude: float, timezone_str: str = 'UTC') -> Optional[None]:
    """
    Prints the current position of the Moon (altitude, azimuth, and distance) from a specified location.
    
    :param latitude: Observer's latitude in degrees.
    :param longitude: Observer's longitude in degrees.
    :param timezone_str: Timezone string, e.g., 'America/New_York'.
    """
    try:
        # Initialize timezone
        timezone = ZoneInfo(timezone_str)
    except Exception as e:
        print(f"Error: Invalid timezone '{timezone_str}'. {e}")
        return

    try:
        # Load timescale and ephemeris data
        ts = load.timescale()
        eph = load('de421.bsp')
    except Exception as e:
        print(f"Error loading ephemeris data: {e}")
        return

    # Define observer's location on Earth
    observer = eph['earth'] + wgs84.latlon(latitude, longitude)

    # Get current UTC time and convert to Skyfield's Time object
    utc_now = datetime.now(ZoneInfo('UTC'))
    t = ts.from_datetime(utc_now)

    # Observe the Moon from the observer's location at time t
    moon = eph['moon']
    try:
        astrometric = observer.at(t).observe(moon).apparent()
    except AttributeError as e:
        print(f"Error during observation: {e}")
        return

    alt, az, distance = astrometric.altaz()

    # Convert UTC time to local timezone
    local_time = utc_now.astimezone(timezone)
    time_str = local_time.strftime('%Y-%m-%d %H:%M:%S %Z')

    # Display the Moon's position
    print(f"\nCurrent Moon Position as of {time_str}:")
    print(f"  Altitude : {alt.degrees:.2f}")
    print(f"  Azimuth  : {az.degrees:.2f} (east of north)")
    print(f"  Distance : {distance.km:.2f} km")

if __name__ == "__main__":
    # Parse command-line and config file
    params, config_path = parse_arguments()
    
    # Get and validate parameters
    lat, lon, tz = validate_input(params)
    
    # Execute main function
    get_moon_position(latitude=lat, longitude=lon, timezone_str=tz)