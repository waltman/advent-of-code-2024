import sys
import networkx as nx
from functools import cache, lru_cache

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

@lru_cache(maxsize=128)
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

# @lru_cache(maxsize=128)
# def gen_directional_seqs(cur, code):
#     global directional
#     global directional_pos
    
#     if len(code) == 1:
#         if code == cur:
#             return ['A']
#         else:
#             result = []
#             for path in nx.all_shortest_paths(directional, cur, code):
#                 seq = []
#                 for i in range(len(path)-1):
#                     seq.append(dirchar(directional_pos[path[i]], directional_pos[path[i+1]]))
#                 seq.append('A')
#                 result.append(''.join(seq))
#             return result
#     else:
#         result = []
#         for path1 in nx.all_shortest_paths(directional, cur, code[0]):
#             seq = []
#             for i in range(len(path1)-1):
#                 seq.append(dirchar(directional_pos[path1[i]], directional_pos[path1[i+1]]))
#             seq.append('A')
#             seq1 = ''.join(seq)
#             for seq2 in gen_directional_seqs(code[0], code[1:]):
#                 result.append(seq1 + seq2)
#         return result

@cache
def gen_directional_seqs(cur, code):
    global directional
    global directional_pos
    
    if len(code) == 1:
        if code == cur:
            return ['A']
        else:
            result = []
            minlen = 13e00
            for path in nx.all_shortest_paths(directional, cur, code):
                seq = []
                for i in range(len(path)-1):
                    seq.append(dirchar(directional_pos[path[i]], directional_pos[path[i+1]]))
                seq.append('A')
                path = ''.join(seq)
                if (curlen := len(path)) < minlen:
                    result = [path]
                    minlen = curlen
                elif curlen == minlen:
                    result.append(path)
            return result
    else:
        seq2s = []
        minlen = 1e300
        for seq2 in gen_directional_seqs(code[0], code[1:]):
            if (curlen := len(seq2)) < minlen:
                seq2s = [seq2]
                minlen = curlen
            elif curlen == minlen:
                seq2s.append(seq2)
        seq1s = []
        for path1 in nx.all_shortest_paths(directional, cur, code[0]):
            seq = []
            for i in range(len(path1)-1):
                seq.append(dirchar(directional_pos[path1[i]], directional_pos[path1[i+1]]))
            seq.append('A')
            seq1 = ''.join(seq)
            seq1s.append(seq1)
        result = []
        for s1 in seq1s:
            for s2 in seq2s:
                result.append(s1+s2)
        return result

# this is from https://github.com/oshlern/adventofcode/blob/main/advent24/2024/python/18/concise.py
#
# It looks like the key thing they're doing that I wasn't is just
# keeping track of the length of the paths instead of actually
# constructing the paths themselves. Now that I see that the answers
# are my approach was obviously never going to work.
def calc_fewest(code, N_ROBOT_KEYBOARDS):
    KEY_COORDS = {c: (x, y) for y, row in enumerate([" ^A", "<v>"]) for x, c in enumerate(row)}
    # Fewest of MY presses to hit kf when starting at ki (at layer 0)
    leg_lengths = {(0, ki, kf): 1 for ki in KEY_COORDS for kf in KEY_COORDS}
    # Fewest of MY presses to hit all ks when starting at A (at layer l)
    fewest_presses = lambda l, ks: sum(leg_lengths[(l, ki, kf)] for ki, kf in zip('A' + ks, ks))
    for layer in range(1, N_ROBOT_KEYBOARDS+1):
        if layer == N_ROBOT_KEYBOARDS:
            KEY_COORDS = {c: (x, y) for y, row in enumerate(["789", "456", "123", " 0A"]) for x, c in enumerate(row)}
        for ki, (xi, yi) in KEY_COORDS.items():
            for kf, (xf, yf) in KEY_COORDS.items():
                hor_ks = ('>' if xf > xi else '<') * abs(xf - xi)
                ver_ks = ('^' if yf < yi else 'v') * abs(yf - yi)
                fewest_hor_first = fewest_presses(layer-1, hor_ks + ver_ks + 'A') if (xf, yi) != KEY_COORDS[' '] else float('inf')
                fewest_ver_first = fewest_presses(layer-1, ver_ks + hor_ks + 'A') if (xi, yf) != KEY_COORDS[' '] else float('inf')
                leg_lengths[(layer, ki, kf)] = min(fewest_hor_first, fewest_ver_first)
    return fewest_presses(layer, code)

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

    print('Part 1:', sum(calc_fewest(code, 3)  * int(code[:-1]) for code in codes))
    print('Part 2:', sum(calc_fewest(code, 26)  * int(code[:-1]) for code in codes))

    # for code in codes:
    #     minlen = 1e300
    #     for path1 in gen_numeric_seqs('A', code):
    #         for path2 in gen_directional_seqs('A', path1):
    #             for path3 in gen_directional_seqs('A', path2):
    #                 minlen = min(minlen, len(path3))
    #     code_val = int(''.join([c for c in code if c.isnumeric()]))
    #     part1 += code_val * minlen

    # for code in codes:
    #     seqs = gen_numeric_seqs('A', code)
    #     for _ in range(2):
    #         new_seqs = []
    #         for path in seqs:
    #             new_seqs += gen_directional_seqs('A', path)
    #         seqs = new_seqs
    #     minlen = min([len(path) for path in seqs])
    #     code_val = int(''.join([c for c in code if c.isnumeric()]))
    #     part1 += code_val * minlen

    # print('Part 1:', part1)

    # part2 = 0
    # for code in codes:
    #     seqs = gen_numeric_seqs('A', code)
    #     for i in range(25):
    #         print(f'{code=} {i=}')
    #         new_seqs = []
    #         for path in seqs:
    #             new_seqs += gen_directional_seqs('A', path)
    #         seqs = new_seqs
    #     minlen = min([len(path) for path in seqs])
    #     code_val = int(''.join([c for c in code if c.isnumeric()]))
    #     part2 += code_val * minlen

    # print('Part 2:', part2)

    # part2 = 0
    # for code in codes:
    #     minlen = 1e300
    #     for path01 in gen_numeric_seqs('A', code):
    #         for path02 in gen_directional_seqs('A', path01):
    #             for path03 in gen_directional_seqs('A', path02):
    #                 for path04 in gen_directional_seqs('A', path03):
    #                     for path05 in gen_directional_seqs('A', path04):
    #                         for path06 in gen_directional_seqs('A', path05):
    #                             for path07 in gen_directional_seqs('A', path06):
    #                                 for path08 in gen_directional_seqs('A', path07):
    #                                     for path09 in gen_directional_seqs('A', path08):
    #                                         for path10 in gen_directional_seqs('A', path09):
    #                                             for path11 in gen_directional_seqs('A', path10):
    #                                                 for path12 in gen_directional_seqs('A', path11):
    #                                                     for path13 in gen_directional_seqs('A', path12):
    #                                                         for path14 in gen_directional_seqs('A', path13):
    #                                                             for path15 in gen_directional_seqs('A', path14):
    #                                                                 for path16 in gen_directional_seqs('A', path15):
    #                                                                     for path17 in gen_directional_seqs('A', path16):
    #                                                                         for path18 in gen_directional_seqs('A', path17):
    #                                                                             for path19 in gen_directional_seqs('A', path18):
    #                                                                                 for path20 in gen_directional_seqs('A', path19):
    #                                                                                     for path21 in gen_directional_seqs('A', path20):
    #                                                                                         for path22 in gen_directional_seqs('A', path21):
    #                                                                                             for path23 in gen_directional_seqs('A', path22):
    #                                                                                                 for path24 in gen_directional_seqs('A', path23):
    #                                                                                                     for path25 in gen_directional_seqs('A', path24):
    #                                                                                                         for path26 in gen_directional_seqs('A', path25):
    #                                                                                                             minlen = min(minlen, len(path26))
    #     code_val = int(''.join([c for c in code if c.isnumeric()]))
    #     part2 += code_val * minlen

    # print('Part 2:', part2)

main()
