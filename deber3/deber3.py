def load_database(file_path):
    database = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            state_str, cost_str = line.strip().split('],')
            state = [int(num) for num in state_str.strip('[]').split(',')]
            cost = int(cost_str.strip())
            database[tuple(state)] = cost
    return database

database1 = load_database('db_1_8.txt')

from queue import PriorityQueue

class Puzzle:
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent
        self.cost = cost

def a_star(initial_state, goal_state, database):
    open_list = PriorityQueue()
    open_list.put((0, initial_state))
    closed_list = set()
    parents = {tuple(initial_state): Puzzle(initial_state, None, 0)}
    
    iterations = 0  # Contador de iteraciones
    max_depth = 0  # Profundidad máxima alcanzada
    expanded_nodes = 0  # Nodos expandidos
    
    while not open_list.empty():
        current_cost, current_state = open_list.get()
        
        if tuple(current_state) in closed_list:
            continue
        iterations += 1
        expanded_nodes += 1
        
        # Calcular la profundidad
        depth = 0
        node = parents[tuple(current_state)]
        while node.parent:
            node = node.parent
            depth += 1
        max_depth = max(max_depth, depth)
        
        if current_state == goal_state:
            print(f"Número de Iteraciones: {iterations}")
            print(f"Número de Nodos Expandidos: {expanded_nodes}")
            print(f"Profundidad Máxima del Árbol: {max_depth}")
            print(f"Nodos en la Frontera: {open_list.qsize()}")
            
            path = []
            node = parents[tuple(current_state)]
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1]
        
        for neighbor in get_neighbors(current_state):
            if tuple(neighbor) in closed_list:
                continue
            
            neighbor_cost = database.get(tuple(neighbor), float('inf'))
            
            new_cost = current_cost + neighbor_cost
            
            if tuple(neighbor) not in parents or parents[tuple(neighbor)].cost > new_cost:
                parents[tuple(neighbor)] = Puzzle(neighbor, parents[tuple(current_state)], new_cost)
                open_list.put((new_cost, neighbor))
        
        closed_list.add(tuple(current_state))
    print(f"Número de Iteraciones: {iterations}")
    print(f"Número de Nodos Expandidos: {expanded_nodes}")
    print(f"Profundidad Máxima del Árbol: {max_depth}")
    print(f"Nodos en la Frontera: {open_list.qsize()}")
    return None

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

initial_state = [3, 5, 8, 2, 6, 4, 0, 1, 7]  # Reemplázalo por tu estado inicial
goal_state_1 = [1, 2, 3, 4, 5, 6, 7, 8, 0]


if check_solvability(initial_state):
    path = a_star(initial_state, goal_state_1, database1)
    if path:
        for p in path:
            print(p)
    else:
        print("No solution found!")
else:
    print("The given initial state is not solvable.")
