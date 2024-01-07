# Linear-Programming-Problems
This repository contains implementations and examples of linear programming problems using various algorithms. The focus is on three key algorithms: Revised Simplex, Hungarian Algorithm for Assignment Problems, and the Transportation Problem.

For each of the algorithms, a detailed explanation is given with examples for each step, as well as the result of executing certain parts of the algorithms.

## Revised simplex

## Hungarian method for solving assignment problems
The Hungarian method is an algorithm for solving assignment problems. In the context of linear programming, the Hungarian method provides an efficient solution to the assignment problem by leveraging the principles of combinatorial optimization.

### Algorithm Overview
**1. Cost Matrix**
- Represent the assignment problem as a cost matrix, where each element represents the cost or weight associated with assigning a task to an agent.
- For the purposes of the example, the following cost matrix will be used:

  |     | A | B | C | D | E |
  |-----|---|---|---|---|---|
  | P | 14 | 9 | 12 | 8 | 16 |
  | Q | 8 | 7 | 9 | 9 | 14 |
  | R | 9 | 11 | 10 | 10 | 12 |
  | S | 10 | 8 | 8 | 6 | 14 |
  | T | 11 | 9 | 10 | 7 | 13 |

**2. Matrix Transformation**
- Subtract the minimum value in each row from all the elements in that row. This ensures that there is at least one zero in each row.
  
  |     | A | B | C | D | E |                        
  |-----|---|---|---|---|---|
  | P | 14 | 9 | 12 | ***8*** | 16 |
  | Q | 8 | ***7*** | 9 | 9 | 14 |      
  | R | ***9*** | 11 | 10 | 10 | 12 |
  | S | 10 | 8 | 8 | ***6*** | 14 |
  | T | 11 | 9 | 10 | ***7*** | 13 |
  
  After row reduction, we get the following matrix.
  
  |     | A | B | C | D | E |                        
  |-----|---|---|---|---|---|
  | P | 6 | 1 | 4 | ***0*** | 8 |
  | Q | 1 | ***0*** | 2 | 2 | 7 |      
  | R | ***0*** | 2 | 1 | 1 | 3 |
  | S | 4 | 2 | 2 | ***0*** | 8 |
  | T | 4 | 2 | 3 | ***0*** | 6 |
  
- If after reducing the rows there is a column in which there is no zero, the reduction of those columns is performed. Subtract the minimum value in each column from all the elements in that column. This ensures that there is at least one zero in each column.

  |     | A | B | C | D | E |                        
  |-----|---|---|---|---|---|
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

  |     | A | B | C | D | E |                        
  |-----|---|---|---|---|---|
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

## Transport problem
