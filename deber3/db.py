from itertools import permutations

def manhattan(config, objetivo):
    distancia = 0
    for idx, val in enumerate(config):
        if val != 0:
            correct_idx = objetivo.index(val)  # Encuentra la posición objetivo del valor actual
            correct_row, correct_col = divmod(correct_idx, 3)
            row, col = divmod(idx, 3)
            distancia += abs(correct_row - row) + abs(correct_col - col)
    return distancia

def generar_configuraciones(numeros, objetivo, filename):
    configuraciones_unicas = set()  # Conjunto para almacenar configuraciones únicas
    
    with open(filename, 'w') as file:
        for perm in set(permutations(numeros)):
            if perm not in configuraciones_unicas:  # Verifica si la configuración ya fue procesada
                configuraciones_unicas.add(perm)
                distancia = manhattan(perm, objetivo)
                file.write(f"{list(perm)}, {distancia}\n")

# Para números 1-8 con estado objetivo [1,2,3,4,5,6,7,8,0]
generar_configuraciones([1,2,3,4,5,6,7,8,0], [1,2,3,4,5,6,7,8,0], 'db_1_8.txt')
