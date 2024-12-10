import sys
import numpy as np
from itertools import product
from collections import deque

def neighbors(grid, row, col):
    deltas = [
        [0,1],
        [0,-1],
        [1,0],
        [-1,0],
    ]
        
    nrows, ncols = grid.shape
    for delta in deltas:
        r = row + delta[0]
        c = col + delta[1]
        if r >= 0 and r < nrows and c >= 0 and c < ncols:
            yield(r, c)

def score(grid, position):
    peaks = set()
    queue = deque()
    queue.append((0, position[0], position[1]))
    while queue:
        height, row, col = queue.popleft()
        if height == 9:
            peaks.add((row, col))
        else:
            for r, c in neighbors(grid, row, col):
                if grid[r,c] == height+1:
                    queue.append((height+1, r, c))
    return len(peaks)

def main():
    with open(sys.argv[1]) as f:
        tmp_grid = np.array([[c for c in line.rstrip()] for line in f])

    # All this just to handle the .'s in the test examples!
    grid = np.ndarray(tmp_grid.shape, dtype=int)
    nrows, ncols = grid.shape
    for row,col in product(range(nrows), range(ncols)):
        grid[row,col] = -1 if tmp_grid[row,col] == '.' else int(tmp_grid[row,col])

    print(grid)

    trailheads = [(row, col) for row,col in product(range(nrows), range(ncols)) if grid[row,col] == 0]
    print(trailheads)
    print('Part 1:', sum([score(grid, th) for th in trailheads]))

main()

