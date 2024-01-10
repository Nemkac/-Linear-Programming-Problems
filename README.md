# Linear-Programming-Problems
This repository contains implementations and examples of linear programming problems using various algorithms. The focus is on three key algorithms: Revised Simplex, Hungarian Algorithm for Assignment Problems, and the Transportation Problem.

For each of the algorithms, a detailed explanation is given with examples for each step, as well as the result of executing certain parts of the algorithms.

## Revised simplex
The Revised Simplex Method is an iterative optimization algorithm used for solving linear programming (LP) problems. It is an enhanced version of the original Simplex Method, designed to improve computational efficiency by maintaining feasibility throughout the iterations.


## Hungarian method for solving assignment problems
The Hungarian method is an algorithm for solving assignment problems. In the context of linear programming, the Hungarian method provides an efficient solution to the assignment problem by leveraging the principles of combinatorial optimization.

### Algorithm Overview
**1. Cost Matrix**
- Represent the assignment problem as a cost matrix, where each element represents the cost or weight associated with assigning a task to an agent.
- For the purposes of the example, the following cost matrix will be used:

  |   | A | B | C | D | E |
  |---|---|---|---|---|---|
  | P | 14 | 9 | 12 | 8 | 16 |
  | Q | 8 | 7 | 9 | 9 | 14 |
  | R | 9 | 11 | 10 | 10 | 12 |
  | S | 10 | 8 | 8 | 6 | 14 |
  | T | 11 | 9 | 10 | 7 | 13 |

**2. Matrix Transformation**
- Subtract the minimum value in each row from all the elements in that row. This ensures that there is at least one zero in each row.
  
  |   | A | B | C | D | E |                        
  |---|---|---|---|---|---|
  | P | 14 | 9 | 12 | ***8*** | 16 |
  | Q | 8 | ***7*** | 9 | 9 | 14 |      
  | R | ***9*** | 11 | 10 | 10 | 12 |
  | S | 10 | 8 | 8 | ***6*** | 14 |
  | T | 11 | 9 | 10 | ***7*** | 13 |
  
  After row reduction, we get the following matrix.
  
  |   | A | B | C | D | E |                        
  |---|---|---|---|---|---|
  | P | 6 | 1 | 4 | ***0*** | 8 |
  | Q | 1 | ***0*** | 2 | 2 | 7 |      
  | R | ***0*** | 2 | 1 | 1 | 3 |
  | S | 4 | 2 | 2 | ***0*** | 8 |
  | T | 4 | 2 | 3 | ***0*** | 6 |
  
- If after reducing the rows there is a column in which there is no zero, the reduction of those columns is performed. Subtract the minimum value in each column from all the elements in that column. This ensures that there is at least one zero in each column.

  |   | A | B | C | D | E |                        
  |---|---|---|---|---|---|
  | P | 6 | 1 | 4 | ***0*** | 8 |
  | Q | 1 | ***0*** | 2 | 2 | 7 |      
  | R | ***0*** | 2 | ***1*** | 1 | ***3*** |
  | S | 4 | 2 | 2 | ***0*** | 8 |
  | T | 4 | 2 | 3 | ***0*** | 6 |
  
  After reducing columns C and E, we get the following matrix.
  
  |     | A | B | C | D | E |                        
  |-----|---|---|---|---|---|
  | P | 6 | 1 | 3 | ***0*** | 5 |
  | Q | 1 | ***0*** | 1 | 2 | 4 |      
  | R | ***0*** | 2 | ***0*** | 1 | ***0*** |
  | S | 4 | 2 | 1 | ***0*** | 5 |
  | T | 4 | 2 | 2 | ***0*** | 3 |
  
**3. Assignment**
- Mark zeros in the matrix in such a way that each row and column contains exactly one marked zero. This can be done through a process called "assignment" which involves drawing the minimum number of lines (either row or column) to cover all zeros.

  <a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/hvrL5dgt/c1.png' border='0' alt='c1'/></a>
  
**4. Zero Count**
- If the number of marked zeros equals the number of rows, an optimal assignment has been found. If not, proceed to step 5.
- In this case, the number of marked zeros is 3 and we have 5 rows, which means that we continue with the algorithm.

**5. Covering Zeros**
- Cover the minimum number of lines (either row or column) such that all zeros are covered. Adjust the matrix values accordingly.
- Covering all zeros with lines can be done according to the following algorithm:
  1. Mark rows that do not have marked (independent) zeros.
  2. Cross out all columns that have any type of zero in the marked rows.
  3. Mark the row that has a zero in the crossed-out column.
  4. Cross out all the unmarked rows.

  After covering all zeros the matrix should look like this:

  <a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/hvznC9V9/c2.png' border='0' alt='c2'/></a>

**6. Updating the matrix**
- When we have covered all the zeros with lines, we update the matrix with the following algorithm:
  1. We find the smallest element that is ***not*** covered by the line.
  2. We ***subtract*** the smallest element from all the others that are ***not*** covered by the line.
  3. We ***add*** the smallest to the elements located at the ***intersection of the vertical and horizontal lines***.
  4. All other elements that are covered with lines are overwritten.

  After updating the elements the matrix should look like this:

  |   | A | B | C | D | E |                        
  |---|---|---|---|---|---|
  | P | 5 | 0 | 2 | 0 | 4 |
  | Q | 1 | 0 | 1 | 3 | 4 |      
  | R | 0 | 2 | 0 | 2 | 0 |
  | S | 3 | 1 | 0 | 0 | 4 |
  | T | 3 | 1 | 1 | 0 | 2 |
  
**7. Repeat**
- Repeat steps 5-6 until an optimal assignment is achieved.

### Usage
Create a cost matrix for your assignment problem
```python
cost_matrix = np.array([[14, 9, 12, 8, 16],
                        [8, 7, 9, 9, 14],
                        [9, 11, 10, 10, 12],
                        [10, 8, 8, 6, 14],
                        [11, 9, 10, 7, 13]])
```

Call the Hungarian method function, passing the cost matrix as a parameter.
```python
zero_pos = hungarian_algorithm(cost_matrix.copy())
```

Obtain the optimal assignment (result_matrix) and corresponding total cost (result).
```python
result, result_matrix = solve_hungarian(cost_matrix, zero_pos)
```

Output
```
Total cost: 44

Result matrix: 
[[ 0.  9.  0.  0.  0.]
 [ 8.  0.  0.  0.  0.]
 [ 0.  0.  0.  0. 12.]
 [ 0.  0.  8.  0.  0.]
 [ 0.  0.  0.  7.  0.]]
```

## Transportation problem

The transportation problem is a type of linear programming problem that deals with the optimal allocation of goods from several suppliers to several consumers, minimizing the total transportation cost. The algorithm presented here provides a solution to the transportation problem using the Least Cost Method for the initial solution and the UV Potential Method for the iterative improvement.

### Algorithm Overview
**1. Initialization - Least Cost Method**
- Start with an initial feasible solution by using the Least Cost Method.
  
  Initial cost, supply and demand matrix:

  |   | A | B | C | Supply |
  |---|---|---|---|--------|
  | P | 10 | 12 | 0 | 20 |
  | Q | 8 | 4 | 3 | 30 |
  | R | 6 | 9 | 4 | 20 |
  | S | 7 | 8 | 5 | 10 | 
  | Demand | 10 | 40 | 30 |
  
- We use the price matrix, the supply and demand matrix, which we pass to the function and make the initial solution from it. We identify the cell with the lowest cost in the cost matrix, allocate as many resources as the supply and demand matrices allow for that field and then update the supply and demand matrix values.

  After filling the matrix using the method of least squares, the solution matrix looks like this:

  |     | A | B | C | Supply |
  |-----|---|---|---|--------|
  | P |  |  | 20 | 0 |
  | Q |  | 20 | 10 | 0 |
  | R | 10 | 10 |  | 0 |
  | S |  | 10 |  | 0 | 
  | Demand | 0 | 0 | 0 |

**2. UV Potential Method - Iterative Improvement**
- Initialize the U and V arrays to represent the dual variables associated with rows and columns.
- The filling of potentials U and V is performed using the following algorithm:
  1. We set the zero potential U on the row that has the most filled fields (it can also be chosen randomly.). In this case, it is Q or R. In this example, we will choose R.
  2. All other potentials are calculated using the formula
     
     $C[i,j] - U[i] - V[j] = 0$   -->   $U[i] = C[i,j] - V[j]$   and   $V[j] = C[i,j] - U[i]$
     
     where $C[i,j]$ is the cost value in the cost matrix for the corresponding field of the solution matrix.
  3. To calculate the potential, we use the prices of only those fields that have a value in the solution matrix.
  
  After calculating the potential U and V the matrix looks like this:
  
  |   | A | B | C | U |
  |---|---|---|---|--------|
  | P |  |  | 20 | -8 |
  | Q |  | 20 | 10 | -5 |
  | R | 10 | 10 |  | 0 |
  | S |  | 10 |  | -1 | 
  | V | 6 | 9 | 8 |

- After calculating the potential, we calculate the value of the penalty matrix. We calculate the values ​​in the penalty matrix on those indexes where there is no value in the solution matrix. We calculate the values ​​in the penalty matrix according to the following formula:

  $P[i,j] = C[i,j] - U[i] - V[j]$

  where $C[i,j]$ is the cost value in the cost matrix for the corresponding field of the solution matrix.

  The calculated penalty matrix looks like this:

  |   | A | B | C |
  |---|---|---|---|
  | P | 12 |11 |  |
  | Q | 7 |  |  |
  | R |  |  | -4 |
  | S | 2 |  | -2 |

**3. Updating the solution matrix**
- Once we have created the penalty matrix, we can move on to updating the solution matrix.
- We perform updating by creating a closed path inside the solution matrix starting from the index with the most negative value in the penalty matrix (or the most positive, depending on whether we are doing minimization or maximization).
- What is important is that the path nodes must contain elements that have a value greater than 0 in the solution matrix.
- Once we have created the path, updating the matrix takes place in the following two steps:
  1. When we created the path, we have to determine how many values ​​we can add to the starting field so that the balance of the matrix is ​​not disturbed.
  2. We go in order from the initial field to which we add a value, in the next edge of the path we subtract, in the next we   add, etc. and so on until the end of the path, that is, to the initial field 

We are creating a path to start from the field $(R, C)$ because the value in the same field in the penalty matrix is ​​the most negative (-4)
  
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/qvWxVHhf/c3.png' border='0' alt='c3'/></a>
    
We subtract 10 because it is the smallest value of all the values ​​from the path nodes and in this way, the balance of the matrix will not be disturbed (no value will become negative).
    
<a href='https://postimages.org/' target='_blank'><img src='https://i.postimg.cc/1zfRFbJz/c4.png' border='0' alt='c4'/></a>
  
  The updated matrix looks like this:
  
  |   | A | B | C |
  |---|---|---|---
  | P |  |  | 20 |
  | Q |  | 30 | 0 |
  | R | 10 | 0 | 10 |
  | S |  | 10 |  |

**4. Repeat**
- We repeat the iterative procedure, calculating the potential, creating the path and updating the matrix until, in some iteration, we get all positive values ​​(or negative, depending on the conditions of the task) of the penalty matrix.

### Usage

Create a cost matrix, supply vector, and demand vector for your transportation problem.

```python
costs = np.array([[10, 12, 0],
                  [8, 4, 3],
                  [6, 9, 4],
                  [7, 8, 5]])

supplies = np.array([20, 30, 20, 10])
demands = np.array([10, 40, 30])
```

Call the function to create the initial solution, passing the cost matrix, supply vector, and demand vector as parameters.

```python
solution_matrix_lc += least_cost_method(costs, supplies.copy(), demands.copy())
```

Iteratively call functions for an iterative procedure through a loop.

```python
iteration = 1
while True:
    print(f"\n===============Iteracija {iteration}:\n")
    print("Pocetno resenje")
    print(solution_matrix_lc)

    U, V = uv_method(costs, solution_matrix_lc)

    print("\nPotencijali U:")
    print(U)
    print("Potencijali V:")
    print(V)

    penalties = calculate_penalties(costs, U, V, solution_matrix_lc)
    print("\nNove cene:")
    print(penalties)

    i, j = find_most_negative(penalties)

    new_basic_cell = (i, j)
    closed_path = form_closed_path(solution_matrix_lc, new_basic_cell)

    print("\nZatvorena putanja:")
    print(closed_path)

    min_value = min(solution_matrix_lc[cell] for cell in closed_path[1:-1])
    solution_matrix_lc = update_solution(solution_matrix_lc, closed_path, min_value)

    print("\nNovo pocetno resenje:")
    print(solution_matrix_lc)

    if np.all(penalties >= 0):
        break

    iteration += 1
    print("\n==========================\n")
```

Obtain the optimal transportation plan and corresponding total cost.

```python
total_cost = np.sum(solution_matrix_lc * costs)
print("\nKrajnje resenje:")
print(solution_matrix_lc)
print("\nZ = ", total_cost)
```

Output
```
MATRICA:
[[ 0  0 20]
 [ 0 30  0]
 [10  0 10]
 [ 0 10  0]]

Z =  300
```
