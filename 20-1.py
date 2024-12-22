import numpy as np
from collections import deque

MAZE: [[str]] = []
WALL = '#'
START_POS: [int] = []
OFFSETS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
CHEATS = {}

class Node:
    NODES: [['Node']] = None

    def __init__(self, y: int, x: int, prev: ['Node'] = None):
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

    def possible_cheat(self, offset: tuple[int, int]) -> bool:
        is_wall = False
        for i in [1, 2]:
            yn, xn = self.y + i * offset[0], self.x + i * offset[1]
            if in_grid(xn, yn):
                is_wall = True if is_wall else WALL == MAZE[yn][xn]
            else:
                return False
        return is_wall


def in_grid(x, y) -> bool:
    return 0 <= y < len(MAZE) and 0 <= x < len(MAZE[0])


def init_maze(start_node: Node = None, cheat_offset: tuple[int, int] = None):
    lines = open("input/20-1.txt").read().splitlines()
    MAZE.clear()
    for y, line in enumerate(lines):
        MAZE.append([str(x) for x in line])

        s_x = line.find('S')
        if s_x >= 0:
            while len(START_POS) > 0: START_POS.pop()
            START_POS.append(y)
            START_POS.append(s_x)
    # input START to END data
    if start_node is None:
        Node.NODES = np.full((len(lines), len(lines[0])), None, dtype=Node)
        Node.NODES[START_POS[0]][START_POS[1]] = Node(START_POS[0], START_POS[1])
    # other start node, compared to input start node
    else:
        MAZE[START_POS[0]][START_POS[1]] = '~'  # '~' really WALL? Maybe .?
        START_POS.pop()
        START_POS.pop()
        START_POS.append(start_node.y)
        START_POS.append(start_node.x)
        MAZE[START_POS[0]][START_POS[1]] = 'S'  # '~'
        actual = start_node
        Node.NODES = np.full((len(lines), len(lines[0])), None, dtype=Node)
        # build old path
        while actual is not None:
            Node.NODES[actual.y][actual.x] = actual
            actual = actual.prev
        # apply two picosecs cheat, two WALL tiles replaced with 1,2 tiles
        for i in [1, 2]: MAZE[START_POS[0] + i * cheat_offset[0]][START_POS[1] + i * cheat_offset[1]] = str(i)


def bfs_go() -> Node:
    node = Node.NODES[START_POS[0]][START_POS[1]]
    end_node = None
    Node.NODES[START_POS[0]][START_POS[1]] = node
    queue = deque()
    queue.append(node)
    while len(queue) > 0:
        node = queue.popleft()
        adjacents = []
        for offset in OFFSETS:
            xn, yn = node.x + offset[0], node.y + offset[1]
            if in_grid(xn, yn):
                char = MAZE[yn][xn]
                if char == WALL: continue
                if char == 'E':
                    new_end = Node(yn, xn, node)
                    actual_end = Node.NODES[yn][xn]
                    if actual_end is None or actual_end.steps > new_end.steps:
                        end_node = new_end
                        Node.NODES[yn][xn] = new_end
                else:
                    adj_node = Node.NODES[yn][xn]
                    new_node = Node(yn, xn, node)
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


def node_at_distance(end_node: Node, distance) -> Node:
    if distance > end_node.steps:
        raise IndexError(f'Index too high! {distance} > {end_node.steps}')
    actual = end_node
    while distance > 0:
        actual = actual.prev
        distance -= 1
    return actual


def apply_cheat(start_node, end_node):
    for offset in OFFSETS:
        if start_node.possible_cheat(offset):
            init_maze(start_node, offset)
            new_end_node = bfs_go()
            if new_end_node.steps < end_node.steps:
                print_path(new_end_node)
                saved_psecs = end_node.steps - new_end_node.steps
                print(f'Saved {saved_psecs} ps!')
                if saved_psecs in CHEATS:
                    CHEATS[saved_psecs] += 1
                else: CHEATS[saved_psecs] = 1

def print_path(end_node) -> int:
    prev = last = end_node.prev
    while prev is not None:
        MAZE[prev.y][prev.x] = 'O'
        last = prev
        prev = prev.prev
    MAZE[last.y][last.x] = 'S'
    for line in MAZE:
        print(''.join(line))
    print(f'Path took {end_node.steps} ps.\n')


init_maze()
end_node = bfs_go()
print_path(end_node)

for i in range(4, end_node.steps):
    start_node = node_at_distance(end_node, i)
    apply_cheat(start_node, end_node)
print(CHEATS)