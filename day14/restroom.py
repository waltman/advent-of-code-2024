import sys
import re
import numpy as np
from collections import Counter

class Robot:
    def __init__(self, px, py, vx, vy):
        self.p = np.array([int(py), int(px)])
        self.v = np.array([int(vy), int(vx)])

    def move(self, nrows, ncols):
        self.p[0] = (self.p[0] + self.v[0]) % nrows
        self.p[1] = (self.p[1] + self.v[1]) % ncols

    def quadrant(self, nrows, ncols):
        crow = nrows // 2
        if self.p[0] < crow:
            qrow = 0
        elif self.p[0] > crow:
            qrow = 1
        else:
            return -1

        ccol = ncols // 2
        if self.p[1] < ccol:
            qcol = 0
        elif self.p[1] > ccol:
            qcol = 1
        else:
            return -1

        return qrow * 2 + qcol

    def __repr__(self):
        return f'p={self.p}, v={self.v}'

def main():
    # parse the input
    robots = []
    infile = sys.argv[1]
    ncols, nrows = [int(x) for x in sys.argv[2:4]]
    with open(sys.argv[1]) as f:
        for line in f:
            m = re.match(r'p=(\d+),(\d+) v=([\d\-]+),([\d\-]+)', line)
            robots.append(Robot(m.group(1), m.group(2), m.group(3), m.group(4)))

    # move the robots
    for _ in range(100):
        for robot in robots:
            robot.move(nrows, ncols)

    c = Counter([robot.quadrant(nrows, ncols) for robot in robots])
    part1 = 1
    for k,v in c.items():
        if k >= 0:
            part1 *= v
    print('Part 1:', part1)

main()
