import sys
import numpy as np
import re
import math

class Machine:
    def __init__(self, ax, ay, bx, by, px, py):
        self.a = np.array([ax, ay])
        self.b = np.array([bx, by])
        self.p = np.array([px, py])

    def play(self):
        best_tok = 1e300
        best_i = -1
        best_j = -1

        for i in range(101):
            a = self.a * i
            if a[0] > self.p[0] or a[1] > self.p[1]:
                break
            for j in range(101):
                b = self.b * j
                tot = a + b
                if np.all(tot == self.p):
                    tok = 3 * i + j
                    if tok < best_tok:
                        best_tok = tok
                        best_i = i
                        best_j = j
                        break
                elif tot[0] > self.p[0] or tot[1] > self.p[1]:
                    break

        return best_tok if best_tok < 1e300 else 0

    def play2(self, limit=100, fudge=0):
        a = np.array([[self.a[0], self.b[0]], [self.a[1], self.b[1]]])

        x = np.linalg.solve(a, self.p + fudge)
        if np.all(x <= limit) and is_int(x):
            return int(round((x[0] * 3 + x[1])))
        else:
            return 0

    def __repr__(self):
        return f'{self.a=}, {self.b=}, {self.p=}'

def is_int(arr):
    eps = 1e-4
    return abs(round(arr[0]) - arr[0]) < eps and abs(round(arr[1]) - arr[1]) < eps

def main():
    # parse the input
    machines = []
    with open(sys.argv[1]) as f:
        state = 'a'
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            if state == 'a':
                m = re.match(r'Button A: X\+(\d+), Y\+(\d+)', line)
                ax = int(m.group(1))
                ay = int(m.group(2))
                state = 'b'
            elif state == 'b':
                m = re.match(r'Button B: X\+(\d+), Y\+(\d+)', line)
                bx = int(m.group(1))
                by = int(m.group(2))
                state = 'p'
            elif state == 'p':
                m = re.match(r'Prize: X=(\d+), Y=(\d+)', line)
                px = int(m.group(1))
                py = int(m.group(2))
                machines.append(Machine(ax, ay, bx, by, px, py))
                state = 'a'

    print('Part 1:', sum([machine.play2() for machine in machines]))
    print('Part 2:', sum([machine.play2(1e300, 10000000000000) for machine in machines]))

main()
