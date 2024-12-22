import numpy as np
from collections import deque

MAZE: [[str]] = []
WALL = '#'
START_POS: [int] = []


class Node:
    NODES: [['Node']] = None

    def __init__(self, x: int, y: int, prev: ['Node'] = None):
        self.x, self.y = x, y
        self.prev = prev
        self.steps = 0 if self.prev is None else self.prev.steps + 1

    def __str__(self):
        return f'[{self.y}, {self.x}] {self.steps}'

    def __lt__(self, other):
        return self.steps - other.steps

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def possible_cheat(self, offset):
        xn, yn = self.x + offset[0], self.y + offset[1]
        if in_grid(xn, yn):
            if WALL == MAZE[yn][xn]:
                xn, yn = xn + offset[0], yn + offset[1]
                return in_grid(xn, yn)


def in_grid(x, y) -> bool:
    return 0 <= y < len(MAZE) and 0 <= x < len(MAZE[0])

def init_maze() -> [[Node]]:
    lines = open("input/20-1.txt").read().splitlines()
    Node.NODES = np.full((len(lines), len(lines[0])), None, dtype=Node)
    for y, line in enumerate(lines):
        MAZE.append([str(x) for x in line])

        s_x = line.find('S')
        if s_x >= 0:
            START_POS.append(y)
            START_POS.append(s_x)


def bfs_go() -> Node:
    init_maze()
    node = Node(START_POS[1], START_POS[0])
    end_node = None
    Node.NODES[START_POS[0]][START_POS[1]] = node
    queue = deque()
    queue.append(node)
    while len(queue) > 0:
        node = queue.popleft()
        adjacents = []
        for offset in [(0, -1), (1, 0), (-1, 0), (0, 1)]:
            xn, yn = node.x + offset[0], node.y + offset[1]
            if in_grid(xn, yn):
                char = MAZE[yn][xn]
                if char == WALL: continue
                if char == 'E':
                    new_end = Node(xn, yn, node)
                    actual_end = Node.NODES[yn][xn]
                    if actual_end is None or actual_end.steps > new_end.steps:
                        end_node = new_end
                        Node.NODES[yn][xn] = new_end
                else:
                    adj_node = Node.NODES[yn][xn]
                    new_node = Node(xn, yn, node)
                    if adj_node is None:
                        Node.NODES[yn][xn] = new_node
                        adjacents.append(new_node)
                    elif adj_node != node.prev:
                        if adj_node.steps > new_node.steps:
                            adj_node.prev = node
                            adj_node.steps = new_node.steps
                            adjacents.append(adj_node)

                if len(adjacents) > 0:
                    adjacents.sort()
                    for ad in adjacents[::-1]:
                        queue.append(ad)

    return end_node


def steps_2_end(start: Node, end: Node):
    return end.steps - start.steps


def node_at_distance_from_end(end_node: Node, distance) -> Node:
    if distance > end_node.steps:
        raise IndexError(f'Index too high! {distance} > {end_node.steps}')
    actual = end_node
    while distance > 0:
        actual = actual.prev
        distance -= 1
    return actual


def apply_cheat(end_node, distance):
    init_maze()
    pass


def print_path(end_node) -> int:
    prev = last = end_node.prev
    psec = 0
    while prev is not None:
        psec += 1
        MAZE[prev.y][prev.x] = 'O'
        last = prev
        prev = prev.prev
    MAZE[last.y][last.x] = 'S'
    for line in MAZE:
        print(''.join(line))
    print(f'Path took {psec} ps.')
    return psec


end_node = bfs_go()
print(f'All steps {end_node.steps}')
print(node_at_distance_from_end(end_node, 5))

time_ms = print_path(end_node)
