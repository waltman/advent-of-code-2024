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

def in_grid(grid, point):
    nrows, ncols = grid.shape
    return 0 <= point[0] < nrows and 0 <= point[1] < ncols;

def rotate(direct):
    return np.array([direct[1], -direct[0]])

# This is based on a really elegant solution by wurlin_murlin on
# reddit. It works by checking for corners by looking for 2 particular
# arrangements of plants at each corner of each cell in the connected
# component. Explanation and code at
# https://www.reddit.com/r/adventofcode/comments/1hcdnk0/comment/m1vyd5u/

def corners(grid, point):
    dUL = np.array([-1, -1])
    dUR = np.array([-1, 0])
    dLL = np.array([0, -1])
    plant = grid[point[0],point[1]]
    cnt = 0

    for d in range(4):
        UL = point + dUL
        UR = point + dUR
        LL = point + dLL
        ul = in_grid(grid, UL) and grid[UL[0],UL[1]] == plant
        ur = in_grid(grid, UR) and grid[UR[0],UR[1]] == plant
        ll = in_grid(grid, LL) and grid[LL[0],LL[1]] == plant

        if not ur and not ll:
            cnt += 1
        if ur and ll and not ul:
            cnt += 1

        dUL = rotate(dUL)
        dUR = rotate(dUR)
        dLL = rotate(dLL)

    return cnt

def num_sides(grid, cc):
    return sum([corners(grid, np.array(p)) for p in cc])

def main():
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    G = make_graph(grid)
    print(f'G has {nx.number_connected_components(G)} connected components')

    print('Part 1:', sum([len(cc) * perimeter(grid,cc) for cc in nx.connected_components(G)]))
    print('Part 2:', sum([len(cc) * num_sides(grid,cc) for cc in nx.connected_components(G)]))

main()
