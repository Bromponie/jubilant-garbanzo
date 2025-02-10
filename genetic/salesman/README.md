---

# Traveling Salesman Problem (TSP) Genetic Algorithm

This project implements a Genetic Algorithm (GA) to solve the classic Traveling Salesman Problem (TSP) for 10 cities. The algorithm evolves a population of candidate solutions (routes) over multiple generations to find a near-optimal solution that minimizes the total travel distance.

## Overview

The TSP is a well-known NP-hard problem where the goal is to determine the shortest possible route that visits a set of cities exactly once and returns to the origin city. Although a brute-force solution is feasible for 10 cities, this project demonstrates how a GA can be structured to address larger instances of the TSP.

## Features

- **Random City Generation:** Cities are generated with random (x, y) coordinates.
- **Permutation-Based Encoding:** Each candidate solution is a permutation of city indices.
- **Order Crossover (OX):** A crossover operator designed for permutation-based representations.
- **Swap Mutation:** A mutation operator that swaps two cities in the route.
- **Tournament Selection:** Parents are selected using tournament selection.
- **Elitism:** The best solution is preserved across generations to ensure quality improvement.
- **Progress Output:** Prints progress every 50 generations.

## File Structure

```
.
├── README.md
└── tsp_ga.py
```

- **tsp_ga.py:** Contains the complete Python implementation of the GA for TSP.

## Requirements

- **Python 3.6+**

No external packages are required; the implementation uses Python's standard libraries (`random`, `math`).

## How to Run

1. **Clone the repository or download the `tsp_ga.py` file.**
2. **Open a terminal** and navigate to the directory containing `tsp_ga.py`.
3. **Run the script:**

   ```bash
   python tsp_ga.py
   ```

   The script will generate 10 random cities, run the genetic algorithm for a preset number of generations, and then output the best route found along with its total distance.

## Configuration

The algorithm's parameters can be adjusted at the top of the `tsp_ga.py` file:

- **NUM_CITIES:** Number of cities (default: 10)
- **POP_SIZE:** Population size (default: 50)
- **NUM_GENERATIONS:** Total number of generations (default: 500)
- **TOURNAMENT_SIZE:** Number of individuals in tournament selection (default: 5)
- **CROSSOVER_RATE:** Probability of performing crossover (default: 0.8)
- **MUTATION_RATE:** Probability of performing mutation (default: 0.2)
- **ELITISM:** Set to `True` to preserve the best solution across generations

Feel free to modify these parameters to experiment with different settings and observe how they affect the algorithm's performance.

## How It Works

1. **Initialization:**  
   A population of random routes (permutations of city indices) is generated.

2. **Fitness Evaluation:**  
   The fitness of each route is calculated as the reciprocal of its total distance (using Euclidean distance).

3. **Selection:**  
   Tournament selection is used to choose parents for reproduction.

4. **Crossover and Mutation:**  
   - **Order Crossover (OX):** Combines parts of two parent routes to create a new route.
   - **Swap Mutation:** Randomly swaps two cities in the route to introduce variation.

5. **Elitism and Replacement:**  
   The best individual is preserved (if elitism is enabled), and a new population is generated for the next generation.

6. **Iteration:**  
   The process is repeated for a fixed number of generations, and progress is printed every 50 generations.

7. **Output:**  
   Once the GA terminates, the best route and its total distance are printed.

## License

This project is provided for educational purposes. You may use and modify the code as needed.

## Author
Brom

---
