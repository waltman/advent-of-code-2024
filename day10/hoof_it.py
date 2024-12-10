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

def rating(grid, position):
    peaks = []
    queue = deque()
    queue.append((0, position[0], position[1]))
    while queue:
        height, row, col = queue.popleft()
        if height == 9:
            peaks.append((row, col))
        else:
            for r, c in neighbors(grid, row, col):
                if grid[r,c] == height+1:
                    queue.append((height+1, r, c))
    return len(peaks)

def fix(c):
    return -1 if c == '.' else int(c)

def main():
    with open(sys.argv[1]) as f:
        grid = np.array([[fix(c) for c in line.rstrip()] for line in f])
    nrows, ncols = grid.shape

    trailheads = [(row, col) for row,col in product(range(nrows), range(ncols)) if grid[row,col] == 0]
    print('Part 1:', sum([score(grid, th) for th in trailheads]))
    print('Part 2:', sum([rating(grid, th) for th in trailheads]))

main()

