import requests  # Import the requests library to handle HTTP requests
import argparse  # Import argparse to parse command-line arguments
import sys  # Import sys for system-specific parameters and functions

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

def parse_arguments():
    """
    Parse command-line arguments for latitude and longitude.
    
    :return: Namespace containing latitude and longitude.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve elevation data for specified latitude and longitude using the Open-Elevation API."
    )
    
    # Define the latitude argument
    parser.add_argument(
        '--lat',
        type=float,
        required=True,
        help='Latitude of the location (e.g., 32.692984377272045)'
    )
    
    # Define the longitude argument
    parser.add_argument(
        '--lon',
        type=float,
        required=True,
        help='Longitude of the location (e.g., 79.27440843846019)'
    )
    
    return parser.parse_args()

# The following block ensures that the example usage only runs when the script is executed directly
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()
    
    latitude = args.lat  # Latitude provided via command line
    longitude = args.lon  # Longitude provided via command line
    
    # Call the get_elevation function with the specified latitude and longitude
    elevation_meters = get_elevation(latitude, longitude)
    
    # Check if the elevation was successfully retrieved
    if elevation_meters is not None:
        # Print the elevation in a formatted string
        print(f"Elevation for {latitude}, {longitude} = {elevation_meters} meters above sea level")
    else:
        # Inform the user that the elevation could not be determined
        print("Could not determine elevation.")
        sys.exit(1)  # Exit the script with a non-zero status to indicate failure
