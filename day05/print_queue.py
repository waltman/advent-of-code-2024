import sys

def main():
    part1 = 0
    part2 = 0
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
                for i in range(len(pages)-1):
                    for j in range(i+1, len(pages)):
                        if (pages[j], pages[i]) in rules:
                            ok = False
                            pages[i], pages[j] = pages[j], pages[i]

                if ok:
                    part1 += pages[len(pages)//2]
                else:
                    part2 += pages[len(pages)//2]

    print('Part 1:', part1)
    print('Part 2:', part2)

main()
