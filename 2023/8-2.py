import re

lines = open('input/8').read().splitlines()
instructions = lines[0]
network = {k: v for k, v in
           list(map(lambda a: (a[0], (a[1], a[2])), map(lambda line: re.findall('\\w{3}', line), lines[2:])))}

nows = list(filter(lambda n: n[-1] == 'A', network.keys()))
routes = [{}] * len(nows)
cycle_found_flag = [-1] * len(nows)

dir_2_index = lambda x: 0 if x == 'L' else 1
step = 0

while sum(cycle_found_flag) != 0:
    nexts = []
    for i, now in enumerate(nows):
        if now in routes[i]:
            cycle_found_flag[i] = 0
        routes[i][now] = step if now[-1] == 'Z' else 0
        direction = instructions[step % len(instructions)]
        next_nodes = network[now]
        nexts += [next_nodes[dir_2_index(direction)]]
    nows = nexts
    step += 1

print(sum(routes[0].values()))

#dic_end_steps = [list(filter(lambda k, v: v > 0, route.items())) for route in routes]
print(f'All cycles found!')
