import sys

sys.setrecursionlimit(15000)

lines = list(map(lambda l: l.split(': '), open('input/11.txt').read().splitlines()))
lines = list(map(lambda i: [i[0], tuple(i[1].split(' '))], lines))

network = {k: v for k, v in lines}
visited = {k: v for k, v in zip(network.keys(), [False] * len(network))}
path_count = 0
paths = set()

def dfs_go(path: [tuple]):
    global path_count

    if len(path) == 0:
        return
    src, index = path.pop()
    dests = network[src]

    if index >= len(dests):
        return dfs_go(path)

    dst = dests[index]
    path_nodes = set(map(lambda x: x[0], path))
    # cycle detection
    cycle_detected = dst in path_nodes and visited[dst]
    path_next = path + [tuple([src, index + 1])]

    if cycle_detected:
        return dfs_go(path_next)

    if dst == 'out':
        path_count += 1
        nodes = list(map(lambda x: x[0], path_next))
        nodes += [dst]
        print(nodes)
        new_path = tuple(nodes)
        assert new_path not in path
        paths.add(new_path)
        return dfs_go(path_next)
    else:
        visited[dst] = True
        dfs_go(path_next + [tuple([dst, 0])])

dfs_go(([('you', 0)]))
print(path_count)