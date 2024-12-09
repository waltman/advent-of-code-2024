import sys

def parse_disk_map(line):
    disk_map = [int(c) for c in line]
    fid = 0
    blocks = []
    for i in range(len(disk_map)):
        if i % 2 == 0:
            for j in range(disk_map[i]):
                blocks.append(fid)
            fid += 1
        else:
            for j in range(disk_map[i]):
                blocks.append('.')

    return blocks

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
#        print(blocks)

def checksum(blocks):
    chk = 0
    for i in range(len(blocks)):
        if blocks[i] == '.':
            break
        else:
            chk += i * blocks[i]

    return chk

def main():
    with open(sys.argv[1]) as f:
        line = f.readline().rstrip()

    blocks = parse_disk_map(line)
    frag(blocks)
    print(blocks)
    print('Part 1:', checksum(blocks))
    
main()
