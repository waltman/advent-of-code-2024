import sys
import networkx as nx
from itertools import product

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
    

main()
