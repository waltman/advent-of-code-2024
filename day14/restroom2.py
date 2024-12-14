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

def show_robots(robots, nrows, ncols):
    grid = np.empty([nrows, ncols], dtype=str)
    grid[:] = ' '
    for robot in robots:
        grid[robot.p[0],robot.p[1]] = 'x'

    res = ''
    for row in range(nrows):
        res += ''.join(grid[row,:]) + '\n'
    return res

def main():
    # parse the input
    robots = []
    infile = sys.argv[1]
    ncols, nrows = [int(x) for x in sys.argv[2:4]]
    with open(sys.argv[1]) as f:
        for line in f:
            m = re.match(r'p=(\d+),(\d+) v=([\d\-]+),([\d\-]+)', line)
            robots.append(Robot(m.group(1), m.group(2), m.group(3), m.group(4)))

    for i in range(1,10001):
        for robot in robots:
            robot.move(nrows, ncols)
        grid = show_robots(robots, nrows, ncols)
        if 'xxxxxxxxxxx' in grid:
            print(f'{i=}')
            print(grid)

main()
