from functools import reduce
from itertools import product

data = open("input/3").read().splitlines()
used_coords = set()

def get_row_num(y_coord: int, x_coord: int) -> int:
    xst = x_coord
    while xst > 0 and data[y_coord][max(0, xst - 1)].isnumeric(): xst -= 1
    result = []
    while xst < len(data[y]) and data[y_coord][xst].isnumeric():
        result.append(data[y_coord][xst])
        used_coords.add((y_coord, xst))
        xst += 1
    return int(''.join(result))

suma = 0
for y, line in enumerate(data):
    last_index = 0
    while last_index < len(data[y]):
        last_index = line.find('*', last_index)
        if last_index == -1: break
        xs, xe = max(0, last_index - 1), min(len(line) - 1, last_index + 1)
        cols = [i for i in range(xs, xs + (xe - xs) + 1)]
        coords = {*product([max(0, y - 1), y, min(len(data) - 1, y + 1)], cols)}
        coords.remove((y, last_index))
        last_index += 1

        digit_coords = list(filter(lambda c: data[c[0]][c[1]].isnumeric(), coords))

        if len(digit_coords) > 1:
            numbers = []
            for digit_coord in digit_coords:
                if digit_coord not in used_coords:
                    numbers.append(get_row_num(digit_coord[0], digit_coord[1]))
            if len(numbers) > 1:
                suma += reduce(lambda a, b: a * b, numbers)
print(suma)