import random
import math

# ----- GA Parameters -----
NUM_CITIES = 10
POP_SIZE = 50
NUM_GENERATIONS = 500
TOURNAMENT_SIZE = 5
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
ELITISM = True

# ----- Helper Functions -----
def generate_cities(num_cities):
    """
    Generates random cities with (x, y) coordinates.
    """
    cities = []
    for _ in range(num_cities):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        cities.append((x, y))
    return cities

def distance(city1, city2):
    """
    Calculates Euclidean distance between two cities.
    """
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def total_distance(route, cities):
    """
    Computes the total distance of the route. The route is assumed to be a cycle.
    """
    total = 0
    for i in range(len(route)):
        city_index1 = route[i]
        city_index2 = route[(i + 1) % len(route)]  # Wrap-around to form a cycle.
        total += distance(cities[city_index1], cities[city_index2])
    return total

def fitness(route, cities):
    """
    Fitness is defined as the reciprocal of the total distance.
    """
    d = total_distance(route, cities)
    return 1 / d if d > 0 else float('inf')

# ----- Population Initialization -----
def init_population(pop_size, num_cities):
    """
    Creates a population of random routes (permutations of city indices).
    """
    population = []
    base = list(range(num_cities))
    for _ in range(pop_size):
        individual = base[:]  # Copy the list of cities.
        random.shuffle(individual)
        population.append(individual)
    return population

# ----- Selection -----
def tournament_selection(population, cities, tournament_size):
    """
    Performs tournament selection by randomly choosing a subset of individuals
    and returning the one with the lowest route distance.
    """
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda route: total_distance(route, cities))
    return tournament[0][:]  # Return a copy of the best individual in the tournament.

# ----- Crossover (Order Crossover) -----
def order_crossover(parent1, parent2):
    """
    Implements the Order Crossover (OX) operator for permutations.
    """
    size = len(parent1)
    child = [None] * size

    # Choose two random crossover points.
    start, end = sorted(random.sample(range(size), 2))

    # Copy the subsequence from parent1 to child.
    child[start:end+1] = parent1[start:end+1]

    # Fill the remaining positions with the order of cities from parent2,
    # skipping those already in the child.
    current_index = (end + 1) % size
    parent2_index = (end + 1) % size
    while None in child:
        if parent2[parent2_index] not in child:
            child[current_index] = parent2[parent2_index]
            current_index = (current_index + 1) % size
        parent2_index = (parent2_index + 1) % size

    return child

# ----- Mutation (Swap Mutation) -----
def swap_mutation(individual):
    """
    Randomly swaps two cities in the route.
    """
    a, b = random.sample(range(len(individual)), 2)
    individual[a], individual[b] = individual[b], individual[a]
    return individual

# ----- Genetic Algorithm -----
def genetic_algorithm(cities, pop_size, num_generations, tournament_size,
                      crossover_rate, mutation_rate, elitism):
    population = init_population(pop_size, len(cities))
    best_route = None
    best_distance = float('inf')

    for generation in range(num_generations):
        new_population = []

        # ----- Elitism: Preserve the best individual -----
        if elitism:
            population.sort(key=lambda route: total_distance(route, cities))
            best_in_population = population[0][:]
            if total_distance(best_in_population, cities) < best_distance:
                best_distance = total_distance(best_in_population, cities)
                best_route = best_in_population[:]
            new_population.append(best_in_population)

        # ----- Create new offspring -----
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, cities, tournament_size)
            parent2 = tournament_selection(population, cities, tournament_size)

            # Crossover
            if random.random() < crossover_rate:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]  # Copy if no crossover

            # Mutation
            if random.random() < mutation_rate:
                child = swap_mutation(child)

            new_population.append(child)

        population = new_population

        # ----- Optionally print progress -----
        if generation % 50 == 0:
            print(f"Generation {generation}: Best distance so far = {best_distance:.2f}")

    return best_route, best_distance

# ----- Main Function -----
def main():
    # Generate random cities.
    cities = generate_cities(NUM_CITIES)
    print("City coordinates:")
    for idx, city in enumerate(cities):
        print(f"City {idx}: {city}")

    # Run the genetic algorithm.
    best_route, best_route_distance = genetic_algorithm(
        cities,
        POP_SIZE,
        NUM_GENERATIONS,
        TOURNAMENT_SIZE,
        CROSSOVER_RATE,
        MUTATION_RATE,
        ELITISM
    )

    # Print the best route found.
    print("\nFinal Best Route (order of city indices):")
    print(best_route)
    print(f"Total route distance: {best_route_distance:.2f}")

if __name__ == '__main__':
    main()
