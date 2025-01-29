import datetime
from astral import LocationInfo
from astral.sun import sun

# Coordinates for the location
latitude = -25.826629230519135
longitude = 28.223651260896336

# Create a location object
location = LocationInfo(
    name="Pretoria",
    region="South Africa",
    timezone="Africa/Johannesburg",
    latitude=latitude,
    longitude=longitude
)

# Use today's date or any other date of your choice
date = datetime.date.today()

# Calculate sunrise, sunset (and other sun events if needed)
s = sun(location.observer, date=date, tzinfo=location.timezone)

print(f"Date       : {date}")
print(f"Sunrise    : {s['sunrise']}")
print(f"Sunset     : {s['sunset']}")
print(f"Noon       : {s['noon']}")
print(f"Dawn       : {s['dawn']}")
print(f"Dusk       : {s['dusk']}")
