from collections import deque

import numpy as np


def start_pos() -> tuple[int, int]:
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                return r, c
    raise Exception("Couldn't find start position")


def print_path(path):
    new_maze = []
    for r in range(len(maze)):
        new_maze.append([x for x in maze[r]])
    for node in path[1:-1]:
        r, c = node[0], node[1]
        new_maze[r][c] = node[2]
    print(np.array(new_maze))


def bfs(start, picosecs=0):
    start = (*start, picosecs, None)
    visited = {}
    q = deque([start])
    end = None
    while q:
        r, c, picos, prev = q.popleft()
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if nr < 0 or nc < 0 or nr >= len(maze) or nc >= len(maze[0]): continue
            if (nr, nc) in visited: continue
            if maze[nr][nc] == '#': continue
            adjacent = (nr, nc, picos + 1, (r, c, picos, prev))
            q.append(adjacent)
            visited[(nr, nc)] = adjacent
            if maze[nr][nc] == 'E':
                end = adjacent
                print('Found path')
    path = []
    actual = end
    while actual:
        path.append(actual)
        actual = actual[3]
    return list(reversed(path))


def cheat(path: [], visited: {}, start: int):
    actual = path[start]
    r, c = actual[0], actual[1]

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        for x in 2, 3:
            nr, nc = r + dr * x, c + dc * x
            if nr < 0 or nc < 0 or nr >= len(maze) or nc >= len(maze[0]): continue
            if (nr, nc) in visited:
                node = visited[nr, nc]
                actual_picosecs, node_picosecs = actual[2], node[2]
                if node_picosecs > actual_picosecs + x:
                    cheat_ident = [(r + dr * k, c + dc * k) for k in range(1, x) if maze[r + dr * k][c + dc * k] == '#']
                    cheat_ident = tuple(sum(cheat_ident, ()))
                    known_cheat_size = -1
                    if cheat_ident in cheats:
                        print('Cheat already used')
                        known_cheat_size = cheats[cheat_ident]
                    size_of_cheat = node_picosecs - (actual_picosecs + x)
                    cheats[cheat_ident] = max(known_cheat_size, size_of_cheat)
                    print(f'Cheat found by {(r, c)}, Cheat len: {x}, Size: {size_of_cheat}')
                    break


maze = open("input/20-1.txt").read().splitlines()
start = start_pos()
path = bfs(start)
print_path(path)
end = path[-1]
print(f'From start [{start[0]}, {start[1]}] to [{end[0]}, {end[1]}] tooks {end[2]} picosecs')
visited = {(value[0], value[1]): value for value in path}
cheats = {}
for i in range(len(path)):
    cheat(path, visited, i)

print(len(list(filter(lambda x: x >=100, cheats.values()))))
#print(sorted(cheats.values()))


