import sys
import networkx as nx
from functools import cache

numeric = nx.grid_graph(dim=(3, 4))
numeric_pos = dict()
directional = nx.grid_graph(dim=(3, 2))
directional_pos = dict()

def dirchar(from_pos, to_pos):
    char = {
        (-1,  0): 'v',
        ( 1,  0): '^',
        ( 0, -1): '>',
        ( 0,  1): '<',
    }
    
    delta = (from_pos[0]-to_pos[0], from_pos[1]-to_pos[1])
    return char[delta]

@cache
def gen_numeric_seqs(cur, code):
    global numeric
    global numeric_pos
    
    if len(code) == 1:
        if code == cur:
            return ['A']
        else:
            result = []
            for path in nx.all_shortest_paths(numeric, cur, code):
                seq = []
                for i in range(len(path)-1):
                    seq.append(dirchar(numeric_pos[path[i]], numeric_pos[path[i+1]]))
                seq.append('A')
                result.append(''.join(seq))
            return result
    else:
        result = []
        for path1 in nx.all_shortest_paths(numeric, cur, code[0]):
            seq = []
            for i in range(len(path1)-1):
                seq.append(dirchar(numeric_pos[path1[i]], numeric_pos[path1[i+1]]))
            seq.append('A')
            seq1 = ''.join(seq)
            for seq2 in gen_numeric_seqs(code[0], code[1:]):
                result.append(seq1 + seq2)
        return result

@cache
def gen_directional_seqs(cur, code):
    global directional
    global directional_pos
    
    if len(code) == 1:
        if code == cur:
            return ['A']
        else:
            result = []
            for path in nx.all_shortest_paths(directional, cur, code):
                seq = []
                for i in range(len(path)-1):
                    seq.append(dirchar(directional_pos[path[i]], directional_pos[path[i+1]]))
                seq.append('A')
                result.append(''.join(seq))
            return result
    else:
        result = []
        for path1 in nx.all_shortest_paths(directional, cur, code[0]):
            seq = []
            for i in range(len(path1)-1):
                seq.append(dirchar(directional_pos[path1[i]], directional_pos[path1[i+1]]))
            seq.append('A')
            seq1 = ''.join(seq)
            for seq2 in gen_directional_seqs(code[0], code[1:]):
                result.append(seq1 + seq2)
        return result

def main():
    with open(sys.argv[1]) as f:
        codes = [line.rstrip() for line in f]

    # make a graph of the numeric keypad
    global numeric
    global numeric_pos
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
    numeric_pos = {v:k for k,v in numeric_labels.items()}

    # make a graph of the numeric keypad
    global directional
    global directional_pos
    
    directional.remove_node((0, 0))
    directional_labels = {
        (0,1): '^',
        (0,2): 'A',
        (1,0): '<',
        (1,1): 'v',
        (1,2): '>',
    }
    directional = nx.relabel_nodes(directional, directional_labels)
    directional_pos = {v:k for k,v in directional_labels.items()}

    part1 = 0
    for code in codes:
        minlen = 1e300
        for path1 in gen_numeric_seqs('A', code):
            for path2 in gen_directional_seqs('A', path1):
                for path3 in gen_directional_seqs('A', path2):
                    minlen = min(minlen, len(path3))
        code_val = int(''.join([c for c in code if c.isnumeric()]))
        part1 += code_val * minlen

    print('Part 1:', part1)

main()
