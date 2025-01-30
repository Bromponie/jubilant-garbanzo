import requests  # Import the requests library to handle HTTP requests

def get_elevation(lat, lon):
    """
    Query the Open-Elevation API for the elevation at a specific latitude and longitude.
    
    :param lat: Latitude (float) - The geographical latitude of the location.
    :param lon: Longitude (float) - The geographical longitude of the location.
    :return: Elevation in meters (float) if successful, or None if an error occurs.
    """
    # Define the endpoint URL for the Open-Elevation API
    url = "https://api.open-elevation.com/api/v1/lookup"
    
    # Prepare the parameters for the GET request
    # The 'locations' parameter expects a string in the format "latitude,longitude"
    params = {
        "locations": f"{lat},{lon}"
    }
    
    try:
        # Send a GET request to the Open-Elevation API with the specified parameters
        response = requests.get(url, params=params)
        
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        
        # Parse the JSON response from the API
        data = response.json()
        
        # Extract the 'results' list from the JSON data
        # The API returns a list of results, each containing elevation data for a location
        results = data.get("results")
        
        # Check if the 'results' list is empty or not present
        if not results:
            print("No results found in the API response.")
            return None  # Return None to indicate that elevation data could not be retrieved
        
        # Since we queried for a single location, we expect only one result in the list
        # Extract the 'elevation' value from the first (and only) result
        elevation = results[0].get("elevation")
        
        # Return the elevation value in meters
        return elevation
    
    except requests.RequestException as e:
        # Catch any exceptions related to the HTTP request (e.g., network issues, invalid responses)
        print(f"Error fetching data from Open-Elevation: {e}")
        return None  # Return None to indicate that an error occurred

# The following block ensures that the example usage only runs when the script is executed directly
if __name__ == "__main__":
    # Example coordinates (latitude and longitude) for which to fetch elevation data
    # Uncomment the following lines to use different coordinates:
    # latitude = -25.826629230519135
    # longitude = 28.223651260896336
    
    # Current example coordinates
    latitude = 32.692984377272045  # Latitude of the location
    longitude = 79.27440843846019  # Longitude of the location
    
    # Call the get_elevation function with the specified latitude and longitude
    elevation_meters = get_elevation(latitude, longitude)
    
    # Check if the elevation was successfully retrieved
    if elevation_meters is not None:
        # Print the elevation in a formatted string
        print(f"Elevation for {latitude}, {longitude} = {elevation_meters} meters above sea level")
    else:
        # Inform the user that the elevation could not be determined
        print("Could not determine elevation.")
