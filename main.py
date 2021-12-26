import random
import numpy as np


def get_block(board, row, col):
    block_row = int(row / 3) * 2 if row == 9 else int(row / 3) * 3
    block_col = int(col / 3) * 2 if col == 9 else int(col / 3) * 3
    return board[block_row:block_row+3, block_col:block_col+3]


def assignment_complete(X):
    return not any([0 in row for row in X])


def extract_domains(board):
    domain = {}
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] != 0: continue
            # Not in the row or the col
            d = [num for num in range(1, 10) if num not in board[row, :] and num not in board[:, col]]
            # get the 3x3 subgrid
            block = get_block(board, row, col)
            d = [num for num in d if num not in block.flatten()]

            domain[(row, col)] = d

    return domain


def select_unassigned_variable(domains):
    """
    select the variable with minimum remaining values
    :param domains:
    :return: variable location (row, col)
    """
    mrv = None
    best = 9
    for row, col in domains:
        n = len(domains[(row, col)])
        if n < best:
            best = n
            mrv = row, col
            if best == 1: break

    return mrv


def assign(mrv, value, domains):
    assignment = {}
    row, col = mrv
    for i, j in domains:
        if (i, j) == mrv: continue
        assignment[(i, j)] = domains[(i, j)].copy()

        same_row = (i == row)
        same_col = (j == col)

        block_row = int(row / 3) * 3
        block_col = int(col / 3) * 3
        same_block = i in range(block_row, block_row + 3) and \
                j in range(block_col, block_col + 3)

        if (same_row or same_col or same_block) and value in assignment[(i, j)]:
            assignment[(i, j)].remove(value)
            if not assignment[(i, j)]: del assignment[(i, j)]

    return assignment


def solve(board, domains):

    if assignment_complete(board): return True

    # backtrack if no remaining values
    if not domains: return False

    # choose value
    mrv = select_unassigned_variable(domains)
    row, col = mrv

    for value in domains[mrv]:
        # remove the value from the neighbours domain
        assignment = assign(mrv, value, domains)
        board[row][col] = value
        # recursive call to subproblem
        if solve(board, assignment): return True
        del assignment

    # revert X, CSP and backtrack
    board[row][col] = 0
    return False


def generate_board():
    random_board = random.randint(1, 50)
    with open('boards.txt', 'r') as f:
        lines = f.readlines()
        board = list()
        for line in lines[random_board*10+1:random_board*10+10]:
            board.append([int(num) for num in line[:-1]])
            if len(board) == 9:
                break

        return np.array(board)


if __name__ == '__main__':
    import time

    board = generate_board()
    for x in board:
        print(x)
    start = time.time()
    domains = extract_domains(board)
    print()
    solve(board, domains)
    end = time.time()
    print("solution")
    for x in board:
        print(x)
    print('elapsed %.4f seconds.' % (end - start))