import sys
import numpy as np
import re

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
        # if best_tok < 1e300:
        #     print(f'best at ({best_i}, {best_j}) for {best_tok} tokens')
        # else:
        #     print("can't win")
        

    def __repr__(self):
        return f'{self.a=}, {self.b=}, {self.p=}'

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

    print('Part 1:', sum([machine.play() for machine in machines]))

    # for machine in machines:
    #     print(machine)
    #     machine.play()
        

main()
