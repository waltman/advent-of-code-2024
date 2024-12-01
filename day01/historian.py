import sys

def main():
    # parse the input
    list1 = []
    list2 = []

    with open(sys.argv[1]) as f:
        for line in f:
            toks = line.rstrip().split('   ')
            list1.append(int(toks[0]))
            list2.append(int(toks[1]))

    # Now solve it
    print('Part 1:', sum(map(lambda x: abs(x[0]-x[1]), zip(sorted(list1), sorted(list2)))))
    print('Part 2:', sum([x * len([y for y in list2 if y == x]) for x in list1]))
    
main()
