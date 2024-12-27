import re
import numpy as np
from enum import Enum
import math
from collections import deque

numbers = [int(x) for x in re.findall("\\d+", open("input/18-1.txt").read())]
coords = list(zip(numbers[0::2], numbers[1::2]))  # [(x0,y0),..,(xn, yn)]
GR_SZ = 71


class State(Enum):
    FRESH = 1
    OPEN = 2
    CLOSED = 3
    FORBIDDEN = 4


class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.dist = 99999999999
        self.pred = None
        self.state = State.FRESH

    def __lt__(self, other):
        return math.sqrt((GR_SZ - self.x) ** 2 + (GR_SZ - self.y) ** 2) - math.sqrt(
            (GR_SZ - other.x) ** 2 + (GR_SZ - other.y) ** 2)

    def __str__(self):
        state_str = '.' if self.state == State.FRESH else 'X' if self.state == State.OPEN else '#' if self.state == State.FORBIDDEN else 'O' if self.state == State.CLOSED else ''
        return state_str


def print_grid(grid_2_print: [[Node]]):
    for nodes in grid_2_print:
        print(''.join(map(lambda node: node.__str__(), nodes)))
    print('\n')


def init_grid(index: int) -> [[Node]]:
    new_grid = []
    for y in range(GR_SZ):
        row = []
        for x in range(GR_SZ):
            row.append(Node(x, y))
        new_grid.append(row)

    for i in range(0, index):
        node = new_grid[coords[i][1]][coords[i][0]]
        node.state = State.FORBIDDEN
    return new_grid


def print_path(node: Node, index: int):
    new_grid = init_grid(index)
    actual = node
    while actual is not None:
        new_grid[actual.y][actual.x].state = State.CLOSED
        actual = actual.pred
    print_grid(new_grid)


def bfs_go(index: int) -> int:
    grid = init_grid(index)
    queue = deque()
    queue.append(grid[0][0])
    node = grid[0][0]
    node.state = State.OPEN
    node.dist = 0
    path_found = False
    path_len = 999999
    while len(queue) > 0:
        node = queue.popleft()
        adjacents = []
        for offset in [[0, -1], [1, 0], [-1, 0], [0, 1]]:
            pos = np.add([node.y, node.x], offset)
            if 0 <= pos[0] < GR_SZ and 0 <= pos[1] < GR_SZ:
                adj = grid[pos[0]][pos[1]]
                if adj.state == State.FRESH:
                    adj.state = State.OPEN
                    adj.dist = node.dist + 1
                    adj.pred = node
                    adjacents.append(adj)
        if len(adjacents) > 0:
            #adjacents.sort()
            for ad in adjacents[::-1]:
                queue.append(ad)

        node.state = State.CLOSED
        #print_path(node)
        if node.x == GR_SZ - 1 and node.y == GR_SZ - 1:
            if path_len > node.dist:
                path_len = node.dist
                path_found = True
                print('Path found: ' + str(node.dist))
    if not path_found:
        print(f'Path not found by index: {index}')
        return -1
    return path_len


for index in range(3000, len(coords)):
    path_len = bfs_go(index)
    if path_len == -1:
        print(f'Line: {index}, Point:[{coords[index - 1][0]},{coords[index - 1][1]}]')
        print(f'{coords[index - 1][0]},{coords[index - 1][1]}')
        break
