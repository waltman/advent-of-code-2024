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
    

def num_sides(grid, cc):
    nrows, ncols = grid.shape
    cc = list(cc)
    minrow = min(x[0] for x in cc)
    mincol = min(x[1] for x in cc)
    maxrow = max(x[0] for x in cc)
    maxcol = max(x[1] for x in cc)
    plant = grid[cc[0][0],cc[0][1]]

    cnt = 0
    # horizontal
#    edges = set()
    for col in range(mincol, maxcol+1):
        for row in range(minrow-1, maxrow+1):
            if row < 0:
                if grid[0,col] == plant:
                    if col == 0 or grid[row+1,0] != plant:
                        flag = True
                else:
                    flag = False
            elif row == maxrow:
                flag = (grid[row,col] == plant and grid[row,col-1] != plant)
            elif col == mincol:
                if grid[row,col] == plant and row in {minrow, maxrow}:
                    flag = True
                elif grid[row,col] != grid[row+1,col] and plant in {grid[row,col], grid[row+1,col]}:
                    flag = True
                else:
                    flag = False
            elif grid[row,col] != grid[row+1,col] and plant in {grid[row,col], grid[row+1,col]}:
                flag = True
            else:
                flag = False
                
            if flag:
                print(f'({row},{col}) is a new edge')
                cnt += 1

    print(cnt, 'horizontal edges')
    tmp = cnt

    for row in range(minrow, maxrow+1):
        for col in range(mincol-1, maxcol+1):
            if col < 0:
                if grid[row,0] == plant:
                    if row == 0 or grid[row-1,0] != plant:
                        flag = True
                else:
                    flag = False
            elif col == maxcol:
                flag = (grid[row,col] == plant)
            elif row == minrow:
                if grid[row,col] == plant and col in {mincol, maxcol}:
                    flag = True
                elif grid[row,col] != grid[row,col+1] and plant in {grid[row,col], grid[row,col+1]}:
                    flag = True
                else:
                    flag = False
            elif grid[row,col] != grid[row,col+1] and plant in {grid[row,col], grid[row,col+1]}:
                flag = True
            else:
                flag = False
                
            if flag:
                print(f'({row},{col}) is a new edge')
                cnt += 1


#             flag = False
#             if row < 0:
#                 if grid[row+1][col] == plant:
#                     flag = True
#             elif row+1 >= nrows:
#                 if grid[row][col] == plant:
#                     flag = True
#             elif grid[row,col] != grid[row+1,col] and plant in {grid[row,col], grid[row+1,col]}:
#                 flag = True

#             if flag:
#                 if col == mincol or
#                    (row == 0 and grid[

#                 if col == mincol:
#                     print(f'({row},{col}) is a new edge')
#                     cnt += 1
#                 elif not ((grid[row,col-1] == grid[row,col]) and (grid[row+1,col-1] == grid[row+1,col])):
#                     print(f'({row},{col}) is a new edge')
#                     cnt += 1
#                 else:
#                     print(f'({row},{col}) is NOT a new edge')
#                 # if col == mincol or (row, col-1) not in edges or grid[row,col-1] != grid[row,col]:
#                 #     print(f'({row},{col}) is a new edge')
#                 #     cnt += 1
#                 # else:
#                 #     print(f'({row},{col}) is NOT a new edge')
# #                edges.add((row, col))

#     print(cnt, 'horizontal edges')
#     tmp = cnt
#     # vertical
# #    edges = set()
#     for row in range(minrow, maxrow+1):
#         for col in range(mincol-1, maxcol+1):
#             flag = False
#             if col < 0:
#                 if grid[row][col+1] == plant:
#                     flag = True
#             elif col+1 >= ncols:
#                 if grid[row][col] == plant:
#                     flag = True
#             elif grid[row,col] != grid[row,col+1] and plant in {grid[row,col], grid[row,col+1]}:
#                 flag = True

#             if flag:
#                 if row == minrow:
#                     print(f'({row},{col}) is a new edge')
#                     cnt += 1
#                 elif not ((grid[row-1,col] == grid[row,col]) and (grid[row-1,col+1] == grid[row,col+1])):
#                     print(f'({row},{col}) is a new edge')
#                     cnt += 1
#                 else:
#                     print(f'({row},{col}) is NOT a new edge')
#                 # if row == minrow or (row-1, col) not in edges or grid[row-1,col] != grid[row,col]:
#                 #     print(f'({row},{col}) is a new edge')
#                 #     cnt += 1
#                 # else:
#                 #     print(f'({row},{col}) is NOT a new edge')
#                 # edges.add((row, col))

    print(cnt-tmp, 'vertical edges')
    print(cc, cnt)
    return cnt
    

def main():
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    G = make_graph(grid)
    for cc in nx.connected_components(G):
        print(cc)
        print(len(cc), perimeter(grid, cc))
        
    print(f'G has {nx.number_connected_components(G)} connected components')

    print('Part 1:', sum([len(cc) * perimeter(grid,cc) for cc in nx.connected_components(G)]))
#    for cc in nx.connected_components(G):
#        num_sides(grid, cc)
    print('Part 2:', sum([len(cc) * num_sides(grid,cc) for cc in nx.connected_components(G)]))
    for cc in nx.connected_components(G):
        print('debug', cc, len(cc), num_sides(grid, cc))

main()
