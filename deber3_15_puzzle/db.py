from queue import PriorityQueue

import heapq

class Puzzle:
    def __init__(self, state, parent, cost, heuristic_cost):
        self.state = state
        self.parent = parent
        self.cost = cost  # g(n)
        self.heuristic_cost = heuristic_cost  # h(n)

    def __lt__(self, other):
        return (self.cost + self.heuristic_cost) < (other.cost + other.heuristic_cost)
    
    def check_solvability(state):
        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1
        return inversion % 2 == 0
    
def manhattan_distance(state, goal_state):
    distance = 0
    for tile in goal_state:
        try:
            x1, y1 = divmod(state.index(tile), 3)
            x2, y2 = divmod(goal_state.index(tile), 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
        except ValueError:
            print(f"Error in {state}")
            distance += 0 
    return distance



def a_star(initial_state, goal_state, heuristic_function):
    open_list = []
    initial_heuristic = heuristic_function(initial_state, goal_state) 
    heapq.heappush(open_list, (initial_heuristic, 0, initial_state))
    parents = {tuple(initial_state): (None, 0, initial_heuristic)}

    iterations = 0
    closed_list = set()

    while open_list:
        _, cost, current_state = heapq.heappop(open_list)
        iterations += 1
        
        if current_state == goal_state:
            path = []
            while current_state:
                path.append(current_state)
                current_state, _, _ = parents[tuple(current_state)]
            return cost, iterations, path

        closed_list.add(tuple(current_state))
        
        for neighbor in get_neighbors(current_state):
            neighbor_heuristic = heuristic_function(neighbor, goal_state)
            neighbor_cost = cost + 1
            neighbor_total_cost = neighbor_cost + neighbor_heuristic
            
            if tuple(neighbor) in closed_list or \
               (tuple(neighbor) in parents and parents[tuple(neighbor)][1] <= neighbor_cost):
                continue 
            
            parents[tuple(neighbor)] = (current_state, neighbor_cost, neighbor_heuristic)
            heapq.heappush(open_list, (neighbor_total_cost, neighbor_cost, neighbor))
    
    return float('inf')


def get_neighbors(state):
    neighbors = []
    zero_indices = [i for i, x in enumerate(state) if x == 0]
    
    for zero_index in zero_indices:
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
        
        for move in possible_moves[zero_index]:
            neighbor = state.copy()
            neighbor[zero_index], neighbor[move] = neighbor[move], neighbor[zero_index]
            if neighbor != state:  # Check to avoid duplicate state
                neighbors.append(neighbor)
    return neighbors

#------------------------------------------------------------------------------------------------

from itertools import permutations
import time

def hamming_distance(state, goal_state):
    return sum(s != g for (s, g) in zip(state, goal_state))

def generate_pattern_database(pattern, filename):
    if not Puzzle.check_solvability(pattern):
        print("No tiene solución")
        return None
    start_time = time.time()
    pdb_entries = []
    for perm in set(permutations(pattern)):
        cost_manhattan = a_star(list(perm), pattern, hamming_distance)
        if cost_manhattan is not None:
            total_cost = cost_manhattan[0]
        else:
            total_cost = 0

        pdb_entries.append(f"{list(perm)}, {total_cost}\n")
    
    with open(filename, 'w') as file:
        file.writelines(pdb_entries)
    
    end_time = time.time()
    print(f"Elapsed to generate PDB: {end_time - start_time:.4f} seconds")


goal_state = [1,2,3,4,5,6,7,8,0]
generate_pattern_database([1,2,3,4,0,0,0,0,0], 'pdb_1_4.txt')
generate_pattern_database([0,0,0,0,5,6,7,8,0], 'pdb_5_8.txt')

