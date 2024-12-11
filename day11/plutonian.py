import sys

def change(stone):
    if stone == 0:
        return [1]
    else:
        digits = str(stone)
        if (cnt := len(digits)) % 2 == 0:
            return [int(digits[0:cnt//2]), int(digits[cnt//2:])]
        else:
            return [stone * 2024]

def main():
    with open(sys.argv[1]) as f:
        for line in f:
            stones = [int(tok) for tok in line.rstrip().split(' ')]

    for i in range(int(sys.argv[2])):
        new_stones = []
        for stone in stones:
            new_stones += change(stone)

        stones = new_stones
        print(f'{i=} {len(stones)=}')

    print('Part 1:', len(stones))
        
main()
