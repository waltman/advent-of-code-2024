import sys
from itertools import combinations, permutations

def bin2dec(wires, sw):
    dec = 0
    for k in sorted([k for k in wires.keys() if k.startswith(sw)], reverse=True):
        dec = dec * 2 + wires[k]
    return dec

def evaluate(wires, rules):
    done = False
    while not done:
        done = True
        for w1, w2, w3, op in rules:
            if w1 in wires and w2 in wires and w3 not in wires:
                wires[w3] = op(wires, w1, w2)
                done = False

def main():
    wires = dict()
    rules = []
    ops = {
        'AND': lambda w, x, y: w[x] & w[y],
        'OR':  lambda w, x, y: w[x] | w[y],
        'XOR': lambda w, x, y: w[x] ^ w[y],
    }
    
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if ':' in line:
                toks = line.split(': ')
                wires[toks[0]] = int(toks[1])
            elif '->' in line:
                toks = line.split(' ')
                rules.append([toks[0], toks[2], toks[4], ops[toks[1]]])

    wires_start = wires.copy()
    evaluate(wires, rules)

    print('Part 1:', bin2dec(wires, 'z'))

    xdec = bin2dec(wires, 'x')
    ydec = bin2dec(wires, 'y')
    zdec = bin2dec(wires, 'z')
    target = xdec + ydec
    print('xdec =', '{0:b}'.format(xdec))
    print('ydec =', '{0:b}'.format(ydec))
    print('zdec =', '{0:b}'.format(zdec))
    print('target =', '{0:b}'.format(target))

    # groups from printing out the graph with graphviz
    # set1 = {'ddd', 'y31', 'kgv', 'x31', 'rfq', 'spc', 'z31'}
    # set2 = {'z23', 'y23', 'x23', 'hpw', 'cgq', 'qdg'}
    # set3 = {'z15', 'x15', 'y15', 'dkk', 'pdb', 'fwr'}
    # set4 = {'z39', 'fnr', 'bdr', 'y39', 'x39', 'nrj'}
    # rules1 = [i for i in range(len(rules)) if len(set1 & set(rules[i][0:3])) > 0]
    # rules2 = [i for i in range(len(rules)) if len(set2 & set(rules[i][0:3])) > 0]
    # rules3 = [i for i in range(len(rules)) if len(set3 & set(rules[i][0:3])) > 0]
    # rules4 = [i for i in range(len(rules)) if len(set4 & set(rules[i][0:3])) > 0]
    set1 = {'z23','y23', 'x23', 'hpw', 'cgq', 'qdg'}
    rules1 = [i for i in range(len(rules)) if len(set1 & set(rules[i][0:3])) > 0]
    for perm1 in permutations(rules1, 4):
        new_wires = wires_start.copy()
        new_rules = rules.copy()
        new_rules[perm1[0]][2], new_rules[perm1[1]][2] = new_rules[perm1[1]][2], new_rules[perm1[0]][2]
        new_rules[perm2[0]][2], new_rules[perm2[1]][2] = new_rules[perm2[1]][2], new_rules[perm2[0]][2]
        new_rules[perm3[0]][2], new_rules[perm3[1]][2] = new_rules[perm3[1]][2], new_rules[perm3[0]][2]
        new_rules[perm4[0]][2], new_rules[perm4[1]][2] = new_rules[perm4[1]][2], new_rules[perm4[0]][2]
        evaluate(new_wires, new_rules)
        zdec = bin2dec(new_wires, 'z')
        if zdec == target:
            print('found one!', comb1, comb2, comb3, comb4)
    # for comb1 in combinations(rules1, 2):
    #     for comb2 in combinations(rules2, 2):
    #         for comb3 in combinations(rules3, 2):
    #             for comb4 in combinations(rules4, 2):
    #                 new_wires = wires_start.copy()
    #                 new_rules = rules.copy()
    #                 new_rules[comb1[0]][2], new_rules[comb1[1]][2] = new_rules[comb1[1]][2], new_rules[comb1[0]][2]
    #                 new_rules[comb2[0]][2], new_rules[comb2[1]][2] = new_rules[comb2[1]][2], new_rules[comb2[0]][2]
    #                 new_rules[comb3[0]][2], new_rules[comb3[1]][2] = new_rules[comb3[1]][2], new_rules[comb3[0]][2]
    #                 new_rules[comb4[0]][2], new_rules[comb4[1]][2] = new_rules[comb4[1]][2], new_rules[comb4[0]][2]
    #                 evaluate(new_wires, new_rules)
    #                 zdec = bin2dec(new_wires, 'z')
    #                 if zdec == target:
    #                     print('found one!', comb1, comb2, comb3, comb4)

    # # let's try setting x and y to 0 and see what happens
    # wires_zero = {k:1 for k in wires_start.copy().keys()}
    # print(wires_zero)
    # evaluate(wires_zero, rules)
    # zdec = bin2dec(wires_zero, 'z')
    # print('zdec =', zdec, '{0:b}'.format(zdec))
    # print(wires_zero)

    # print('graph G {')
    # for rule in rules:
    #     print(rule[2], '-- {' , rule[0], rule[1], '}')
    # print('}')

#     xdec = bin2dec(wires, 'x')
#     ydec = bin2dec(wires, 'y')
#     target = xdec & ydec
    
#     swaps = list(combinations(range(len(rules)), 2))

#     for comb in combinations(swaps, 2):
#         print(comb)
#         continue
# #        print('comb', comb)
#         for perm in permutations(comb):
#             wires = wires_start.copy()
# #            print('perm', perm)
#             new_rules = rules.copy()
#             for i in range(2):
#                 new_rules[comb[i]][2] = rules[perm[i]][2]
#             evaluate(wires, new_rules)
#             new_z = bin2dec(wires, 'z')
#             print(f'{target=}, {new_z=}')
#             if new_z == target:
#                 print('found!', perm)
#                 break

main()
