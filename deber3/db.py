from itertools import permutations
import time

def calculate_pattern_cost(state, pattern, goal):
    cost = 0
    for piece in pattern:
        if piece in state and piece != 0:
            # Encontrar la posición de la pieza en el estado y el objetivo
            piece_idx_state = state.index(piece)
            piece_idx_goal = goal.index(piece)
            
            # Calcular y sumar la distancia de Manhattan para esta pieza
            cost += abs(piece_idx_state // 3 - piece_idx_goal // 3) + abs(piece_idx_state % 3 - piece_idx_goal % 3)
    return cost


def generate_pattern_database(pattern, goal, filename):
    start_time = time.time()
    
    # Extraemos todas las permutaciones posibles del patrón y calculamos el costo
    pdb_entries = []
    for perm in set(permutations(pattern)):
        cost = calculate_pattern_cost(perm, pattern, goal)
        pdb_entries.append(f"{list(perm)}, {cost}\n")
    
    # Escribimos la PDB en un archivo
    with open(filename, 'w') as file:
        file.writelines(pdb_entries)
    
    end_time = time.time()
    print(f"Elapsed to generate PDB: {end_time - start_time:.4f} seconds")

# Ejemplo de uso
goal_state = [1,2,3,4,5,6,7,8,0]
generate_pattern_database([1,2,3,4,0,0,0,0,0], goal_state, 'pdb_1_4.txt')
generate_pattern_database([0,0,0,0,5,6,7,8,0], goal_state, 'pdb_5_8.txt')
