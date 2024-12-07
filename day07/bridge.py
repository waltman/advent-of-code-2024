import sys
from itertools import product

def evaluate(eqn, func):
    target = eqn[0]
    values = eqn[1]
    for ops in product(func.keys(), repeat = len(values) - 1):
        res = values[0]
        for i in range(len(ops)):
            res = func[ops[i]](res, values[i+1])
            if res > target:
                break
        if res == target:
            return res
    return 0

def main():
    # parse the input
    equations = []
    with open(sys.argv[1]) as f:
        for line in f:
            toks = line.rstrip().split(': ')
            equations.append([int(toks[0]), [int(x) for x in toks[1].split(' ')]])

    # now evaluate each equation using these handy lambdas
    func1 = {'+': lambda x,y: x + y,
             '*': lambda x,y: x * y,
    }
    func2 = {'+': lambda x,y: x + y,
             '*': lambda x,y: x * y,
             '|': lambda x,y: int(f'{x}{y}'),
    }
    print('Part 1:', sum([evaluate(eqn, func1) for eqn in equations]))
    print('Part 2:', sum([evaluate(eqn, func2) for eqn in equations]))
          
main()
