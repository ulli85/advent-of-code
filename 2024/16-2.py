import numpy as np
from collections import deque

MAZE: [[str]] = []
WALL = '#'
START_POS: [int] = []

DIRECTIONS = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}
ROTATIONS = {(0, 1): '>', (0, -1): '<', (1, 0): 'v', (-1, 0): '^'}


class Node:
    NODES: [['Node']] = None

    def __init__(self, x: int, y: int, prev: ['Node'] = None):
        self.x, self.y = x, y
        self.prev = prev
        self.direction = '>' if prev is None else self.__get_direction()
        self.steps = 0 if self.prev is None else self.prev.steps + 1
        self.rot_cnt = self.__count_rotations()

    def __str__(self):
        return f'{self.direction} {self.rot_cnt}'

    def __lt__(self, other):
        return self.cost() - other.cost()

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __get_direction(self):
        offset = (self.y - self.prev.y, self.x - self.prev.x)
        return ROTATIONS[offset]

    def __count_rotations(self) -> int:
        if self.prev is None: return 0
        rotation = 0 if self.direction == self.prev.direction else 1
        return self.prev.rot_cnt + rotation

    def cost(self):
        return self.rot_cnt * 1000 + self.steps


def init_maze() -> [[Node]]:
    lines = open("input/16-1.txt").read().splitlines()
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
            if 0 <= yn < len(MAZE) and 0 <= xn < len(MAZE[0]):
                char = MAZE[yn][xn]
                if char == WALL: continue
                if char == 'E':
                    new_end = Node(xn, yn, node)
                    actual_end = Node.NODES[yn][xn]
                    if actual_end is None or actual_end.cost() > new_end.cost():
                        end_node = new_end
                        Node.NODES[yn][xn] = new_end
                else:
                    adj_node = Node.NODES[yn][xn]
                    new_node = Node(xn, yn, node)
                    if adj_node is None:
                        Node.NODES[yn][xn] = new_node
                        adjacents.append(new_node)
                    elif adj_node != node.prev:
                        if adj_node.cost() > new_node.cost():
                            adj_node.prev = node
                            adj_node.steps = new_node.steps
                            adj_node.direction = new_node.direction
                            adj_node.rot_cnt = new_node.rot_cnt
                            adjacents.append(adj_node)

                if len(adjacents) > 0:
                    adjacents.sort()
                    for ad in adjacents[::-1]:
                        queue.append(ad)

    return end_node


def best_tiles(start: Node, tiles: set[Node]) -> set[Node]:
    #print_maze(tiles)
    if start is None: return tiles
    if start not in tiles:
        tiles.add(start)
    prev = start.prev
    if prev is not None:
        xd, yd = start.x - prev.x, start.y - prev.y
        xn, yn = prev.x - xd, prev.y - yd
        if 0 <= yn < len(MAZE) and 0 <= xn < len(MAZE[0]):
            prev_prev = Node.NODES[yn][xn]
            if prev_prev is not None and prev.direction != start.direction and prev_prev.direction == start.direction and prev_prev.cost() == start.cost() - 2:
                best_tiles(prev_prev, tiles)
    return best_tiles(prev, tiles)


def print_maze(best):
    for j, line in enumerate(MAZE):
        for i in range(len(MAZE[0])):
            node = Node(i, j)
            if node in best:
                MAZE[j][i] = 'O'
    for line in MAZE:
        print(''.join(line))


best = best_tiles(bfs_go(), set())
print(len(best))
