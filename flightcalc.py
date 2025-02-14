import argparse
from datetime import datetime, timedelta

# Use zoneinfo for timezone support (Python 3.9+)
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # For older Python versions, install backports.zoneinfo:
    # pip install backports.zoneinfo
    from backports.zoneinfo import ZoneInfo


def parse_datetime(dt_str: str, tz_str: str) -> datetime:
    """
    Parse a datetime string and assign the provided timezone.

    Parameters:
        dt_str (str): Date and time in "YYYY-MM-DD HH:MM" format.
        tz_str (str): Timezone string (e.g., "America/New_York").

    Returns:
        datetime: A timezone-aware datetime object.
    """
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {dt_str}. Expected 'YYYY-MM-DD HH:MM'.") from e

    try:
        tz = ZoneInfo(tz_str)
    except Exception as e:
        raise ValueError(f"Invalid timezone: {tz_str}.") from e

    return dt.replace(tzinfo=tz)


def flight_duration(departure: datetime, arrival: datetime) -> (int, int):
    """
    Calculate the flight duration given departure and arrival datetimes.

    Both datetime objects must be timezone-aware.
    
    Parameters:
        departure (datetime): Departure time.
        arrival (datetime): Arrival time.

    Returns:
        (int, int): Tuple containing hours and minutes of duration.
    """
    # Convert both times to UTC for an accurate difference calculation.
    duration = arrival.astimezone(ZoneInfo("UTC")) - departure.astimezone(ZoneInfo("UTC"))
    
    if duration < timedelta(0):
        raise ValueError("Arrival time must be after departure time.")

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return hours, minutes


def layover_duration(prev_arrival: datetime, next_departure: datetime) -> (int, int):
    """
    Calculate the layover duration between two flights.

    Parameters:
        prev_arrival (datetime): Arrival time of the previous flight.
        next_departure (datetime): Departure time of the next flight.

    Returns:
        (int, int): Tuple containing hours and minutes of layover duration.
    """
    duration = next_departure.astimezone(ZoneInfo("UTC")) - prev_arrival.astimezone(ZoneInfo("UTC"))
    
    if duration < timedelta(0):
        raise ValueError("Next departure time must be after previous arrival time.")
    
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return hours, minutes


def main():
    parser = argparse.ArgumentParser(
        description="Calculate flight duration and layover durations considering time zones."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command: 'flight' or 'layover'.")

    # Subparser for flight duration calculation
    flight_parser = subparsers.add_parser("flight", help="Calculate flight duration.")
    flight_parser.add_argument("--dep_time", type=str, required=True,
                               help="Departure time in 'YYYY-MM-DD HH:MM' format.")
    flight_parser.add_argument("--dep_zone", type=str, required=True,
                               help="Departure timezone (e.g., 'America/New_York').")
    flight_parser.add_argument("--arr_time", type=str, required=True,
                               help="Arrival time in 'YYYY-MM-DD HH:MM' format.")
    flight_parser.add_argument("--arr_zone", type=str, required=True,
                               help="Arrival timezone (e.g., 'Europe/London').")

    # Subparser for layover duration calculation
    layover_parser = subparsers.add_parser("layover", help="Calculate layover duration between flights.")
    layover_parser.add_argument("--prev_arr", type=str, required=True,
                                help="Previous flight arrival time in 'YYYY-MM-DD HH:MM' format.")
    layover_parser.add_argument("--prev_arr_zone", type=str, required=True,
                                help="Previous flight arrival timezone.")
    layover_parser.add_argument("--next_dep", type=str, required=True,
                                help="Next flight departure time in 'YYYY-MM-DD HH:MM' format.")
    layover_parser.add_argument("--next_dep_zone", type=str, required=True,
                                help="Next flight departure timezone.")

    args = parser.parse_args()

    try:
        if args.command == "flight":
            departure = parse_datetime(args.dep_time, args.dep_zone)
            arrival = parse_datetime(args.arr_time, args.arr_zone)
            hours, minutes = flight_duration(departure, arrival)
            print(f"Flight duration: {hours} hours and {minutes} minutes")
        elif args.command == "layover":
            prev_arrival = parse_datetime(args.prev_arr, args.prev_arr_zone)
            next_departure = parse_datetime(args.next_dep, args.next_dep_zone)
            hours, minutes = layover_duration(prev_arrival, next_departure)
            print(f"Layover duration: {hours} hours and {minutes} minutes")
    except ValueError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
