import os
import json
import argparse
import datetime
import pytz
from pysolar.solar import get_altitude, get_azimuth

CONFIG_FILENAME = "config.json"

def load_config(filename=CONFIG_FILENAME):
    """
    Load latitude/longitude from a JSON config file if it exists.
    Expected format:
        {
            "latitude": <float>,
            "longitude": <float>
            "timezone":  <string>
        }
    :param filename: Path to the config file (default: 'config.json').
    :return: (latitude, longitude, timezone) from config or (None, None, None) if file doesn't exist or fails to parse.
    """
    
    if not os.path.isfile(filename):
        current_path = os.path.abspath(os.getcwd())
        print(f"Config file '{filename}' not found in current directory: {current_path}")
        print("Files in the current directory:")
        for f in os.listdir(current_path):
            print(f)
        return None, None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            lat = data.get("latitude")
            lon = data.get("longitude")
            timez = data.get("timezone")
            return lat, lon, timez
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: could not read/parse config file '{filename}' ({e}).")
        return None, None, None





def get_sun_position(latitude, longitude, when_utc=None):
    """
    Calculate the sun's elevation (altitude) and azimuth for a given location and time (UTC).

    :param latitude:  Latitude in decimal degrees (float)
    :param longitude: Longitude in decimal degrees (float)
    :param when_utc:  A datetime object in UTC. If None, uses the current UTC time.
    :return: (elevation_degrees, azimuth_degrees)
             elevation_degrees = angle above the horizon in degrees
             azimuth_degrees   = angle measured by PySolar's default:
                                South=0, West=90, North=180, East=270.
    """
    if when_utc is None:
        when_utc = datetime.datetime.now(tz=pytz.UTC)

    elevation_degrees = get_altitude(latitude, longitude, when_utc)
    azimuth_degrees = get_azimuth(latitude, longitude, when_utc)
    return elevation_degrees, azimuth_degrees

def convert_azimuth_pysolar_to_north0(azimuth_south0):
    """
    Convert PySolars azimuth (South=0, West=90, North=180, East=270)
    to a more conventional system where North=0, East=90, South=180, West=270.
    """
    # Shift by 180 and wrap to [0, 360).
    az_north0 = (azimuth_south0 + 180.0) % 360.0
    return az_north0

def main():
   
    # Try to load default coordinates from config file first
    config_lat, config_lon, config_timezone = load_config()

    # If config file not found or invalid, use these fallback defaults
    default_lat = config_lat if config_lat is not None else -25.826629230519135
    default_lon = config_lon if config_lon is not None else 28.223651260896336
    local_tz = config_timezone if config_timezone is not None else "Universal"

    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Calculate the sun's elevation and azimuth for a given location and time.  e.g. python sun.py --lat 34.0522 --lon -118.2437 --date 2025-07-01 --time 15:30 --tz America/Los_Angeles"
    )

    parser.add_argument("--lat", type=float, default=None, help=f"Latitude in decimal degrees (default from {CONFIG_FILENAME} if present, else {default_lat})")
    parser.add_argument("--lon", type=float, default=None, help=f"Longitude in decimal degrees (default from {CONFIG_FILENAME} if present, else {default_lon})")
    parser.add_argument("--date", default=None, help="Local date in YYYY-MM-DD format (default: today's date)")
    parser.add_argument("--time", default=None, help="Local time in HH:MM (24-hour) format (default: current local time)")
    parser.add_argument("--tz",   default=local_tz, help="Local time zone (default: Africa/Accra | Universal | America/Los_Angeles)")

    args = parser.parse_args()

    # Determine final lat/lon:
    # 1) If user provided via CLI, use that.
    # 2) Else use config (loaded above).
    # 3) Else fallback to built-in default.
    latitude = args.lat if args.lat is not None else default_lat
    longitude = args.lon if args.lon is not None else default_lon
    
    # Validate lat/lon
    if latitude is None or longitude is None:
        parser.error("No valid latitude/longitude found. Provide via CLI or config file.")

    # Handle local date/time
    local_tz = pytz.timezone(args.tz)
        
    if args.date and args.time:
        # User provided date and time
        local_dt_str = f"{args.date} {args.time}"
        local_format = "%Y-%m-%d %H:%M"
        local_dt = datetime.datetime.strptime(local_dt_str, local_format)
        local_dt = local_tz.localize(local_dt)
    elif args.date and not args.time:
        # Provided date but not time => assume midnight local
        local_format = "%Y-%m-%d"
        local_dt = datetime.datetime.strptime(args.date, local_format)
        local_dt = local_tz.localize(local_dt)
    else:
        # No date/time => use current local time
        local_dt = datetime.datetime.now(tz=local_tz)

    # Convert local time to UTC
    when_utc = local_dt.astimezone(pytz.UTC)

    # Calculate sun position
    elevation_deg, azimuth_pysolar = get_sun_position(latitude, longitude, when_utc)
    azimuth_north0 = convert_azimuth_pysolar_to_north0(azimuth_pysolar)

    # Print results
    print("========================================")
    print(f"Location:   Latitude={latitude:.6f}, Longitude={longitude:.6f}")
    print(f"Local TZ:   {args.tz}")
    print(f"Local Time: {local_dt}")
    print(f"UTC Time:   {when_utc}")
    print("----------------------------------------")
    print(f"Sun Elevation (above horizon): {elevation_deg:.2f}")
    print("----------------------------------------")
    print("Azimuth (PySolar convention):")
    print(f"   {azimuth_pysolar:.2f} [South=0, West=90, North=180, East=270]")
    print("Azimuth (North=0 convention):")
    print(f"   {azimuth_north0:.2f} [North=0, East=90, South=180, West=270]")
    print("========================================")

if __name__ == "__main__":
    main()
