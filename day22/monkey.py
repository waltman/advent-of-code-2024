import sys
from collections import defaultdict

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
    seq_list = []
    all_seqs = set()
    for i in range(len(initials)):
        secret = initials[i]
        prices = [secret % 10]
        for _ in range(2000):
            secret = next_secret(secret)
            prices.append(secret % 10)
        cnt += secret
        deltas = [prices[j+1] - prices[j] for j in range(len(prices)-1)]
        seqs = defaultdict(int)
        for j in range(len(deltas) - 4):
            k = ','.join([str(x) for x in deltas[j:j+4]])
            if k not in seqs:
                seqs[k] = prices[j+4]
                all_seqs.add(k)
        seq_list.append(seqs)
    print('Part 1:', cnt)
    print('Part 2:', max([sum([seq[k] for seq in seq_list]) for k in all_seqs]))
    
main()
