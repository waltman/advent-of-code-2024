import sys
import networkx as nx
from itertools import product

def neighbors(row, col, dim):
    if row > 0:
        yield (row-1, col)
    if row < dim:
        yield (row+1, col)
    if col > 0:
        yield (row, col-1)
    if col < dim:
        yield (row, col+1)

def main():
    infile = sys.argv[1]
    dim, cutoff = (int(x) for x in sys.argv[2:4])
    bytes = []
    with open(infile) as f:
        for line in f:
            col, row = (int(x) for x in line.rstrip().split(','))
            bytes.append((row, col))

    byteset = {bytes[i] for i in range(cutoff)}

    G = nx.Graph()
    for row in range(dim+1):
        for col in range(dim):
            if len(byteset & {(row, col), (row, col+1)}) == 0:
                G.add_edge((row, col), (row, col+1))
    for col in range(dim+1):
        for row in range(dim):
            if len(byteset & {(row, col), (row+1, col)}) == 0:
                G.add_edge((row, col), (row+1, col))

    print('Part 1:', len(nx.shortest_path(G, (0,0), (dim, dim))) - 1)

    for i in range(cutoff, len(bytes)):
        ebunch = tuple([(bytes[i], neighbor) for neighbor in neighbors(bytes[i][0], bytes[i][1], dim)])
        G.remove_edges_from(ebunch)
        try:
            nx.shortest_path(G, (0,0), (dim, dim))
        except nx.NetworkXNoPath:
            print(f'Part 2: ({bytes[i][1]},{bytes[i][0]})')
            break

main()
