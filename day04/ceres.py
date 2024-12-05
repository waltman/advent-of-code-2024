import sys
import numpy as np
from itertools import product

def main():
    # parse the input
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    nrows, ncols = grid.shape
    cnt1 = 0
    valid = {'XMAS', 'SAMX'}

    # across
    for row, col in product(range(nrows), range(ncols-3)):
        if ''.join(grid[row,col:col+4]) in valid:
            cnt1 += 1
    
    # down
    for row, col in product(range(nrows-3), range(ncols)):
        if ''.join(grid[row:row+4,col]) in valid:
            cnt1 += 1

    # nw to se
    for row, col in product(range(nrows-3), range(ncols-3)):
        diag = ''.join([grid[r,c] for r,c in zip(range(row, row+4), range(col, col+4))])
        if diag in valid:
            cnt1 += 1

    # sw to ne
    for row, col in product(range(nrows-1, 2, -1), range(ncols-3)):
        diag = ''.join([grid[r,c] for r,c in zip(range(row, row-4, -1), range(col, col+4))])
        if diag in valid:
            cnt1 += 1

    print('Part1:', cnt1)
    
main()
