def load_database(file_path):
    database = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            state_str, cost_str = line.strip().split('],')
            state = [int(num) for num in state_str.strip('[]').split(',')]
            cost = int(cost_str.strip())
            database[tuple(state)] = cost
    return database

database_1_4 = load_database('pdb_1_4.txt')
database_5_8 = load_database('pdb_5_8.txt')


def pdb_heuristic(state, database_1_4, database_5_8):
    """
    Calcula la heurística para un estado dado utilizando dos PDBs.
    
    Toma el máximo de las dos heurísticas de las PDBs como la heurística para el estado.
    """
    cost_1_4 = database_1_4.get(tuple([state[i] if state[i] < 5 else 0 for i in range(9)]), 0)
    cost_5_8 = database_5_8.get(tuple([state[i] if state[i] >= 5 else 0 for i in range(9)]), 0)
    return cost_1_4 + cost_5_8

from queue import PriorityQueue
import time  # Importar el módulo time
import heapq  # Usaremos heapq en lugar de PriorityQueue para más control sobre la comparación de nodos

class Puzzle:
    def __init__(self, state, parent, cost, heuristic_cost):
        self.state = state
        self.parent = parent
        self.cost = cost  # g(n)
        self.heuristic_cost = heuristic_cost  # h(n)

    def __lt__(self, other):
        return (self.cost + self.heuristic_cost) < (other.cost + other.heuristic_cost)
def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(1, 9):  # 0 no es necesario ya que es el espacio vacío
        x1, y1 = divmod(state.index(i), 3)
        x2, y2 = divmod(goal_state.index(i), 3)
        distance += abs(x1-x2) + abs(y1-y2)
    return distance

def a_star_manhattan(initial_state, goal_state):
    open_list = []
    closed_list = set()
    initial_heuristic = manhattan_distance(initial_state, goal_state)
    heapq.heappush(open_list, Puzzle(initial_state, None, 0, initial_heuristic))
    parents = {tuple(initial_state): Puzzle(initial_state, None, 0, initial_heuristic)}

    iterations = 0  # Contador de iteraciones
    max_depth = 0  # Profundidad máxima alcanzada
    expanded_nodes = 0  # Nodos expandidos

    while open_list:
        current_node = heapq.heappop(open_list)
        current_state = current_node.state
        iterations += 1

        # Calcular la profundidad
        depth = 0
        node = current_node
        while node.parent:
            node = node.parent
            depth += 1
        max_depth = max(max_depth, depth)
        
        if current_state == goal_state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            print(f"Número de Iteraciones: {iterations}")
            print(f"Número de Nodos Expandidos: {expanded_nodes}")
            print(f"Profundidad Máxima del Árbol: {max_depth}")
            print(f"Nodos en la Frontera: {len(open_list)}")
            return path[::-1], expanded_nodes  # Retorna la solución y el número de nodos expandidos
        
        expanded_nodes += 1

        for neighbor in get_neighbors(current_state):
            neighbor_heuristic = manhattan_distance(neighbor, goal_state)
            neighbor_node = Puzzle(neighbor, current_node, current_node.cost+1, neighbor_heuristic)

            if tuple(neighbor) in closed_list:
                continue
            
            if tuple(neighbor) not in parents or parents[tuple(neighbor)].cost > neighbor_node.cost:
                parents[tuple(neighbor)] = neighbor_node
                heapq.heappush(open_list, neighbor_node)
        
        closed_list.add(tuple(current_state))

    print(f"Número de Iteraciones: {iterations}")
    print(f"Número de Nodos Expandidos: {expanded_nodes}")
    print(f"Profundidad Máxima del Árbol: {max_depth}")
    print(f"Nodos en la Frontera: {len(open_list)}")
    return None, expanded_nodes  # No hay solución y número de nodos expandidos


# ---------------------------------------------------------------------------------------------

def a_star(initial_state, goal_state):
    open_list = []
    closed_list = set()
    initial_heuristic = pdb_heuristic(initial_state, database_1_4, database_5_8)
    heapq.heappush(open_list, Puzzle(initial_state, None, 0, initial_heuristic))
    parents = {tuple(initial_state): Puzzle(initial_state, None, 0, initial_heuristic)}

    iterations = 0  # Contador de iteraciones
    max_depth = 0  # Profundidad máxima alcanzada
    expanded_nodes = 0  # Nodos expandidos

    while open_list:
        current_node = heapq.heappop(open_list)
        current_state = current_node.state
        iterations += 1

        # Calcular la profundidad
        depth = 0
        node = current_node
        while node.parent:
            node = node.parent
            depth += 1
        max_depth = max(max_depth, depth)
        
        if current_state == goal_state:
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            print(f"Número de Iteraciones: {iterations}")
            print(f"Número de Nodos Expandidos: {expanded_nodes}")
            print(f"Profundidad Máxima del Árbol: {max_depth}")
            print(f"Nodos en la Frontera: {len(open_list)}")
            return path[::-1], expanded_nodes  # Retorna la solución y el número de nodos expandidos
        
        expanded_nodes += 1

        for neighbor in get_neighbors(current_state):
            neighbor_heuristic = pdb_heuristic(current_state, database_1_4, database_5_8)
            neighbor_node = Puzzle(neighbor, current_node, current_node.cost+1, neighbor_heuristic)

            if tuple(neighbor) in closed_list:
                continue
            
            if tuple(neighbor) not in parents or parents[tuple(neighbor)].cost > neighbor_node.cost:
                parents[tuple(neighbor)] = neighbor_node
                heapq.heappush(open_list, neighbor_node)
        
        closed_list.add(tuple(current_state))

    print(f"Número de Iteraciones: {iterations}")
    print(f"Número de Nodos Expandidos: {expanded_nodes}")
    print(f"Profundidad Máxima del Árbol: {max_depth}")
    print(f"Nodos en la Frontera: {len(open_list)}")
    return None, expanded_nodes  # No hay solución y número de nodos expandidos


def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    possible_moves = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }
    
    for move in possible_moves[index]:
        neighbor = state.copy()
        neighbor[index], neighbor[move] = neighbor[move], neighbor[index]
        neighbors.append(neighbor)
    return neighbors

def check_solvability(state):
    """ Checks if the given state is solvable """
    inversion = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                inversion += 1
    return inversion % 2 == 0

initial_state = [2, 0, 3, 1, 7, 4, 5, 8, 6] 
initial_state2 =[0, 4, 3, 5, 7, 8, 6, 2, 1]
initial_state3 = [7, 6, 2, 4, 1, 5, 8, 3, 0]
initial_state4 = [1, 2, 3, 5, 4, 0, 6, 7, 8]

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]


def solve_puzzle_db(initial_state, goal_state_1):
    if check_solvability(initial_state):
        start_time = time.time()  # Guardar el tiempo de inicio
        path = a_star(initial_state, goal_state_1)
        end_time = time.time()  # Guardar el tiempo de finalización
        if path:
            for p in path:
                print(p)
            print(f"Elapsed Time: {end_time - start_time:.4f} seconds")
        else:
            print("No solution found!")
    else:
        print("The given initial state is not solvable.")

def solve_puzzle_manhattan(initial_state, goal_state):
    if check_solvability(initial_state):
        start_time = time.time()
        path, expanded_nodes = a_star_manhattan(initial_state, goal_state)
        end_time = time.time()
        if path:
            for p in path:
                print(p)
            print(f"Nodos expandidos: {expanded_nodes}")
            print(f"Elapsed Time: {end_time - start_time:.4f} seconds")
        else:
            print("No solution found!")
    else:
        print("The given initial state is not solvable.")

start_time = time.time() 
solve_puzzle_db(initial_state, goal_state)
print("-----------------------1------------------------------")
#solve_puzzle_db(initial_state2, goal_state, database1)
#print("-----------------------2------------------------------")
#solve_puzzle_db(initial_state3, goal_state, database1)
#print("-----------------------3------------------------------")
end_time = time.time()

start_time2 = time.time() 
solve_puzzle_manhattan(initial_state, goal_state)
print("-----------------------1.1------------------------------")
#solve_puzzle_manhattan(initial_state2, goal_state)
#print("-----------------------1.2------------------------------")
#solve_puzzle_manhattan(initial_state3, goal_state)
#print("-----------------------1.3------------------------------")
end_time2 = time.time()

print(f"Tiempo total DB -> Elapsed Time: {end_time - start_time:.4f} seconds")
print(f"Tiempo total Manhattan -> Elapsed Time: {end_time2 - start_time2:.4f} seconds")
