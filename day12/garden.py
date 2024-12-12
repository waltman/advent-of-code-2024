import sys
import networkx as nx
import numpy as np
from itertools import product

# turn the grid into an undirected graph connecting common letters
def make_graph(grid):
    G = nx.Graph()
    nrows, ncols = grid.shape

    # make a node for every plot
    for r, c in product(range(nrows), range(ncols)):
        G.add_node((r,c))

    # rows:
    for r in range(nrows):
        for c in range(ncols-1):
            if grid[r,c] == grid[r,c+1]:
                G.add_edge((r,c), (r,c+1))

    # cols:
    for c in range(ncols):
        for r in range(nrows-1):
            if grid[r,c] == grid[r+1,c]:
                G.add_edge((r,c), (r+1,c))

    return G

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

def node_perimeter(grid, row, col):
    nrows, ncols = grid.shape
    cnt = 0
    for r,c in neighbors(grid, row, col):
        if grid[row,col] != grid[r,c]:
            cnt += 1
    if row == 0 or row == nrows-1:
        cnt += 1
    if col == 0 or col == ncols-1:
        cnt += 1

    return cnt

def perimeter(grid, cc):
    return sum([node_perimeter(grid,r,c) for r,c in cc])
    

def main():
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    G = make_graph(grid)
    for cc in nx.connected_components(G):
        print(cc)
        print(len(cc), perimeter(grid, cc))

    print('Part 1:', sum([len(cc) * perimeter(grid,cc) for cc in nx.connected_components(G)]))

main()
