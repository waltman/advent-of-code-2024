import sys
import numpy as np
from itertools import product, combinations
from collections import defaultdict

def in_grid(point, nrows, ncols):
    return point[0] >= 0 and point[0] < nrows and point[1] >= 0 and point[1] < ncols

def main():
    # read in the grid
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    # find all the antennas
    antennas = defaultdict(list)
    nrows, ncols = grid.shape
    for row, col in product(range(nrows), range(ncols)):
        if grid[row,col] != '.':
            antennas[grid[row,col]].append(np.array([row,col]))

    # find all the antinodes
    antinodes = set()
    for k in antennas.keys():
        for pair in combinations(antennas[k], 2):
            delta = pair[1] - pair[0]
            a1 = pair[0] - delta
            a2 = pair[1] + delta
            if in_grid(a1, nrows, ncols):
                antinodes.add(tuple(a1))
            if in_grid(a2, nrows, ncols):
                antinodes.add(tuple(a2))

    print('Part 1:', len(antinodes))
    
main()
