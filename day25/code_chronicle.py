import sys
import numpy as np
from itertools import product

def pin_heights(grid, direction):
    nrows, ncols = grid.shape
    heights = []
    it = range(1, nrows) if direction == 'lock' else range(nrows-2, -1, -1)
    for col in range(ncols):
        cnt = 0
        for row in it:
            if grid[row,col] == '#':
                cnt += 1
            else:
                heights.append(cnt)
                break
    return np.array(heights)

def main():
    # parse input
    locks = []
    keys = []
    with open(sys.argv[1]) as f:
        grid_list = []
        for line in f:
            line = line.rstrip()
            if line == '':
                grid = np.array(grid_list)
                if grid[0,0] == '#':
                    locks.append(grid)
                else:
                    keys.append(grid)
                grid_list = []
            else:
                grid_list.append([c for c in line])
        # handle last grid
        grid = np.array(grid_list)
        if grid[0,0] == '#':
            locks.append(grid)
        else:
            keys.append(grid)
        grid_list = []
        
    lock_heights = [pin_heights(lock, 'lock') for lock in locks]
    key_heights = [pin_heights(key, 'key') for key in keys]

    print('Part 1:', sum([all(lh + kh <= 5) for lh, kh in product(lock_heights, key_heights)]))

main()
