import sys
from itertools import pairwise

def main():
    part1 = 0
    in_rules = True
    rules = set()

    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if line == '':
                in_rules = False
            elif in_rules:
                before, after = [int(x) for x in line.split('|')]
                rules.add((before, after))
            else: # in reports, so check it
                pages = [int(x) for x in line.split(',')]
                ok = True
                for i, j in pairwise(pages):
                    if (j, i) in rules:
                        ok = False
                        break
                if ok:
                    part1 += pages[len(pages)//2]

    print('Part 1:', part1)

main()
