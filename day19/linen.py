import sys
from collections import defaultdict

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
    
def possible_cnt(design, patterns):
    stack = [design]
    cnt = 0
    while stack:
        dsn = stack.pop()
        for pattern in patterns[dsn[0]]:
            if pattern == dsn:
                cnt += 1
                print('cnt =', cnt)
            elif dsn.startswith(pattern):
                stack.append(dsn[len(pattern):])
    return cnt
    

def main():
    patterns = defaultdict(list)
    designs = []
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if ',' in line:
                for pattern in line.split(', '):
                    patterns[pattern[0]].append(pattern)
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
        cnt += possible_cnt(designs[i], patterns)
    print('Part 2:', cnt)

main()
