import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from pyproj import Proj
from customAlgorithms import custom_eaSimple


city_mapping = {
    0: ["Seattle", (47.608013, -122.335167)],
    1: ["Boise", (43.616616, -116.200886)],
    2: ["Everett", (47.967306, -122.201399)],
    3: ["Pendleton", (45.672075, -118.788597)],
    4: ["Biggs", (45.669846, -120.832841)],
    5: ["Portland", (45.520247, -122.674194)],
    6: ["Twin Falls", (42.570446, -114.460255)],
    7: ["Bend", (44.058173, -121.315310)],
    8: ["Spokane", (47.657193, -117.423510)],
    9: ["Grant Pass", (42.441561, -123.339336)],
    10: ["Burns", (43.586126, -119.054413)],
    11: ["Eugene", (44.050505, -123.095051)],
    12: ["Lakeview", (42.188772, -120.345792)],
    13: ["Missoula", (46.870105, -113.995267)]
}

p = Proj(proj='utm', zone=10, ellps='WGS84', preserve_units=False)

def to_utm(lat, lon):
    return p(lon, lat)

for city in city_mapping.values():
    city[1] = to_utm(*city[1])

def create_route():
    route = list(city_mapping.keys())
    route.remove(0)  # Remove Seattle
    random.shuffle(route)
    route.insert(0, 0) 
    print(route)    
    return route

def evaluate(individual):
    distance = 0
    for i in range(len(individual) - 1):
        coord1 = city_mapping[individual[i]][1]
        coord2 = city_mapping[individual[i+1]][1]
        distance += np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
    return distance / 1000,


def print_generation(gen, population, file):
    best_ind = tools.selBest(population, 1)[0]
    best_route = [city_mapping[i][0] for i in best_ind]
    file.write("\n**GENERATION**: " + str(gen) + "\n")
    file.write("******************\n")
    file.write(" ==> ".join(best_route) + " ==> " + best_route[0] + "\n")
    if best_ind.fitness.valid:
        file.write("Fitness value: " + str(best_ind.fitness.values[0]) + "\n")
    else:
        file.write("Fitness value: Not Evaluated\n")
    file.write("******************\n")


def callback(population, num_gen, stats):
    with open("results.txt", "a") as f:
        print_generation(num_gen, population, f)
    return False



def main(hofVal):
    random.seed(42)
    if "FitnessMin" in creator.__dict__:
        del creator.FitnessMin

    if "Individual" in creator.__dict__:
        del creator.Individual

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    permutableList = []
    for row in range(1, len(city_mapping)-1):
        permutableList.append(row-1)

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(len(city_mapping)), len(city_mapping))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(city_mapping))
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("evaluate", evaluate)

    pop = toolbox.population(n=300)
    
    best_initial = tools.selBest(pop, 1)[0]

    hof = tools.HallOfFame(hofVal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    _, logbook = custom_eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.1, ngen=200, stats=stats, halloffame=hof, callback=callback)
    return pop, stats, hof, best_initial, logbook

def plot_route(route):
    x = [city_mapping[i][1][0] for i in route]
    y = [city_mapping[i][1][1] for i in route]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red')
    plt.plot(x, y, linestyle='-')
    for i in route:
        plt.text(city_mapping[i][1][0], city_mapping[i][1][1], city_mapping[i][0])
    plt.show()

def plot_graph3(logbook):
    gen_nums = logbook.select("gen")
    fit_mins = logbook.select("min")
    fit_avgs = logbook.select("avg")
    plt.figure(figsize=(10, 6))
    plt.plot(gen_nums, fit_mins, 'b-', label='Mejor Fitness')
    plt.plot(gen_nums, fit_avgs, 'r-', label='Promedio Fitness')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title('Evolución del Fitness a lo largo de las Generaciones')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

def print_route(route):
    route_names = [city_mapping[i][0] for i in route]
    print(" -> ".join(route_names))

if __name__ == "__main__":
    _, _, hof, best_initial, logbook = main(5)
    plot_route(best_initial)
    best_route = hof[0]
    print("Ruta optima: ")
    print_route(best_route)
    plot_route(best_route)
    plot_graph3(logbook)

    print("Valor de hof: 5 -> Ejecución Finalizada")

    _, _, hof, best_initial, logbook = main(30)
    plot_route(best_initial)
    best_route = hof[0]
    print("Ruta optima: ")
    print_route(best_route)
    plot_route(best_route)
    plot_graph3(logbook)

    print("Valor de hof: 30 -> Ejecución Finalizada")



