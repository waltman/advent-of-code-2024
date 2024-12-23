import sys
import networkx as nx

def main():
    G = nx.Graph()
    with open(sys.argv[1]) as f:
        for line in f:
            toks = line.strip().split('-')
            G.add_edge(toks[0], toks[1])

    cliques = list(nx.enumerate_all_cliques(G))
    print('Part 1:', len([clique for clique in cliques if len(clique) == 3 and any([node.startswith('t') for node in clique])]))
    print('Part 2:', ','.join(sorted(set(cliques[-1]))))

main()
