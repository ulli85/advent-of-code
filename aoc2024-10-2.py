from enum import Enum


class Node:
    ADJACENCY = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def __init__(self, y: int, x: int, val: int):
        self.y = y
        self.x = x
        self.val = val

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.val}"

    def __adj_dy(self, adjacency_idx):
        return Node.ADJACENCY[adjacency_idx][0]

    def __adj_dx(self, adjacency_idx):
        return Node.ADJACENCY[adjacency_idx][1]

    def in_grid(self, point: [int]) -> bool:
        if (point[0] < 0 or point[0] >= len(Grid.grid)) or (point[1] < 0 or point[1] >= len(Grid.grid[0])):
            return False
        return True

    def is_adjacent(self, adjacency_idx: int) -> bool:
        return True if self.in_grid(
            [self.y + self.__adj_dy(adjacency_idx), self.x + self.__adj_dx(adjacency_idx)]) else False

    def get_adjacent(self, adjacency_idx: int) -> 'Node':
        if not self.is_adjacent(adjacency_idx):
            raise ValueError("")
        return Grid.grid[self.y + self.__adj_dy(adjacency_idx)][self.x + self.__adj_dx(adjacency_idx)]

    def all_adjacents(self):
        adjacents = []
        for i in range(len(Node.ADJACENCY)):
            if self.is_adjacent(i):
                neighbour = self.get_adjacent(i)
                if self.val + 1 == neighbour.val:
                    adjacents.append(neighbour)
        return adjacents


class Grid:
    grid = []
    NODES_START = []
    NODES_END = []
    NODE_START = 0
    NODE_END = 9
    path_max = 0

    def __init__(self, input):
        self.__create_grid(input)

    def __create_grid(self, input):
        for y in range(len(input)):
            self.grid.append([])
            for x in range(len(input[0])):
                node = Node(y, x, int(input[y][x]))
                self.grid[y].append(node)
                if node.val == Grid.NODE_START:
                    self.NODES_START.append(node)
                if node.val == Grid.NODE_END:
                    self.NODES_END.append(node)

    def dfs_go(self, start_node: Node, end_node: Node):
        if start_node == end_node:
            Grid.path_max += 1
        else:
            adjacents = start_node.all_adjacents()
            for adjacent in adjacents:
                self.dfs_go(adjacent, end_node)

    def mark_path(self, actual: Node, start: Node):
        prev = actual
        while prev != start and not prev.on_path:
            prev.on_path = True
            prev = prev.prev

    def reset(self):
        Grid.path_max = 0


f = open("aoc2024-10-1-input.txt", "r")
input = f.read()
grid = Grid(input.splitlines())

total_sum = 0
for start_node in Grid.NODES_START:
    for end_node in Grid.NODES_END:
        grid.dfs_go(start_node, end_node)
        total_sum += Grid.path_max
        grid.reset()
print(total_sum)
