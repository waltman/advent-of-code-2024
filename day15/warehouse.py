import sys
import numpy as np
from itertools import product

def show_grid(grid):
    nrows, ncols = grid.shape
    res = ''
    for row in range(nrows):
        res += ''.join(grid[row,:]) + '\n'
    print(res)

def move_bot(grid, rpos, delta):
    # look in delta direction until we find a wall or a dot
    position = rpos + delta
    while (ch := grid[position[0],position[1]]) != '#':
        if ch == '.':
            break
        position += delta

    if grid[position[0],position[1]] == '#':
        return rpos

    # move whatever we can
    while np.any(position != rpos):
        new_pos = position - delta
        grid[position[0],position[1]] = grid[new_pos[0],new_pos[1]]
        grid[new_pos[0],new_pos[1]] = '.'
        position = new_pos

    return rpos + delta        

def execute_moves(grid, rpos, moves):
    delta = {
        '^': np.array([-1,  0]),
        'v': np.array([ 1,  0]),
        '<': np.array([ 0, -1]),
        '>': np.array([ 0,  1]),
    }

    for move in moves:
#        print('processing', move)
        rpos = move_bot(grid, rpos, delta[move])
#        print(move)
#        show_grid(grid)

def score(grid):
    nrows, ncols = grid.shape
    return sum([100*row + col for row, col in product(range(nrows), range(ncols)) if grid[row,col] == 'O'])

def main():
    # parse the input
    grid_list = []
    moves = ''
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if line == '':
                grid = np.array(grid_list)
            elif line[0] == '#':
                grid_list.append([c for c in line])
            else:
                moves += line

    nrows, ncols = grid.shape
    # find the robot
    for row in range(nrows):
        for col in range(ncols):
            if grid[row,col] == '@':
                rpos = np.array([row, col])
                break

    # move the robot around
    execute_moves(grid, rpos, moves)

    print('Part 1:', score(grid))

main()
