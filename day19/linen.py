import sys
from collections import defaultdict
from functools import cache

all_patterns = []

def possible(design, patterns):
    stack = [design]
    while stack:
        dsn = stack.pop()
        for pattern in patterns[dsn[0]]:
            if pattern == dsn:
                return True
            elif dsn.startswith(pattern):
                stack.append(dsn[len(pattern):])
    return False
    
@cache
def possible_cnt(design):
#    print(f'{design=}')
    subpatterns = []
    flag = 0
    for pattern in all_patterns:
        if pattern == design:
            flag = 1
        elif design.startswith(pattern):
            subpatterns.append(pattern)
#    print(f'{subpatterns=}')
    res = flag + sum([possible_cnt(design[len(subpat):]) for subpat in subpatterns])
#    print(f'{design=} {res=}')
    return res

def main():
    patterns = defaultdict(list)
    designs = []
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if ',' in line:
                for pattern in line.split(', '):
                    patterns[pattern[0]].append(pattern)
                    all_patterns.append(pattern)
            elif line:
                designs.append(line)

    cnt = 0
    for i in range(len(designs)):
#        print(f'testing design {i}: {designs[i]}')
        if possible(designs[i], patterns):
            cnt += 1
    print('Part 1:', cnt)

    cnt = 0
    for i in range(len(designs)):
        print(f'testing design {i}: {designs[i]}')
        tmp = possible_cnt(designs[i])
        print('cnt =', tmp)
        cnt += tmp
    print('Part 2:', cnt)

main()
