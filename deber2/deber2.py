def a_star_search(Grafo, salida, destino, heuristica):
    dist, prev = {}, {}
    result = []
    expanded_count = 0
    
    for vertice in Grafo:
        dist[vertice] = float("inf")
        prev[vertice] = None
    dist[salida] = 0
    
    Q = [vertice for vertice in Grafo]
    
    while Q:
        u = min(Q, key=lambda vertice: dist[vertice] + heuristica[vertice])
        Q.remove(u)
        
        if u == destino:
            break  # Terminamos si hemos llegado al destino
        
        for vecino in Grafo[u]:
            if vecino in Q and dist[vecino] > dist[u] + Grafo[u][vecino]:
                dist[vecino] = dist[u] + Grafo[u][vecino]
                prev[vecino] = u
                # Imprimir la información requerida por cada nodo expandido
                print(f"Padre: {u}, Hijo: {vecino}, Costo desde {salida} a {u}: {dist[u]} mi, Costo de {u} a {vecino}: {Grafo[u][vecino]} mi")
        
        expanded_count += 1
        result.append(u)
        
    print(f"Número total de nodos expandidos: {expanded_count}")
    return result, dist, prev


def ruta_mas_corta(prev, dist, inicio, fin):
    ruta = [fin]
    distancias = [dist[fin]]
    while ruta[-1] != inicio:
        ruta.append(prev[ruta[-1]])
        distancias.append(dist[ruta[-1]])
    ruta.reverse()
    distancias.reverse()
    return ruta, distancias


def imprimir_ruta_y_exploracion(grafo, ruta, distancias_ruta):
    for i in range(1, len(ruta)+1):
        print("Frontera={} (peso = {} mi); Explored={}".format(ruta[i-1], distancias_ruta[i-1], ', '.join(grafo[ruta[i-1]].keys())))


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
    'Ellensburg': 516.03,  # Distancia heurística entre Ellensburg y Havre
   'Pendleton': 472.53,
    'Spokane': 362.93,
    'Missoula': 232.19,
    'Bonners Ferry': 303.57,
    'Helena': 174.65,
    'Butte': 221.04,
    'West Glacier': 197.21,
    'Great Falls': 104.1,
    'Havre': 0  # Estás en el destino, por lo tanto, la distancia es 0
}

inicio = 'Ellensburg'
destino = 'Havre'

s, distancia, previos = a_star_search(grafo, inicio, destino, heuristica)
ruta, distancias_ruta = ruta_mas_corta(previos, distancia, inicio, destino)

print(f"\nLa ruta desde {inicio} hasta {destino} es:")
for i in range(len(ruta)):
    if i == len(ruta) - 1:
        print(f"{ruta[i]}")
    else:
        print(f"{ruta[i]} ({distancias_ruta[i+1] - distancias_ruta[i]} mi) -> ", end="")
print(f"\nCon una distancia total de {distancia[destino]} mi.")


