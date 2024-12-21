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
    cheat_len = int(sys.argv[2])

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
    dist_to_exit = nx.single_source_shortest_path_length(G, end_node);
    baseline = dist_to_exit[start_node]
    print(baseline)
    dist_from_start = nx.single_source_shortest_path_length(G, start_node);
    cheats = []
    cnt = 0
    for n1, n2 in combinations(G.nodes(), 2):
        if (d := l2_dist(n1, n2)) <= cheat_len and abs(dist_to_exit[n1] - dist_to_exit[n2]) > d:
            if dist_to_exit[n1] > dist_to_exit[n2]:
                cheats.append(baseline - (dist_from_start[n1] + dist_to_exit[n2] + d))
            else:
                cheats.append(baseline - (dist_from_start[n2] + dist_to_exit[n1] + d))
#            print(n1, n2, dist_to_exit[n1], dist_to_exit[n2], cheats[-1])
            if cheats[-1] >= 100:
                cnt += 1

    c = Counter(cheats)
    for k, v in c.items():
        print(k, v)

    print('Part 1:', cnt)
    
main()
