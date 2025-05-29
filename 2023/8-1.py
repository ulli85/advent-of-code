import re

lines = open('input/8').read().splitlines()
instructions = lines[0]
network = {k: v for k, v in
           list(map(lambda a: (a[0], (a[1], a[2])), map(lambda line: re.findall('\\w{3}', line), lines[2:])))}

dir_2_index = lambda x: 0 if x == 'L' else 1
now, dest = 'AAA', 'ZZZ'

for step in range(10000000):
    direction = instructions[step % len(instructions)]
    next_nodes = network[now]
    now = next_nodes[dir_2_index(direction)]

    if now == dest:
        print(step + 1)
        exit(0)
print(f'Path not found actual: {now}')
