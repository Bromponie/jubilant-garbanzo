import sys
import argparse
import datetime
import pytz
from pysolar.solar import get_altitude, get_azimuth

def get_sun_position(latitude, longitude, when_utc=None):
    """
    Calculate the sun's elevation (altitude) and azimuth for a given location and time (UTC).

    :param latitude:  Latitude in decimal degrees  (float).
    :param longitude: Longitude in decimal degrees (float).
    :param when_utc:  A datetime object in UTC. If None, uses the current UTC time.
    :return: (elevation_degrees, azimuth_degrees)
             elevation_degrees = angle above the horizon in degrees
             azimuth_degrees   = angle measured from South=0, West=90, North=180, East=270 by default in PySolar
    """
    if when_utc is None:
        when_utc = datetime.datetime.now(tz=pytz.UTC)

    # Elevation (altitude) is the angle above the horizon in degrees
    elevation_degrees = get_altitude(latitude, longitude, when_utc)

    # Azimuth is the compass direction (in PySolars default convention)
    azimuth_degrees = get_azimuth(latitude, longitude, when_utc)

    return elevation_degrees, azimuth_degrees

def convert_azimuth_pysolar_to_north0(azimuth_south0):
    """
    Convert PySolars azimuth (South=0, West=90, North=180, East=270)
    to a more conventional system where North=0, East=90, South=180, West=270.

    :param azimuth_south0: Azimuth in PySolar convention (float).
    :return: Azimuth in conventional "North=0" system (float).
    """
    # In PySolar, 0 = South. We want 0 = North.
    # So the offset is 180 (to make South=180) plus or minus some wrapping.
    # One simple formula is:
    az_north0 = azimuth_south0 + 180.0
    # But we must wrap it back into [0, 360).
    az_north0 = az_north0 % 360.0
    return az_north0

def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Calculate the sun's elevation and azimuth for a given location and time."
    )
    parser.add_argument("--lat", type=float, default=-25.826629230519135,
                        help="Latitude in decimal degrees (default: -25.826629230519135)")
    parser.add_argument("--lon", type=float, default=28.223651260896336,
                        help="Longitude in decimal degrees (default: 28.223651260896336)")
    parser.add_argument("--date", default=None,
                        help="Local date in YYYY-MM-DD format (default: today's date)")
    parser.add_argument("--time", default=None,
                        help="Local time in HH:MM (24-hour) format (default: current local time)")
    parser.add_argument("--tz", default="Africa/Johannesburg",
                        help="Local time zone (default: Africa/Johannesburg)")

    args = parser.parse_args()

    latitude = args.lat
    longitude = args.lon

    # If user does not provide date/time, we assume "now" in local tz
    local_tz = pytz.timezone(args.tz)

    if args.date and args.time:
        # User provided date and time
        date_str = args.date
        time_str = args.time
        # Parse them into a datetime object with the specified local time zone
        local_dt_str = f"{date_str} {time_str}"
        local_format = "%Y-%m-%d %H:%M"
        local_dt = datetime.datetime.strptime(local_dt_str, local_format)
        local_dt = local_tz.localize(local_dt)
    elif args.date and not args.time:
        # User provided date, but not time - assume midnight local
        date_str = args.date
        local_format = "%Y-%m-%d"
        local_dt = datetime.datetime.strptime(date_str, local_format)
        local_dt = local_tz.localize(local_dt)
    else:
        # Neither date nor time provided: use current local time
        local_dt = datetime.datetime.now(tz=local_tz)

    # Convert local time to UTC
    when_utc = local_dt.astimezone(pytz.UTC)

    # Calculate sun position
    elevation_deg, azimuth_pysolar = get_sun_position(latitude, longitude, when_utc)

    # Convert PySolars azimuth to the more typical North=0, East=90 system
    azimuth_north0 = convert_azimuth_pysolar_to_north0(azimuth_pysolar)

    # Print results
    print("========================================")
    print(f"Location:  Latitude={latitude:.6f}, Longitude={longitude:.6f}")
    print(f"Local TZ:  {args.tz}")
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
    # If you dont want command-line usage, you could directly call main() 
    # or skip parser logic. For demonstration, we leave it as is.
    main()
