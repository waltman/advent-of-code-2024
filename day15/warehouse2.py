import sys
import numpy as np
from itertools import product
from collections import deque

def show_grid(grid):
    nrows, ncols = grid.shape
    res = ''
    for row in range(nrows):
        res += ''.join(grid[row,:]) + '\n'
    print(res)

def move_bot(grid, rpos, delta):
    # look in delta direction until we find a wall or a dot
    position = rpos + delta
    while (ch := grid[position[0],position[1]]) != '#':
        if ch == '.':
            break
        position += delta

    if grid[position[0],position[1]] == '#':
        return rpos

    # move whatever we can
    while np.any(position != rpos):
        new_pos = position - delta
        grid[position[0],position[1]] = grid[new_pos[0],new_pos[1]]
        grid[new_pos[0],new_pos[1]] = '.'
        position = new_pos

    return rpos + delta        

# this is the same as in part 1
def move_bot_row(grid, rpos, delta):
    # look in delta direction until we find a wall or a dot
    position = rpos + delta
    while (ch := grid[position[0],position[1]]) != '#':
        if ch == '.':
            break
        position += delta

    if grid[position[0],position[1]] == '#':
        return rpos

    # move whatever we can
    while np.any(position != rpos):
        new_pos = position - delta
        grid[position[0],position[1]] = grid[new_pos[0],new_pos[1]]
        grid[new_pos[0],new_pos[1]] = '.'
        position = new_pos

    return rpos + delta        

def move_bot_col(grid, rpos, delta):
    position = rpos + delta
    ch = grid[position[0],position[1]]

    # Do the two easy cases first
    if ch == '.':
        move_bot_simple(grid, rpos, delta)
        return rpos + delta
    elif ch == '#':
        # can't move
        return rpos
    else:
        assert ch in {'[',']'}

    # now check all the boxes on top of us
    queue = deque()
    move_stack = [rpos]
    left = np.array([0, -1])
    right = np.array([0, 1])
    added = set()
    if ch == '[':
        queue += [position, position + right]
        move_stack += [position, position + right]
    else:
        queue += [position, position + left]
        move_stack += [position, position + left]

    while queue:
        old_pos = queue.popleft()
        position = old_pos + delta
        ch = grid[position[0], position[1]]
        if ch == '#':
            # can't move
            return rpos
        elif ch == '[':
            if tuple(position) not in added:
                queue.append(position)
                move_stack.append(position)
                added.add(tuple(position))
            if tuple(position + right) not in added:
                queue.append(position + right)
                move_stack.append(position + right)
                added.add(tuple(position + right))
        elif ch == ']':
            if tuple(position) not in added:
                queue.append(position)
                move_stack.append(position)
                added.add(tuple(position))
            if tuple(position + left) not in added:
                queue.append(position + left)
                move_stack.append(position + left)
                added.add(tuple(position + left))
        
    # if we get here it should be safe to move everything on the move stack
    while move_stack:
        position = move_stack.pop()
        move_bot_simple(grid, position, delta)
    return rpos + delta

# move the bot one square in the delta direction
def move_bot_simple(grid, position, delta):
    new_pos = position + delta
    grid[new_pos[0],new_pos[1]] = grid[position[0],position[1]]
    grid[position[0],position[1]] = '.'

def execute_moves(grid, rpos, moves):
    delta = {
        '^': np.array([-1,  0]),
        'v': np.array([ 1,  0]),
        '<': np.array([ 0, -1]),
        '>': np.array([ 0,  1]),
    }

    for move in moves:
        if move in '<>':
            rpos = move_bot_row(grid, rpos, delta[move])
        else:
            rpos = move_bot_col(grid, rpos, delta[move])

def score(grid):
    nrows, ncols = grid.shape
    return sum([100*row + col for row, col in product(range(nrows), range(ncols)) if grid[row,col] == '['])

def main():
    # parse the input
    grid_list = []
    moves = ''
    double = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.',
    }
    
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.rstrip()
            if line == '':
                grid = np.array(grid_list)
            elif line[0] == '#':
                arr = []
                for c in line:
                    for c2 in double[c]:
                        arr.append(c2)
                grid_list.append(arr)
            else:
                moves += line

    nrows, ncols = grid.shape
    # find the robot
    for row, col in product(range(nrows), range(ncols)):
        if grid[row,col] == '@':
            rpos = np.array([row, col])
            break

    # move the robot around
    execute_moves(grid, rpos, moves)

    print('Part 2:', score(grid))

main()
