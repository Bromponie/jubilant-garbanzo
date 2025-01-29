import argparse
import datetime
from astral import LocationInfo
from astral.sun import sun
import pytz

def parse_date(date_str):
    """Parse a date string in YYYY-MM-DD format into a date object."""
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

def format_timedelta(delta):
    """Convert a timedelta into a human-readable string of hours and minutes."""
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m"

def main():
    parser = argparse.ArgumentParser(description='Calculate solar events and daylight information.')
    parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--lat', type=float, help='Latitude of the location (default: Pretoria)')
    parser.add_argument('--lon', type=float, help='Longitude of the location (default: Pretoria)')
    args = parser.parse_args()

    # Date handling
    try:
        date = parse_date(args.date) if args.date else datetime.date.today()
    except ValueError as e:
        print(e)
        return

    # Location configuration
    if args.lat and args.lon:
        location = LocationInfo(
            name="Custom Location",
            region="Custom",
            timezone="Africa/Johannesburg",
            latitude=args.lat,
            longitude=args.lon
        )
    else:
        # Default to Pretoria coordinates
        location = LocationInfo(
            name="Pretoria",
            region="South Africa",
            timezone="Africa/Johannesburg",
            latitude=-25.8266,
            longitude=28.2237
        )

    tz = pytz.timezone(location.timezone)

    try:
        solar_events = sun(location.observer, date=date, tzinfo=tz)
    except Exception as e:
        print(f"Error calculating solar events: {e}")
        return

    # Calculate time durations
    daylight = solar_events['sunset'] - solar_events['sunrise']
    dawn = solar_events['sunrise'] - solar_events['dawn']
    dusk = solar_events['dusk'] - solar_events['sunset']

    # Display results
    print(f"\n{' Solar Events ':-^40}")
    print(f"Location: {location.name} ({location.latitude:.4f}N, {location.longitude:.4f}E)")
    print(f"Date: {date.strftime('%Y-%m-%d')}")
    print(f"Timezone: {location.timezone}\n")

    for event, time in solar_events.items():
        print(f"{event.capitalize():<10}: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    print(f"\n{' Durations ':-^40}")
    print(f"Daylight Hours  : {format_timedelta(daylight)}")
    print(f"Morning Twilight: {format_timedelta(dawn)}")
    print(f"Evening Twilight: {format_timedelta(dusk)}")

    # Current status and predictions
    if date == datetime.date.today():
        now = datetime.datetime.now(tz)
        print(f"\n{' Current Status ':-^40}")

        if solar_events['sunrise'] < now < solar_events['sunset']:
            print("?? The sun is currently up")
            time_left = solar_events['sunset'] - now
            print(f"Time until sunset: {format_timedelta(time_left)}")
        else:
            print("?? The sun is currently down")
            if now < solar_events['sunrise']:
                time_left = solar_events['sunrise'] - now
                print(f"Time until sunrise: {format_timedelta(time_left)}")
            else:
                # Calculate tomorrow's sunrise
                tomorrow = date + datetime.timedelta(days=1)
                try:
                    tomorrow_events = sun(location.observer, date=tomorrow, tzinfo=tz)
                    time_left = tomorrow_events['sunrise'] - now
                    print(f"Time until next sunrise: {format_timedelta(time_left)} (tomorrow)")
                except Exception as e:
                    print(f"Could not calculate tomorrow's sunrise: {e}")

if __name__ == "__main__":
    main()