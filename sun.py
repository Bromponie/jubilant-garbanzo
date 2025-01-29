import datetime
import pytz
from pysolar.solar import get_altitude, get_azimuth

def get_sun_position(latitude, longitude, when_utc=None):
    """
    Calculate the sun's elevation (altitude) and azimuth for a given location and time.
    
    :param latitude:  Latitude in decimal degrees  (float)
    :param longitude: Longitude in decimal degrees (float)
    :param when_utc:  A datetime object (UTC). If None, uses the current UTC time.
    :return: (elevation_degrees, azimuth_degrees)
             elevation_degrees = angle above the horizon (degrees)
             azimuth_degrees   = angle measured from South=0, West=90, North=180, East=270 by default in PySolar
    """
    if when_utc is None:
        when_utc = datetime.datetime.now(tz=pytz.UTC)
    
    # altitude: angle above the horizon (in degrees)
    elevation_degrees = get_altitude(latitude, longitude, when_utc)
    
    # azimuth: angle measured from South=0, West=90, North=180, East=270
    azimuth_degrees = get_azimuth(latitude, longitude, when_utc)
    
    return elevation_degrees, azimuth_degrees

if __name__ == "__main__":
    # Coordinates for the location
    latitude = -25.826629230519135
    longitude = 28.223651260896336
    
    # Let's pick a sample UTC time. If you prefer local time, convert it to UTC first.
    # For demonstration, we'll just use "now" in UTC.
    now_utc = datetime.datetime.now(tz=pytz.UTC)
    
    elevation, azimuth = get_sun_position(latitude, longitude, now_utc)
    
    print(f"Date/Time (UTC): {now_utc}")
    print(f"Sun Elevation  : {elevation:.2f} above horizon")
    print(f"Sun Azimuth    : {azimuth:.2f} (PySolar convention: 0=South, 90=West, 180=North, 270=East)")
