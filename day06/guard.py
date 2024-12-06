import sys
import numpy as np
from itertools import product

def makes_loop(grid, position, start, deltas, next_dir):
    nrows, ncols = grid.shape
    STEP_LIMIT = 10000
    grid[position[0], position[1]] = '#'
    direction = 'up'
    steps = 0
    start_pos = position
    
    position = np.array(start)
    steps = 0
    while True:
        if steps > STEP_LIMIT:
            print(f'Loop, {start_pos=}, {steps=}')
            return True
        next_pos = position + deltas[direction]
        if next_pos[0] < 0 or next_pos[0] >= nrows or next_pos[1] < 0 or next_pos[1] >= ncols:
            # made it out, so no loop
            print(f'No loop, {start_pos=}, {steps=}')
            return False
        elif grid[tuple(next_pos)] == '#':
            # turn
            direction = next_dir[direction]
        else:
            position = next_pos
            steps += 1

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
    start = tuple(position)
    steps = 0
    tour = [(int(position[0]), int(position[1]))]
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
            tour.append([int(x) for x in position])
            steps += 1

    print('Part 1:', len(seen))
    print('steps:', steps)
    
    part2 = 0
    seen.remove(start)
    i = 1
    for position in seen:
        print(f'{i=}')
        i += 1
        if makes_loop(grid.copy(), np.array(position), start, deltas, next_dir):
            part2 += 1

    print('Part 2:', part2)


main()
