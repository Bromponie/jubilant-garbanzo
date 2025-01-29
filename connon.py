import math
import time
import random
import keyboard
import matplotlib.pyplot as plt
import logging
from dataclasses import dataclass

# -------------------------
#  CONFIGURATION CLASSES
# -------------------------
@dataclass
class GameConfig:
    min_target_dist: float = 50_000.0  # 50 km
    max_target_dist: float = 300_000.0  # 300 km
    target_radius: float = 1000.0
    projectile_speed: float = 1500.0  # More realistic for long-range artillery
    max_sim_time: float = 600.0  # 10 minutes
    time_step: float = 0.1
    gravity: float = 9.81
    air_density: float = 1.225  # kg/m3
    projectile_diameter: float = 0.155  # 155mm artillery shell
    drag_coefficient: float = 0.3
    earth_rotation_rate: float = 7.2921e-5  # rad/s

# -------------------------
#  PHYSICS MODEL
# -------------------------
class ProjectileSimulator:
    def __init__(self, config: GameConfig):
        self.config = config
        self.cross_sectional_area = math.pi * (config.projectile_diameter/2)**2
        self.base_drag_coeff = 0.5 * config.air_density * config.drag_coefficient * self.cross_sectional_area

    def calculate_drag(self, velocity, wind_speed):
        """Calculate drag force using quadratic drag model"""
        relative_velocity = velocity - wind_speed
        speed_sq = relative_velocity**2
        return -self.base_drag_coeff * speed_sq * math.copysign(1, relative_velocity)

    def coriolis_acceleration(self, velocity, latitude=45.0):
        """Calculate Coriolis effect acceleration components"""
        lat_rad = math.radians(latitude)
        return (
            2 * self.config.earth_rotation_rate * velocity[1] * math.sin(lat_rad),
            -2 * self.config.earth_rotation_rate * velocity[0] * math.sin(lat_rad)
        )

    def simulate_shot(self, launch_angle_deg, target_dist, wind_speed=0.0, drag=True, coriolis=True):
        """Improved simulation with wind, drag, and Coriolis effects"""
        angle_rad = math.radians(launch_angle_deg)
        vx = self.config.projectile_speed * math.cos(angle_rad)
        vy = self.config.projectile_speed * math.sin(angle_rad)

        x, y, t = 0.0, 0.0, 0.0
        trajectory = []

        while t < self.config.max_sim_time:
            trajectory.append((x, y))
            
            if y < 0:
                break

            # Calculate forces
            drag_x = self.calculate_drag(vx, wind_speed) if drag else 0
            drag_y = self.calculate_drag(vy, 0) if drag else 0

            coriolis_x, coriolis_y = self.coriolis_acceleration((vx, vy)) if coriolis else (0, 0)

            # Update accelerations
            ax = (drag_x / self.config.projectile_speed) + coriolis_x
            ay = (-self.config.gravity) + (drag_y / self.config.projectile_speed) + coriolis_y

            # Euler integration
            vx += ax * self.config.time_step
            vy += ay * self.config.time_step
            x += vx * self.config.time_step
            y += vy * self.config.time_step
            t += self.config.time_step

        # Calculate precise impact point
        if len(trajectory) > 1 and y < 0:
            x_prev, y_prev = trajectory[-2]
            frac = -y_prev / (y - y_prev)
            impact_x = x_prev + frac * (x - x_prev)
        else:
            impact_x = x

        return trajectory, impact_x

# -------------------------
#  GAME MECHANICS
# -------------------------
class ArtilleryGame:
    def __init__(self, config: GameConfig):
        self.config = config
        self.simulator = ProjectileSimulator(config)
        
    def propose_angle(self, target_dist, wind_speed=0.0, drag=True, coriolis=True):
        """Improved angle suggestion with physics considerations"""
        # Base vacuum trajectory solution
        max_range = (self.config.projectile_speed**2)/self.config.gravity
        if target_dist > max_range:
            return None  # Impossible shot
        
        # Iterative solution with drag approximation
        angle_deg = 45.0
        for _ in range(5):  # Simple convergence loop
            _, impact = self.simulator.simulate_shot(angle_deg, target_dist, wind_speed, drag, coriolis)
            error = impact - target_dist
            angle_deg += math.copysign(0.5, -error)
            
        return max(15.0, min(75.0, angle_deg))

    def run_game_loop(self):
        """Main game loop with improved controls"""
        config = self.config
        
        while True:
            # Generate random scenario
            target_dist = random.uniform(config.min_target_dist, config.max_target_dist)
            wind_speed = random.uniform(-50, 50)
            drag_enabled = random.choice([True, False])
            coriolis_enabled = random.choice([True, False])
            
            # Get initial angle suggestion
            suggested_angle = self.propose_angle(
                target_dist, wind_speed, drag_enabled, coriolis_enabled
            ) or 45.0

            current_angle = suggested_angle
            
            print("\n=== New Round ===")
            print(f"Target: {target_dist/1000:.1f} km")
            print(f"Wind: {wind_speed:.1f} m/s {'east' if wind_speed >0 else 'west'}")
            print(f"Drag: {'ON' if drag_enabled else 'OFF'}")
            print(f"Coriolis: {'ON' if coriolis_enabled else 'OFF'}")
            print(f"Suggested angle: {suggested_angle:.1f}")
            print("Controls: W/S - adjust angle, SPACE - fire, Q - quit")

            # Angle adjustment loop
            while True:
                # Handle input
                if keyboard.is_pressed('w'):
                    current_angle = min(85.0, current_angle + 0.5)
                if keyboard.is_pressed('s'):
                    current_angle = max(15.0, current_angle - 0.5)
                if keyboard.is_pressed('space'):
                    break
                if keyboard.is_pressed('q'):
                    return

                # Display current angle
                print(f"\rCurrent angle: {current_angle:.1f}", end='')
                time.sleep(0.02)

            # Run simulation
            trajectory, impact_x = self.simulator.simulate_shot(
                current_angle, target_dist, wind_speed, drag_enabled, coriolis_enabled
            )
            
            # Calculate results
            distance_error = abs(impact_x - target_dist)
            result = "DIRECT HIT!" if distance_error <= config.target_radius else "MISS"
            
            print(f"\nImpact at {impact_x/1000:.1f} km ({distance_error/1000:.1f} km error)")
            print(f"Result: {result}")

            # Plot trajectory
            plt.figure(figsize=(12, 6))
            plt.plot([x for x, y in trajectory], [y for x, y in trajectory])
            plt.scatter([target_dist], [0], c='red', s=100)
            plt.title(f"Shot Trajectory ({current_angle:.1f})")
            plt.xlabel("Distance (m)")
            plt.ylabel("Altitude (m)")
            plt.grid(True)
            plt.show()

if __name__ == "__main__":
    config = GameConfig()
    game = ArtilleryGame(config)
    game.run_game_loop()