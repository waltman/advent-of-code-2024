import sys

def mix(x, y):
    return x ^ y

def next_secret(x):
    x ^= x * 64
    x = x % 16777216
    x ^= x // 32
    x = x % 16777216
    x ^= x * 2048
    x = x % 16777216
    return x
    

def main():
    with open(sys.argv[1]) as f:
        initials = [int(line) for line in f]

    cnt = 0
    for i in range(len(initials)):
        secret = initials[i]
        for _ in range(2000):
            secret = next_secret(secret)
        cnt += secret
    print('Part 1:', cnt)
    
main()
