import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from geopy.distance import geodesic

# Define the cities dictionary with coordinates
cities = {
    "Seattle": (47.608013, -122.335167),
    "Boise": (43.616616, -116.200886),
    "Everett": (47.967306, -122.201399),
    "Pendleton": (45.672075, -118.788597),
    "Biggs": (45.669846, -120.832841),
    "Portland": (45.520247, -122.674194),
    "Twin Falls": (42.570446, -114.460255),
    "Bend": (44.058173, -121.315310),
    "Spokane": (47.657193, -117.423510),
    "Grant Pass": (42.441561, -123.339336),
    "Burns": (43.586126, -119.054413),
    "Eugene": (44.050505, -123.095051),
    "Lakeview": (42.188772, -120.345792),
    "Missoula": (46.870105, -113.995267)
}

# Ensure Seattle is always the first city in the route
def create_route():
    city_names = list(cities.keys())
    city_names.remove('Seattle')  # Remove Seattle from the list
    random.shuffle(city_names)  # Shuffle the remaining cities
    return [0] + [city_names.index(city) + 1 for city in city_names]  # Seattle is index 0

# The evaluation function
def evaluate(individual):
    distance = 0
    city_names = ['Seattle'] + [city for city in cities if city != 'Seattle']
    for i in range(len(individual) - 1):
        city1 = city_names[individual[i]]
        city2 = city_names[individual[i+1]]
        distance += geodesic(cities[city1], cities[city2]).kilometers
    # Add distance from last city back to Seattle
    last_city = city_names[individual[-1]]
    distance += geodesic(cities[last_city], cities['Seattle']).kilometers
    return distance,



# Set up the genetic algorithm
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(cities)), len(cities)) # Randomly sample indices
toolbox.register("individual", tools.initIterate, creator.Individual, create_route)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/(len(cities)-1))
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("evaluate", evaluate)

# Main function to run the genetic algorithm
def main():
    random.seed(42)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(5)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.90, mutpb=0.1, ngen=200, stats=stats, halloffame=hof)
    
    return pop, stats, hof

# Function to plot the route
def plot_route(route):
    city_names = ['Seattle'] + [city for city in cities if city != 'Seattle']
    x = [cities[city_names[i]][1] for i in route]
    y = [cities[city_names[i]][0] for i in route]
    
    # Add Seattle at the end to close the loop
    x.append(x[0])
    y.append(y[0])

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red')
    plt.plot(x, y, linestyle='-')
    for i, city in enumerate(city_names):
        plt.text(cities[city][1], cities[city][0], city)
    plt.show()

# Function to print the route
def print_route(route):
    city_names = ['Seattle'] + [city for city in cities if city != 'Seattle']
    route_names = [city_names[i] for i in route] + ['Seattle']
    print(" -> ".join(route_names))

# Run the genetic algorithm
if __name__ == "__main__":
    _, _, hof = main()
    best_route = hof[0]
    print("Best route:")
    print_route(best_route)
    print(f"Total distance: {evaluate(best_route)[0]:.2f} km")
    plot_route(best_route)
