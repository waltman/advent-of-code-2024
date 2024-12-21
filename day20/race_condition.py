import sys
import numpy as np
import networkx as nx
from itertools import product, combinations
from collections import Counter

def neighbors(row, col):
    return [
        [(row, col), (row-1, col)],
        [(row, col), (row+1, col)],
        [(row, col), (row, col-1)],
        [(row, col), (row, col+1)],
    ]

def l2_dist(node1, node2):
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

def main():
    # parse the input
    with open(sys.argv[1]) as f:
        grid = np.array([[c for c in line.rstrip()] for line in f])

    nrows, ncols = grid.shape

    # find the start and end nodes
    walls = []
    for row, col in product(range(nrows), range(ncols)):
        if grid[row,col] == 'S':
            start_node = (row, col)
        elif grid[row,col] == 'E':
            end_node = (row, col)
        elif grid[row, col] == '#':
            walls.append((row, col))

    # make a graph out of the grid
    G = nx.grid_graph(dim=(ncols, nrows))
    G.remove_nodes_from(walls)

    # find the shortest path through the grid as a baseline
    lengths = nx.single_source_shortest_path_length(G, end_node);
    print(lengths)
    baseline = lengths[start_node]
    print(baseline)
    cheats = []
    for n1, n2 in combinations(G.nodes(), 2):
        if l2_dist(n1, n2) <= 2 and abs(lengths[n1] - lengths[n2]) > 2:
            cheats.append(min(lengths[n1], lengths[n2]) + 2)
#     baseline = len(nx.shortest_path(G, source=start_node, target=end_node)) - 1
#     print(f'{baseline=}')
# #    cheats = []
#     cnt = 0
#     for row, col in product(range(1, nrows-1), range(1, ncols-1)):
#         if grid[row,col] == '#':
#             G2 = G.copy()
#             G2.add_edges_from(neighbors(row, col))
#             if (path_len := len(nx.shortest_path(G2, source=start_node, target=end_node)) - 1) < baseline:
# #                cheats.append(baseline - path_len)
#                 if baseline - path_len >= 100:
#                     cnt += 1

#     print('Part 1:', cnt)

    c = Counter(cheats)
    for k, v in c.items():
        print(k, v)
    
main()
