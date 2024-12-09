import sys

def parse_disk_map(line):
    disk_map = [int(c) for c in line]
    fid = 0
    blocks = []
    stats = []
    for i in range(len(disk_map)):
        if i % 2 == 0:
            stats.append((len(blocks), disk_map[i]))
            for j in range(disk_map[i]):
                blocks.append(fid)
            fid += 1
        else:
            for j in range(disk_map[i]):
                blocks.append('.')

    return blocks, stats

def frag(blocks):
    i = 0
    j = len(blocks)-1
    while i < j:
        while blocks[i] != '.':
            i += 1
        while j > i and blocks[j] == '.':
            j -= 1
        blocks[i] = blocks[j]
        blocks[j] = '.'
        i += 1
        j -= 1

def free_block(blocks, position, size):
    for i in range(len(blocks)-size):
        ok = True
        for j in range(i, i+size):
            if blocks[j] != '.':
                ok = False
                break
        if ok:
            return i if i < position else -1
    return -1

def frag2(blocks, stats):
    for fid in range(len(stats)-1, -1, -1):
        position, size = stats[fid]
        if (i := free_block(blocks, position, size)) >= 0:
            for j in range(size):
                blocks[i+j] = fid
                blocks[position+j] = '.'

def checksum(blocks):
    chk = 0
    for i in range(len(blocks)):
        if blocks[i] != '.':
            chk += i * blocks[i]

    return chk

def main():
    with open(sys.argv[1]) as f:
        line = f.readline().rstrip()

    blocks, stats = parse_disk_map(line)
    frag(blocks)
    print('Part 1:', checksum(blocks))
    
    blocks, stats = parse_disk_map(line)
    frag2(blocks, stats)
    print('Part 2:', checksum(blocks))

main()
