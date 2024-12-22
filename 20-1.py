import numpy as np
from collections import deque

MAZE: [[str]] = []
WALL = '#'
START_POS = np.full(2, 0, dtype=int)
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

    # could be better!!
    def possible_cheat(self, offset: tuple[int, int]) -> bool:
        is_wall = False
        for i in [1, 2]:
            yn, xn = self.y + i * offset[0], self.x + i * offset[1]
            if in_grid(xn, yn):
                is_wall = True if is_wall else WALL == MAZE[yn][xn]
            else:
                return False
        return is_wall

    def apply_cheat_on_maze(self, offset: tuple[int, int])-> bool:
        if self.possible_cheat(offset):
            for i in [1, 2]:
                yn = self.y + i * offset[0]
                xn = self.x + i * offset[1]
                if MAZE[yn][xn] != 'E':
                    MAZE[yn][xn] = str(i)
            return True
        return False


def in_grid(x, y) -> bool:
    return 0 <= y < len(MAZE) and 0 <= x < len(MAZE[0])


def init_maze():
    lines = open("input/20-1.txt").read().splitlines()
    MAZE.clear()
    for y, line in enumerate(lines):
        MAZE.append([str(x) for x in line])
        s_x = line.find('S')
        if s_x >= 0:
            START_POS[0] = y
            START_POS[1] = s_x
    # input START to END data
    Node.NODES = np.full((len(lines), len(lines[0])), None, dtype=Node)
    Node.NODES[START_POS[0]][START_POS[1]] = Node(START_POS[0], START_POS[1])


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


def apply_cheat_on_maze(node: Node, offset: tuple[int, int]) -> bool:
    if node.possible_cheat(offset):
        init_maze()
        node.apply_cheat_on_maze(offset)
        return True
    return False

def print_path(end_node) -> int:
    prev = last = end_node.prev
    while prev is not None:
        tile = MAZE[prev.y][prev.x]
        if tile != '1' and tile != '2':
            MAZE[prev.y][prev.x] = 'O'
        last = prev
        prev = prev.prev
    MAZE[last.y][last.x] = 'S'
    for line in MAZE:
        print(''.join(line))

def get_path_hash(end_node):
    vals = []
    actual = end_node.prev
    while actual is not None:
        vals.append(f'{actual.y}{actual.x}')
        actual = actual.prev
    return ''.join(vals)

init_maze()
end_node = bfs_go()
print_path(end_node)
print(f'Path took {end_node.steps} ps.\n')
unique_paths = set()
actual = end_node
while actual is not None:
    for offset in OFFSETS:
        if apply_cheat_on_maze(actual, offset):
            end_of_new_path = bfs_go()
            psecs_diff = end_node.steps - end_of_new_path.steps
            if psecs_diff > 0:
                path_hash = get_path_hash(end_of_new_path)
                if path_hash not in unique_paths:
                    if psecs_diff in CHEATS:
                        CHEATS[psecs_diff] += 1
                    else: CHEATS[psecs_diff] = 1
                    unique_paths.add(path_hash)
                else: print('Path not unique')
    actual = actual.prev

cheat_lengts = sorted(list(CHEATS.keys()))
for cheat_lengt in cheat_lengts:
    times = CHEATS[cheat_lengt]
    print(f'- There are {times} cheats that save {cheat_lengt} picoseconds')


print(CHEATS)
