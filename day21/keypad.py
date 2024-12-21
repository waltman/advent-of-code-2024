import sys
import networkx as nx

def dirchar(from_pos, to_pos):
    char = {
        (-1,  0): 'v',
        ( 1,  0): '^',
        ( 0, -1): '>',
        ( 0,  1): '<',
    }
    
    delta = (from_pos[0]-to_pos[0], from_pos[1]-to_pos[1])
    return char[delta]

def gen_seq(code, paths, pos):
    sequence = []
    cur = 'A'
    for ch in code:
        if ch != cur:
            path = paths[cur][ch]
            for i in range(len(path)-1):
                sequence.append(dirchar(pos[path[i]], pos[path[i+1]]))
        sequence.append('A')
        cur = ch
    return ''.join(sequence)

def main():
    with open(sys.argv[1]) as f:
        codes = [line.rstrip() for line in f]

    # make a graph of the numeric keypad
    numeric = nx.grid_graph(dim=(3, 4))
    numeric.remove_node((3, 0))
    numeric_labels = {
        (0,0): '7',
        (0,1): '8',
        (0,2): '9',
        (1,0): '4',
        (1,1): '5',
        (1,2): '6',
        (2,0): '1',
        (2,1): '2',
        (2,2): '3',
        (3,1): '0',
        (3,2): 'A',
    }
    numeric = nx.relabel_nodes(numeric, numeric_labels)
    numeric_paths = dict(nx.all_pairs_shortest_path(numeric))
    numeric_pos = {v:k for k,v in numeric_labels.items()}

    # make a graph of the numeric keypad
    directional = nx.grid_graph(dim=(3, 2))
    directional.remove_node((0, 0))
    directional_labels = {
        (0,1): '^',
        (0,2): 'A',
        (1,0): '<',
        (1,1): 'v',
        (1,2): '>',
    }
    directional = nx.relabel_nodes(directional, directional_labels)
    directional_paths = dict(nx.all_pairs_shortest_path(directional))
    directional_pos = {v:k for k,v in directional_labels.items()}

    for code in codes:
        sequence = gen_seq(gen_seq(gen_seq(code, numeric_paths, numeric_pos), directional_paths, directional_pos), directional_paths, directional_pos)
        print(code, len(sequence))

main()
