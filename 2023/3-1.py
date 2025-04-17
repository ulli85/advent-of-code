import re

num_or_dot = {str(i) for i in range(0, 10)}
num_or_dot.add('.')

data = open("input/3").read().splitlines()
suma = 0
for y, line in enumerate(data):
    last_index = 0
    for num in re.findall('\\d+', line):
        last_index = line.index(num, last_index)
        y_up, y_dwn = max(0, y - 1), min(len(data) - 1, y + 1)
        xs, xe = max(0, last_index - 1), min(len(line) - 1, last_index + len(num))
        coords = {(y, xs), (y, xe)}
        for i in range(xs, xs + (xe - xs) + 1):
            coords.add((y_up, i))
            coords.add((y_dwn, i))
        last_index += len(num)
        adjacent_symbols = list(filter(lambda c: data[c[0]][c[1]] not in num_or_dot, coords))
        adjacent_symbol = len(adjacent_symbols) > 0
        if adjacent_symbol: suma += int(num)
print(suma)