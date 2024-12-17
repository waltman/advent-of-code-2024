import sys
import numpy as np
from collections import deque
from itertools import product

def neighbors(grid, row, col, direct):
    neigh = {
        '>': [(-1, 0, '^'), (1, 0, 'v')],
        '<': [(-1, 0, '^'), (1, 0, 'v')],
        '^': [(0, -1, '<'), (0, 1, '>')],
        'v': [(0, -1, '<'), (0, 1, '>')],
    }

    for r,c,d in neigh[direct]:
        if grid[row+r,col+c] == '.':
            yield (row+r, col+c, d)
        

def main():
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    nrows, ncols = grid.shape
    best_at = np.ones(grid.shape) * 1e300
    for row, col in product(range(nrows), range(ncols)):
        if grid[row,col] == 'S':
            start_tile = (row, col)
        elif grid[row,col] == 'E':
            end_tile = (row, col)
            grid[row,col] = '.'

    delta = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }
    best = 1e300
    stack = []
    seen = {start_tile}
    stack.append((start_tile[0], start_tile[1], '>', seen, 0));
    best_tiles = set()
    while stack:
        row, col, direct, seen, score = stack.pop()
        if score > best:
            continue
        if score > best_at[row, col]:
            continue
        else:
            best_at[row,col] = score
        if (row, col) == end_tile:
            if score < best:
                print('new best of', score)
                best = score
                best_tiles = seen
            elif score == best:
                best_tiles |= seen
        else:
            d = delta[direct]
            if grid[row+d[0], col+d[1]] == '.':
                next_pos = row+d[0], col+d[1]
                if next_pos not in seen:
                    stack.append((row+d[0], col+d[1], direct, seen | {next_pos}, score+1))
            for row2, col2, direct2 in neighbors(grid, row, col, direct):
                if (row2, col2) not in seen:
                    stack.append((row2, col2, direct2, seen | {(row2, col2)}, score+1001))

    print('Part 1:', best)
    print('Part 2:', len(best_tiles))
    print(sorted(best_tiles))
    print(best_at[(9,1)])
    print(best_at[(9,2)])
    print(best_at[(10,1)])

main()
