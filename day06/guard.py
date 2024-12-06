import sys
import numpy as np
from itertools import product

def main():
    # read in the grid
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    # make some helper dicts
    deltas = {
        'up':    [-1, 0],
        'down':  [1, 0],
        'right': [0, 1],
        'left':  [0, -1],
    }

    next_dir = {
        'up': 'right',
        'right': 'down',
        'down': 'left',
        'left': 'up',
    }

    # find the guard's initial position
    nrows, ncols = grid.shape
    for row, col in product(range(nrows), range(ncols)):
        if grid[row,col] == '^':
            position = np.array([row, col])
            direction = 'up'
            break

    # now let the guard walk around
    seen = {tuple(position)}
    while True:
        next_pos = position + deltas[direction]
        if next_pos[0] < 0 or next_pos[0] >= nrows or next_pos[1] < 0 or next_pos[1] >= ncols:
            # we're finished!
            break
        elif grid[tuple(next_pos)] == '#':
            # turn
            direction = next_dir[direction]
        else:
            position = next_pos
            seen.add(tuple(position))

    print('Part 1:', len(seen))

main()
