import sys

def main():
    wires = dict()
    rules = []
    ops = {
        'AND': lambda x, y: wires[x] & wires[y],
        'OR':  lambda x, y: wires[x] | wires[y],
        'XOR': lambda x, y: wires[x] ^ wires[y],
    }
    
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if ':' in line:
                toks = line.split(': ')
                wires[toks[0]] = int(toks[1])
            elif '->' in line:
                toks = line.split(' ')
                rules.append((toks[0], toks[2], toks[4], ops[toks[1]]))

    done = False
    while not done:
        done = True
        for w1, w2, w3, op in rules:
            if w1 in wires and w2 in wires and w3 not in wires:
                wires[w3] = op(w1, w2)
                done = False

    part1 = 0
    for k in sorted([k for k in wires.keys() if k.startswith('z')], reverse=True):
        print(k, wires[k])
        part1 = part1 * 2 + wires[k]
    print('Part 1:', part1)
    
main()
