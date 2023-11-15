import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from customAlgorithms import custom_eaMuPlusLambda, custom_eaSimple

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
# Ciudades y sus coordenadas (latitud, longitud)
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
# Lista de nombres de ciudades
city_names = list(cities.keys())

def distance(city1, city2):
    # Convertir la distancia a kilómetros (asumiendo que las coordenadas están en grados)
    # El factor de 111.32 es una aproximación de cuántos km hay en un grado
    lat1, lon1 = city1
    lat2, lon2 = city2
    return 111.32 * np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def evaluate(individual):
    # Mapear los índices numéricos a los nombres de las ciudades
    route = [city_names[i] for i in individual]
    return sum(distance(cities[route[i-1]], cities[route[i]]) for i in range(len(route))), 

def print_generation(gen, population, file):
    best_ind = tools.selBest(population, 1)[0]
    best_route = [city_names[i] for i in best_ind]
    file.write("\n**GENERATION**: " + str(gen) + "\n")
    file.write("******************\n")
    file.write(" ==> ".join(best_route) + " ==> " + best_route[0] + "\n")
    if best_ind.fitness.valid:
        file.write("Fitness value: " + str(best_ind.fitness.values[0]) + "\n")
    else:
        file.write("Fitness value: Not Evaluated\n")
    file.write("******************\n")

# Callback para la función eaSimple para imprimir cada generación
def callback(population, num_gen, stats):
    with open("results.txt", "a") as f:
        print_generation(num_gen, population, f)
    return False

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(cities)), len(cities))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
indpb = 1.0/len(cities) # Probabilidad de mutación por índice
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=indpb)
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("evaluate", evaluate)

population = toolbox.population(n=300) # Población de 300 individuos

fitnesses = map(toolbox.evaluate, population)
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Gráfico 1: Ruta del mejor individuo de la población original
best_initial_route_indices = tools.selBest(population, 1)[0]
best_initial_route = [city_names[i] for i in best_initial_route_indices]
plt.figure(figsize=(10, 6))
for i in range(-1, len(best_initial_route)-1):
    city1 = cities[best_initial_route[i]]
    city2 = cities[best_initial_route[i+1]]
    plt.plot([city1[1], city2[1]], [city1[0], city2[0]], 'b-')
    plt.scatter(city1[1], city1[0], marker='o')
    plt.text(city1[1], city1[0], best_initial_route[i])
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Ruta del Mejor Individuo de la Población Original')
plt.grid(True)
plt.show()

with open("results.txt", "w") as f:
    print_generation(0, population, f)

hof = tools.HallOfFame(30)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)
stats.register("max", np.max)


mu = 300  # Tamaño de la población
lambda_ = 500  # Número de hijos generados por generación
ngen = 200  # Número de generaciones
cxpb = 0.90  # Probabilidad de cruzamiento
mutpb = 0.1  # Probabilidad de mutación

#population, logbook = custom_eaMuPlusLambda(population, toolbox, mu, lambda_, cxpb, mutpb, ngen, stats=stats, halloffame=hof, verbose=False, )

population, logbook = custom_eaSimple(population, toolbox, 0.90, 0.1, 200, stats=stats, halloffame=hof, verbose=False, callback=callback)


# Gráfico 2: Mejor ruta de todas las generaciones
best_route_indices = hof[0]
best_route = [city_names[i] for i in best_route_indices]
plt.figure(figsize=(10, 6))
for i in range(-1, len(best_route)-1):
    city1 = cities[best_route[i]]
    city2 = cities[best_route[i+1]]
    plt.plot([city1[1], city2[1]], [city1[0], city2[0]], 'b-')
    plt.scatter(city1[1], city1[0], marker='o')
    plt.text(city1[1], city1[0], best_route[i])
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Mejor Ruta de Todas las Generaciones')
plt.grid(True)
plt.show()

# Gráfico 3: Evolución del fitness a lo largo de las generaciones
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