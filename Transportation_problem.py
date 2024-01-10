import numpy as np

def least_cost_method(costs, supplies, demands):
    m, n = costs.shape
    solution = np.zeros((m, n), dtype=int)

    while np.any(supplies > 0) and np.any(demands > 0):
        min_cost = np.inf
        min_i, min_j = -1, -1

        for i in range(m):
            for j in range(n):
                if supplies[i] > 0 and demands[j] > 0 and costs[i, j] < min_cost:
                    min_cost = costs[i, j]
                    min_i, min_j = i, j

        if min_i == -1 or min_j == -1:
            break

        quantity = min(supplies[min_i], demands[min_j])
        solution[min_i, min_j] = quantity

        supplies[min_i] -= quantity
        demands[min_j] -= quantity

    solution = np.where(solution == 0, -1, solution)
    return solution

def uv_method(costs, solution):
    m, n = costs.shape

    U = np.full(m, 'x', dtype='object')
    V = np.full(n, 'x', dtype='object')

    row_with_max_elements = np.argmax(np.sum(solution != -1, axis=1))
    U[row_with_max_elements] = 0

    while 'x' in U or 'x' in V:
        for i in range(m):
            for j in range(n):
                if solution[i, j] != -1:
                    if U[i] == 'x' and V[j] != 'x':
                        U[i] = int(costs[i, j]) - int(V[j])
                    elif U[i] != 'x' and V[j] == 'x':
                        V[j] = int(costs[i, j]) - int(U[i])

        for j in range(n):
            non_zero_elements = solution[:, j].nonzero()[0]
            if len(non_zero_elements) == 1:
                i = non_zero_elements[0]
                if U[i] == 'x' and V[j] != 'x':
                    U[i] = int(costs[i, j]) - int(V[j])
                elif U[i] != 'x' and V[j] == 'x':
                    V[j] = int(costs[i, j]) - int(U[i])


    return U, V

def calculate_penalties(costs, U, V, solution):
    m, n = costs.shape
    penalties = np.zeros_like(solution, dtype=int)
    tmp_solution = np.where(solution == 0, -1, solution)

    for i in range(m):
        for j in range(n):
            if tmp_solution[i, j] == -1:
                penalties[i, j] = costs[i, j] - U[i] - V[j]

    return penalties

def find_most_negative(penalties):
    min_penalty = np.min(penalties)
    indices = np.where(penalties == min_penalty)
    return indices[0][0], indices[1][0]

def update_solution(solution, closed_path, min_value):
    solution = np.where(solution == -1, 0, solution)
    visited_nodes = set()

    for i in range(len(closed_path)):
        x, y = closed_path[i]

        if i % 2 == 0 and (x, y) not in visited_nodes:
            solution[x, y] += min_value
            visited_nodes.add((x, y))
        elif i % 2 != 0 and (x, y) not in visited_nodes:
            solution[x, y] -= min_value
            visited_nodes.add((x, y))

   
    return solution

def form_closed_path(solution_matrix, new_basic_cell, penalties, U, V):
    m, n = solution_matrix.shape
    visited_cells = set()
    closed_path = []

    def find_cycle(cell):
        visited_cells.add(cell)
        closed_path.append(cell)

        i, j = cell
        for col in range(n):
            next_cell = (i, col)
            if solution_matrix[next_cell] != -1 and next_cell not in visited_cells:
                find_cycle(next_cell)

        for row in range(m):
            next_cell = (row, j)
            if solution_matrix[next_cell] != -1 and next_cell not in visited_cells:
                find_cycle(next_cell)

    find_cycle(new_basic_cell)
    closed_path.append(closed_path[0]) 

    pruned_path = [closed_path[0]]
    for i in range(1, len(closed_path)-1):
        if closed_path[i][0] == closed_path[i+1][0] and closed_path[i][1] != closed_path[i+1][1]:
            col_forward = closed_path[i][1] < closed_path[i+1][1]
            col_backward = not col_forward
            col = closed_path[i+1][1] if penalties[closed_path[i+1][0], closed_path[i+1][1]] == 0 else closed_path[i][1]
            pruned_path.append((closed_path[i][0], col))
        elif closed_path[i][1] == closed_path[i+1][1] and closed_path[i][0] != closed_path[i+1][0]:
            row_forward = closed_path[i][0] < closed_path[i+1][0]
            row_backward = not row_forward
            row = closed_path[i+1][0] if penalties[closed_path[i+1][0], closed_path[i+1][1]] == 0 else closed_path[i][0]
            pruned_path.append((row, closed_path[i][1]))


    for i in range(3, len(pruned_path)):
      current_cell = pruned_path[i]
      base_cell = pruned_path[0]

      if current_cell[0] == base_cell[0] or current_cell[1] == base_cell[1]:
          final_closed_path = pruned_path[:i+1].copy()
          break
  
    return final_closed_path

#================================TEST 1============================================

costs = np.array([[10, 12, 0],
                  [8, 4, 3],
                  [6, 9, 4],
                  [7, 8, 5]])

supplies = np.array([20, 30, 20, 10])
demands = np.array([10, 40, 30])
'''
costs = np.array([[40, 60, 90],
                  [60, 80, 70],
                  [50, 50, 100]])

supplies = np.array([40, 35, 50])
demands = np.array([35, 45, 35])
'''
solution_matrix_lc = np.zeros_like(costs)

solution_matrix_lc += least_cost_method(costs, supplies.copy(), demands.copy())

#================================TEST 2============================================
'''
costs2 = np.array([[3, 1, 7, 4],
                  [2, 6, 5, 9],
                  [8, 3, 3, 2]])

supplies2 = np.array([250, 350, 400])
demands2 = np.array([200, 300, 350, 150])

solution_matrix_lc2 = np.zeros_like(costs2)

solution_matrix_lc2 += least_cost_method(costs2, supplies2.copy(), demands2.copy())
'''

iteration = 1
while True:
    print(f"\n===============Iteracija {iteration}:\n")
    print("Pocetno resenje")
    print(solution_matrix_lc)
    #print(solution_matrix_lc2)

    U, V = uv_method(costs, solution_matrix_lc)
    #U,V = uv_method(costs2, solution_matrix_lc2)

    print("\nPotencijali U:")
    print(U, "\n")
    print("Potencijali V:")
    print(V, "\n")

    print("---------------------------\n")

    penalties = calculate_penalties(costs, U, V, solution_matrix_lc)
    #penalties = calculate_penalties(costs2, U, V, solution_matrix_lc2)
    print("Nove cene:")
    print(penalties)
    
    if np.all(penalties >= 0):
      print("\n==========================\n")
      break

    i, j = find_most_negative(penalties)

    new_basic_cell = (i, j)
    closed_path = form_closed_path(solution_matrix_lc, new_basic_cell, penalties, U, V)
    #closed_path = form_closed_path(solution_matrix_lc2, new_basic_cell, penalties, U, V)

    print("\nZatvorena putanja:")
    print(closed_path)

    tmp_solution = np.where(solution_matrix_lc == -1, 0, solution_matrix_lc)
    min_value = min(tmp_solution[cell] for cell in closed_path[1:-1])
    solution_matrix_lc = update_solution(solution_matrix_lc, closed_path, min_value)

    #tmp_solution = np.where(solution_matrix_lc2 == -1, 0, solution_matrix_lc2)
    #min_value = min(tmp_solution[cell] for cell in closed_path[1:-1])
    #solution_matrix_lc2 = update_solution(solution_matrix_lc2, closed_path, min_value)

    print("\nNovo pocetno resenje:")
    print(solution_matrix_lc)
    #print(solution_matrix_lc2)

    iteration += 1
    print("\n==========================\n")

print("\n===================RESENJE===================\n")
total_cost = np.sum(solution_matrix_lc * costs)
#total_cost = np.sum(solution_matrix_lc2 * costs2)
print("MATRICA:")
print(solution_matrix_lc)
#print(solution_matrix_lc2)
print("\nZ = ", total_cost)
