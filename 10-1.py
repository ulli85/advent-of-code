from enum import Enum


class State(Enum):
    NEW = 1
    OPEN = 2
    CLOSED = 3


class Node:
    LIFE_STATES = {State.NEW, State.OPEN}
    ADJACENCY = [[-1, 0], [1, 0], [0, -1], [0, 1]]

    def __init__(self, y: int, x: int, val: int):
        self.y = y
        self.x = x
        self.val = val
        self.state = State.NEW
        self.prev: Node = None
        self.path_len = 0

    def __str__(self):
       return f"{self.state.name}[{self.y}, {self.x}]V:{self.val}"

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

    def getAdjacent(self, adjacency_idx: int) -> 'Node':
        if not self.is_adjacent(adjacency_idx):
            raise ValueError("")
        return Grid.grid[self.y + self.__adj_dy(adjacency_idx)][self.x + self.__adj_dx(adjacency_idx)]

    def allLiveAdjacents(self) -> ['Node']:
        return self.filteredAdjacents(Node.LIFE_STATES)

    def filteredAdjacents(self, states: {State}) -> ['Node']:
        adjacents = []
        for i in range(len(Node.ADJACENCY)):
            if self.is_adjacent(i):
                neighbour = self.getAdjacent(i)
                if self.val -1 == neighbour.val and neighbour.state in states:
                    adjacents.append(neighbour)
        return adjacents

class Grid:
    grid = []
    NODES_START = []
    NODES_END = []
    NODE_START = 0
    NODE_END = 9

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

    def rank_path(self, end_node: Node) -> int:
        path_rank = 0
        stack = [end_node]
        while len(stack) > 0:
            node = stack.pop()
            node.state = State.CLOSED
            adjacents = node.allLiveAdjacents()

            for adj in adjacents:
                adj.state = State.OPEN
                if node.path_len + 1 > adj.path_len:  # longer path is prefered
                    adj.prev = node
                    adj.path_len = node.path_len + 1
            if len(adjacents) == 0:
                if node.val == Grid.NODE_START:
                    path_rank += 1
            else:
                stack += adjacents
        return path_rank

    def reset(self):
        for i in range(len(Grid.grid)):
            for j in range(len(Grid.grid[0])):
                node = Grid.grid[i][j]
                node.prev = None
                node.state = State.NEW
                node.path_len = 0


f = open("aoc2024-10-1-input.txt", "r")
input = f.read()
grid = Grid(input.splitlines())

total_sum = 0

for end_node in Grid.NODES_END:
    total_sum += grid.rank_path(end_node)
    grid.reset()
print(total_sum)