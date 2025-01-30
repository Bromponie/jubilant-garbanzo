import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def draw_3d_celestial_sphere(observer_lat, observer_lon, celestial_objects):
    """
    Draws a 3D celestial sphere and plots celestial objects based on azimuth, altitude, and distance.
    
    Parameters:
    - observer_lat (float): Observer's latitude in degrees (-90 to +90).
    - observer_lon (float): Observer's longitude in degrees (-180 to +180).
    - celestial_objects (list of dict): List containing celestial objects with keys:
        - 'name' (str): Name of the celestial body.
        - 'azimuth' (float): Azimuth in degrees (0 = North, increasing clockwise).
        - 'altitude' (float): Altitude in degrees (0 = Horizon, +90 = Zenith).
        - 'distance' (float): Distance to the celestial body (arbitrary units).
    """
    
    # Validate observer's latitude and longitude
    if not (-90 <= observer_lat <= 90):
        raise ValueError("Latitude must be between -90 and +90 degrees.")
    if not (-180 <= observer_lon <= 180):
        raise ValueError("Longitude must be between -180 and +180 degrees.")
    
    # Create a new figure for 3D plotting
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Define celestial sphere parameters
    sphere_radius = 1  # Unit sphere for celestial sphere
    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
    x = sphere_radius * np.cos(u) * np.sin(v)
    y = sphere_radius * np.sin(u) * np.sin(v)
    z = sphere_radius * np.cos(v)
    
    # Plot the celestial sphere
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.1, edgecolor='none')
    
    # Plot the horizon plane based on observer's latitude
    # For simplicity, we'll assume the observer is at the origin looking towards the celestial sphere
    # and the horizon is the XY-plane. Adjustments can be made for more accurate representations.
    
    # Draw the horizon circle
    horizon_theta = np.linspace(0, 2*np.pi, 200)
    horizon_x = sphere_radius * np.cos(horizon_theta)
    horizon_y = sphere_radius * np.sin(horizon_theta)
    horizon_z = np.zeros_like(horizon_theta)
    ax.plot(horizon_x, horizon_y, horizon_z, color='k', linestyle='--', label='Horizon')
    
    # Draw zenith and nadir points
    ax.scatter(0, 0, sphere_radius, color='r', s=100, label='Zenith')
    ax.scatter(0, 0, -sphere_radius, color='b', s=100, label='Nadir')
    
    # Annotate cardinal directions on the horizon
    cardinal_points = ['N', 'E', 'S', 'W']
    cardinal_angles = [0, 90, 180, 270]  # Degrees
    for cp, angle in zip(cardinal_points, cardinal_angles):
        angle_rad = np.deg2rad(angle)
        x_cp = sphere_radius * np.cos(angle_rad)
        y_cp = sphere_radius * np.sin(angle_rad)
        z_cp = 0
        ax.text(x_cp, y_cp, z_cp, cp, fontsize=12, ha='center', va='center', color='k')
    
    # Plot celestial objects
    for obj in celestial_objects:
        name = obj.get('name', 'Object')
        az = obj.get('azimuth', 0)
        alt = obj.get('altitude', 0)
        dist = obj.get('distance', 1)
        
        # Convert azimuth and altitude to radians
        az_rad = np.deg2rad(az)
        alt_rad = np.deg2rad(alt)
        
        # Convert spherical coordinates (azimuth, altitude, distance) to Cartesian coordinates
        # Note: Altitude is measured from the horizon, so zenith is +90 degrees
        r = dist  # Distance to the celestial body
        x_obj = r * np.cos(alt_rad) * np.cos(az_rad)
        y_obj = r * np.cos(alt_rad) * np.sin(az_rad)
        z_obj = r * np.sin(alt_rad)
        
        # Plot the celestial object
        ax.scatter(x_obj, y_obj, z_obj, s=100, label=name)
        ax.text(x_obj, y_obj, z_obj, f" {name}", fontsize=10, color='k')
        
        # Optionally, draw a line from observer to celestial object
        ax.plot([0, x_obj], [0, y_obj], [0, z_obj], color='gray', linestyle=':', linewidth=0.5)
    
    # Set the aspect ratio to be equal
    ax.set_box_aspect([1,1,1])
    
    # Set labels
    ax.set_xlabel('East', fontsize=12)
    ax.set_ylabel('North', fontsize=12)
    ax.set_zlabel('Up', fontsize=12)
    
    # Set title with observer's location
    plt.title(f"3D Celestial Sphere\nObserver's Location: Latitude {observer_lat}, Longitude {observer_lon}", fontsize=14)
    
    # Set limits
    max_range = 1.2 * sphere_radius
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # Add legend
    ax.legend(loc='upper left')
    
    # Show grid
    ax.grid(True)
    
    # Show the plot
    plt.show()

# Example Usage
if __name__ == "__main__":
    # Observer's geographic coordinates
    observer_latitude = -25.8344     # Example: Los Angeles latitude
    observer_longitude = 28.2245  # Example: Los Angeles longitude

    
    # Define celestial objects to plot
    # For simplicity, distances are normalized (e.g., Moon ~ 0.00257 units if Earth is 1 unit)
    celestial_objects = [
        {
            'name': 'Moon',
            'azimuth': 260,      
            'altitude': 15,      
            'distance': 1.0      # Normalized distance (adjust as needed)
        }
    ]
    
    draw_3d_celestial_sphere(
        observer_lat=observer_latitude,
        observer_lon=observer_longitude,
        celestial_objects=celestial_objects
    )
