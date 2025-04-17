import re
from itertools import product

num_or_dot = {str(i) for i in range(0, 10)}.union({'.'})
data = open("input/3").read().splitlines()
suma = 0
for y, line in enumerate(data):
    last_index = 0
    for num in re.findall('\\d+', line):
        y_up, y_dwn = max(0, y - 1), min(len(data) - 1, y + 1)
        last_index = line.index(num, last_index)
        xs, xe = max(0, last_index - 1), min(len(line) - 1, last_index + len(num))
        last_index += len(num)
        cols = [i for i in range(xs, xs + (xe - xs) + 1)]
        coords = {(y, xs), (y, xe)}.union(product([y_up], cols)).union(product([y_dwn], cols))
        adjacent_symbols = list(filter(lambda c: data[c[0]][c[1]] not in num_or_dot, coords))
        if len(adjacent_symbols) > 0: suma += int(num)
print(suma)