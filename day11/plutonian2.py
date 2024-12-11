import sys
from collections import defaultdict

def main():
    with open(sys.argv[1]) as f:
        for line in f:
            stones = [int(tok) for tok in line.rstrip().split(' ')]

    cnts = defaultdict(int)
    for stone in stones:
        cnts[stone] += 1

    for i in range(int(sys.argv[2])):
        new_cnts = defaultdict(int)
        for key, value in cnts.items():
            if key == 0:
                new_cnts[1] += value
            else:
                digits = str(key)
                if (cnt := len(digits)) % 2 == 0:
                    new_cnts[int(digits[0:cnt//2])] += value
                    new_cnts[int(digits[cnt//2:])] += value
                else:
                    new_cnts[key * 2024] += value

        cnts = new_cnts
        print(f'{i=} {sum(cnts.values())=}')

    print('Part 1:', sum(cnts.values()))
        
main()
