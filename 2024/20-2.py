from collections import deque

maze = open("input/20-1.txt").read().splitlines()
cheats = {}


def start_pos() -> tuple[int, int]:
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                return r, c
    raise Exception("Couldn't find start position")


def dist(a: tuple[int, int, int, tuple[...] | None], b: tuple[int, int, int, tuple[...] | None]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def adjacents(path: [tuple[int, int, int, tuple[...] | None]], index: int, radius: int) -> [
    tuple[int, int, int, tuple[...] | None]]:
    a = path[index]
    return list(filter(lambda b: b[2] > a[2] and dist(a, b) <= radius, path))


def bfs(start: tuple[int, int]) -> [tuple[int, int, int, tuple[...] | None]]:
    first = (*start, 0, None)
    visited = {}
    q = deque([first])
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


def cheat(path: [], start: int, radius: int):
    actual = path[start]
    r, c, actual_picosecs = actual[0], actual[1], actual[2]
    adj = adjacents(path, start, radius)
    for a in adj:
        cheat_id = tuple(sorted(((r, c), (a[0], a[1]))))
        distance = dist(actual, a)
        size_of_cheat = a[2] - (actual_picosecs + distance)
        if cheat_id in cheats:
            cheats[cheat_id] = max(cheats[cheat_id], distance)
        else:
            cheats[cheat_id] = size_of_cheat


path = bfs(start_pos())
for i in range(len(path)): cheat(path, i, 20)
print(len(list(filter(lambda x: x >= 100, cheats.values()))))
