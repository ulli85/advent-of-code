import re

lines = open('input/8').read().splitlines()
instructions = lines[0]
network = {k: v for k, v in
           list(map(lambda a: (a[0], {'L': a[1], 'R': a[2]}), map(lambda line: re.findall('\\w{3}', line), lines[2:])))}

node, step = 'AAA', 0

while node != 'ZZZ':
    direction = instructions[step % len(instructions)]
    node_list = network[node]
    node = node_list[direction]
    step += 1
print(step)