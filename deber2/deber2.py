
def dijkstra(Grafo, salida, destino, heuristica):
    # Inicializamos las distancias y los predecesores
    dist, prev = {}, {}
    result = []
    expanded_count = -1  # Contador para los nodos expandidos
    
    # Establecemos la distancia inicial a todos los nodos como infinito y el predecesor como Ninguno
    for vertice in Grafo:
        dist[vertice] = float("inf")
        prev[vertice] = None
    # La distancia al nodo de salida es 0
    dist[salida] = 0
    
    # Creamos una lista con todos los nodos del grafo
    Q = [vertice for vertice in Grafo]
    
    # Mientras haya nodos en la lista
    while Q:
        # Seleccionamos el nodo con la menor función de costo f(n) = g(n) + h(n)
        u = min(Q, key=lambda vertice: dist[vertice] + heuristica[vertice])
        Q.remove(u)  # Eliminamos el nodo de la lista
        
        expanded_count += 1
        print(f"\nExpandiendo nodo: {u} (Nodo Expandido {expanded_count})")  # Imprimimos el nodo que se está expandiendo
        
        if u == destino:
            break  # Terminamos si hemos llegado al destino
        
        vecinos_actualizados = False
        for vecino in Grafo[u]:
            # Si el vecino está en la lista y su distancia es mayor que la del nodo actual más el costo del camino entre ellos
            if vecino in Q and dist[vecino] > dist[u] + Grafo[u][vecino]:
                # Actualizamos la distancia y el predecesor del vecino
                dist[vecino] = dist[u] + Grafo[u][vecino]
                prev[vecino] = u
                # Imprimimos la información requerida por cada nodo expandido
                print(f"  Padre: {u}, Hijo: {vecino}, Costo desde {salida} a {u}: {dist[u]} mi, Costo de {u} a {vecino}: {Grafo[u][vecino]} mi")
                vecinos_actualizados = True
        
        if not vecinos_actualizados:
            print(f"  No se encontró un camino más corto a los vecinos de {u}")
        
        result.append(u)
        
    print(f"\nNúmero total de nodos expandidos: {expanded_count + 1}")
    return result, dist, prev


#función para reconstruir la ruta más corta utilizando la información de los predecesores
def ruta_mas_corta(prev, dist, inicio, fin):
    ruta = [fin]
    distancias = [dist[fin]]
    while ruta[-1] != inicio:
        ruta.append(prev[ruta[-1]])
        distancias.append(dist[ruta[-1]])
    ruta.reverse()
    distancias.reverse()
    return ruta, distancias


# función para imprimir la ruta y la exploración
def imprimir_ruta_y_exploracion(grafo, ruta, distancias_ruta):
    for i in range(1, len(ruta)+1):
        print("Frontera={} (peso = {} mi); Explored={}".format(ruta[i-1], distancias_ruta[i-1], ', '.join(grafo[ruta[i-1]].keys())))


# Definicion del grafo y la heurística
grafo = {
    'Ellensburg': {'Pendleton': 168, 'Spokane': 175},
    'Pendleton': {'Ellensburg': 168},
    'Spokane': {'Bonners Ferry': 112, 'Missoula': 199, 'Ellensburg': 175},
    'Bonners Ferry': {'West Glacier': 176, 'Spokane': 112},
    'West Glacier': {'Bonners Ferry': 176, 'Helena': 243, 'Great Falls': 211, 'Havre': 231},
    'Missoula': {'Spokane': 199, 'Helena': 111},
    'Butte': {'Helena': 65},
    'Helena': {'Butte': 65, 'Missoula': 111, 'West Glacier': 243, 'Great Falls': 91},
    'Great Falls': {'Helena': 91, 'West Glacier': 211, 'Havre': 115},
    'Havre': {'Great Falls': 115, 'West Glacier': 231},
}

heuristica = {
    'Ellensburg': 516.03,
   'Pendleton': 472.53,
    'Spokane': 362.93,
    'Missoula': 232.19,
    'Bonners Ferry': 303.57,
    'Helena': 174.65,
    'Butte': 221.04,
    'West Glacier': 197.21,
    'Great Falls': 104.1,
    'Havre': 0
}

# Definimos el nodo de inicio y el nodo destino
inicio = 'Ellensburg'
destino = 'Havre'


s, distancia, previos = dijkstra(grafo, inicio, destino, heuristica)
ruta, distancias_ruta = ruta_mas_corta(previos, distancia, inicio, destino)

# Imprimimos la ruta desde el inicio hasta el destino
print(f"\nLa ruta desde {inicio} hasta {destino} es:")
for i in range(len(ruta)):
    if i == len(ruta) - 1:
        print(f"{ruta[i]}")
    else:
        print(f"{ruta[i]} ({distancias_ruta[i+1] - distancias_ruta[i]} mi) -> ", end="")
print(f"\nCon una distancia total de {distancia[destino]} mi.\n")
