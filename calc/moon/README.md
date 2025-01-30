# jubilant-garbanzo

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)



# 3D Celestial Sphere Visualizer

![Celestial Sphere](https://i.imgur.com/YourImageLink.png) *(Replace with actual image if available)*

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

The **3D Celestial Sphere Visualizer** is a Python-based tool that provides an interactive 3D representation of the celestial sphere from an observer's vantage point on Earth. By inputting geographic coordinates (latitude and longitude) and specifying celestial objects with their respective azimuth, altitude, and distance, users can visualize the positions of stars, planets, the Moon, and other celestial bodies in a comprehensive 3D environment.

This tool is ideal for astronomy enthusiasts, educators, and developers looking to explore celestial mechanics, plan observations, or integrate celestial visualizations into larger projects.

## Features

- **Interactive 3D Visualization:** Rotate, zoom, and explore the celestial sphere from any angle.
- **Customizable Celestial Objects:** Plot multiple celestial bodies by specifying their azimuth, altitude, and distance.
- **Observer's Geographic Coordinates:** Accurately represents the sky based on the observer's latitude and longitude.
- **Cardinal Directions:** Clearly marked North, East, South, and West on the horizon for orientation.
- **Zenith and Nadir Markers:** Easily identify the points directly overhead and beneath the observer.
- **Scalable Distance Representation:** Normalize distances to visualize celestial objects proportionally.

## Demo

![3D Celestial Sphere Demo](https://i.imgur.com/YourDemoImageLink.gif) *(Replace with actual GIF or image if available)*

*Note: Interactive 3D plots can be rotated and zoomed using mouse controls.*

## Installation

### Prerequisites

- **Python 3.6 or higher**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/yourusername/3d-celestial-sphere.git
cd 3d-celestial-sphere





# Observer's geographic coordinates
observer_latitude = 34.05     # Example: Los Angeles latitude
observer_longitude = -118.25  # Example: Los Angeles longitude

# Define celestial objects to plot
celestial_objects = [
    {
        'name': 'Moon',
        'azimuth': 135,     # Southeast
        'altitude': 45,     # 45 degrees above the horizon
        'distance': 1.0     # Normalized distance
    },
    {
        'name': 'Star A',
        'azimuth': 210,     # Southwest
        'altitude': 30,     # 30 degrees above the horizon
        'distance': 1.2
    },
    {
        'name': 'Planet X',
        'azimuth': 75,      # East-Northeast
        'altitude': 60,     # 60 degrees above the horizon
        'distance': 0.8
    }
]
