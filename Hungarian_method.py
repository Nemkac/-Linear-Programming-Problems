import numpy as np


def matrix_transformation(cost_matrix):
    print("Početna matrica:")
    print(cost_matrix)

    # Oduzimanje minimuma u svakom redu
    reduced_matrix = cost_matrix - np.min(cost_matrix, axis=1)[:, np.newaxis]

    print("\nNakon oduzimanja minimuma u svakom redu:")
    print(reduced_matrix)

    # Oduzimanje minimuma u svakoj koloni gde nema nule (samo u koloni bez nule)
    for j in range(reduced_matrix.shape[1]):
        column_without_zeros = reduced_matrix[reduced_matrix[:, j] > 0, j]
        if len(column_without_zeros) > 0 and np.count_nonzero(reduced_matrix[:, j] == 0) == 0:
            min_val = np.min(column_without_zeros)
            reduced_matrix[:, j] -= min_val

    print("\nNakon oduzimanja minimuma u odabranoj koloni:")
    print(reduced_matrix)

    return reduced_matrix


def min_zero_row(zero_bool_mat, marked_zero):
    #Pronalazi red sa najmanjim brojem nula i dodaje prvu nulu u tom redu u listu označenih nula.
    min_row = [99999, -1]
    for row in range(zero_bool_mat.shape[0]):
        if np.sum(zero_bool_mat[row]) > 0 and min_row[0] > np.sum(zero_bool_mat[row]):
            min_row = [np.sum(zero_bool_mat[row]), row]

    zero_index = np.where(zero_bool_mat[min_row[1]])[0][0]
    marked_zero.append((min_row[1], zero_index))
    zero_bool_mat[min_row[1]] = False
    zero_bool_mat[:, zero_index] = False


def mark_matrix(cost_matrix):
    cur_mat = matrix_transformation(cost_matrix)
    zero_bool_mat = (cur_mat == 0) #Ako je u matrici troskova 0, na tom indexu je True
    zero_bool_mat_copy = zero_bool_mat.copy()

    marked_zeros_idxs = []
    while True in zero_bool_mat_copy:
        min_zero_row(zero_bool_mat_copy, marked_zeros_idxs)

    marked_zero_row = [i[0] for i in marked_zeros_idxs]
    marked_zero_col = [i[1] for i in marked_zeros_idxs]

    non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))

    marked_cols = []
    flag = True
    while flag:
        flag = False
        for i in range(len(non_marked_row)):
            row_array = zero_bool_mat[non_marked_row[i], :]

            for j in range(row_array.shape[0]):
                if row_array[j] and j not in marked_cols:
                    marked_cols.append(j)
                    flag = True

        for row_num, col_num in marked_zeros_idxs:
            if row_num not in non_marked_row and col_num in marked_cols:
                non_marked_row.append(row_num)
                flag = True

    marked_rows = list(set(range(cost_matrix.shape[0])) - set(non_marked_row))

    return marked_zeros_idxs, marked_rows, marked_cols


def update_matrix(cost_matrix, cover_rows, cover_cols):
    cur_mat = cost_matrix
    non_zero_element = []

    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    non_zero_element.append(cur_mat[row, i])
    min_num = min(non_zero_element)

    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    cur_mat[row, i] = cur_mat[row, i] - min_num
    for row in range(len(cover_rows)):
        for col in range(len(cover_cols)):
            cur_mat[cover_rows[row], cover_cols[col]] = cur_mat[cover_rows[row], cover_cols[col]] + min_num
    return cur_mat


def hungarian_algorithm(cost_matrix):
    #Dodavanje i oduzimanje minimalnog elementa sa odgovarajucih mesta
    dim = cost_matrix.shape[0]
    cur_mat = cost_matrix

    for row_num in range(cost_matrix.shape[0]):
        cur_mat[row_num] = cur_mat[row_num] - np.min(cur_mat[row_num])

    for col_num in range(cost_matrix.shape[1]):
        cur_mat[:, col_num] = cur_mat[:, col_num] - np.min(cur_mat[:, col_num])

    zero_count = 0
    while zero_count < dim:
        zero_pos, marked_rows, marked_cols = mark_matrix(cur_mat)
        zero_count = len(marked_rows) + len(marked_cols)

        if zero_count < dim:
            cur_mat = update_matrix(cur_mat, marked_rows, marked_cols)

    return zero_pos


def solve_hungarian(cost_matrix, pos):
    total = 0
    solution_matrix = np.zeros((cost_matrix.shape[0], cost_matrix.shape[1]))
    for i in range(len(pos)):
        total += cost_matrix[pos[i][0], pos[i][1]]
        solution_matrix[pos[i][0], pos[i][1]] = cost_matrix[pos[i][0], pos[i][1]]
    return total, solution_matrix


cost_matrix = np.array([[14, 9, 12, 8, 16],
                        [8, 7, 9, 9, 14],
                        [9, 11, 10, 10, 12],
                        [10, 8, 8, 6, 14],
                        [11, 9, 10, 7, 13]])

zero_pos = hungarian_algorithm(cost_matrix.copy())
result, result_matrix = solve_hungarian(cost_matrix, zero_pos)
print(f"\nRezultat problema dodele: {result:.0f}\n{result_matrix}\n")
