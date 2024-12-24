import sys

op = {
    'OR': '|',
    'AND': '&',
    'XOR': '^',
}

print('graph G {')
with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip()
        if '->' in line:
            toks = line.split(' ')
            print(f'{toks[4]} -- {{{toks[0]} {toks[2]}}} [label = "{toks[1]}"];')
print('}')

