from functools import reduce
from itertools import product

data = open("input/3").read().splitlines()
used_coords = set()

def get_row_num(y_coord: int, x_coord: int) -> int:
    xst = x_coord
    while xst > 0:
        if data[y_coord][xst - 1].isnumeric():
            xst -= 1
        else: break
    xst = max(0, xst)
    result = []
    while xst < len(data[y]):
        char = data[y_coord][xst]
        if char.isnumeric():
            result.append(data[y_coord][xst])
            used_coords.add((y_coord, xst))
        else:
            break
        xst += 1

    return int(''.join(result))

num_set = {str(i) for i in range(0, 10)}
suma = 0
for y, line in enumerate(data):
    last_index = 0
    while last_index < len(data[y]):
        last_index = line.find('*', last_index)
        if last_index == -1: break
        y_up, y_dwn = max(0, y - 1), min(len(data) - 1, y + 1)
        xs, xe = max(0, last_index - 1), min(len(line) - 1, last_index + 1)
        last_index += 1
        cols = [i for i in range(xs, xs + (xe - xs) + 1)]
        coords = {(y, xs), (y, xe)}.union(product([y_up], cols)).union(product([y_dwn], cols))
        digit_coords = sorted(list(filter(lambda c: data[c[0]][c[1]] in num_set, coords)))
        if len(digit_coords) > 1:
            numbers = []
            for digit_coord in digit_coords:
                if digit_coord not in used_coords:
                    numbers.append(get_row_num(digit_coord[0], digit_coord[1]))
            if len(numbers) > 1:
                suma += reduce(lambda a, b: a * b, numbers)
print(suma)
