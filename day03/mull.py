import sys
import re

def parse(tok):
    m = re.match(r'mul\((\d{1,3}),(\d{1,3})\)', tok)
    return int(m.group(1)) * int(m.group(2))

def main():
    with open(sys.argv[1]) as f:
        lines = [line.rstrip() for line in f]

    part1 = sum([sum([parse(tok) for tok in re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)]) for line in lines])
    print('Part 1:', part1)

    part2 = 0
    do = True
    for line in lines:
        toks = re.findall(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", line)
        for tok in toks:
            if tok == "do()":
                do = True
            elif tok == "don't()":
                do = False
            elif do:
                part2 += parse(tok)

    print('Part 2:', part2)

main()
