from enum import Enum


class Display(Enum):
    NUMERIC = 1,
    ARROW = 2


NDPL_ARR = [['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            [None, '0', 'A']]

NDPL = {'7': [0, 0], '8': [0, 1], '9': [0, 2],
        '4': [1, 0], '5': [1, 1], '6': [1, 2],
        '1': [2, 0], '2': [2, 1], '3': [2, 2],
        '0': [3, 1], 'A': [3, 2]
        }

ARROWS = {
    'AA': '', 'A<': ['v<<', '<v<'], 'Av': ['v<', '<v'], 'A>': 'v', 'A^': '<',
    '^^': '', '^A': '>', '^v': 'v', '^<': 'v<', '^>': ['>v', 'v>'],
    '<<': '', '<A': ['>>^', '>^>'], '<v': '>', '<^': '>^', '<>': '>>',
    '>>': '', '>A': '^', '>v': '<', '>^': ['^<', '<^'], '><': '<<',
    'vv': '', 'v<': '<', 'v>': '>', 'v^': '^', 'vA': ['>^', '^>']}

ALL_PATHS = set()


def numeric_path(start, row) -> [str]:
    s_pos = NDPL[start]
    e_pos = NDPL[row[0]]

    dy = e_pos[0] - s_pos[0]
    dx = e_pos[1] - s_pos[1]

    char = NDPL_ARR[s_pos[0] + dy][s_pos[1]]
    leftright = '<' if dx < 0 else '>'
    updown = 'v' if dy > 0 else '^'
    if char is None:
        return [leftright * abs(dx) + updown * abs(dy)]

    char = NDPL_ARR[s_pos[0]][s_pos[1] + dx]
    if char is None:
        return [updown * abs(dy) + leftright * abs(dx)]

    return [leftright * abs(dx) + updown * abs(dy), updown * abs(dy) + leftright * abs(dx)]


def arrow_path(start, row) -> [str]:
    mv = ARROWS[start + row[0]]
    if type(mv) is str: return [mv]
    return mv


def next_path(start: str, row: str, disp: Display) -> [str]:
    if Display.NUMERIC == disp:
        return numeric_path(start, row)
    return arrow_path(start, row)


def transform(start: str, row: str, disp: Display = Display.NUMERIC, result: str = ''):
    if len(row) == 0:
        ALL_PATHS.add(result)
        return
    for path in next_path(start, row, disp):
        transform(row[0], row[1:], disp, result + path + 'A')


lines = open("input/21-1.txt").read().splitlines()
sum = 0
for line in lines:
    ALL_PATHS.clear()
    transform('A', line)
    for a in 0, 1:
        paths = list(ALL_PATHS)
        ALL_PATHS.clear()
        for path in paths:
            transform('A', path, Display.ARROW)

    min_path = min(ALL_PATHS, key=len)
    row_num = int(line[0:len(line) - 1])
    print(f'{line} {min_path}\n {len(min_path)} * {row_num}')
    #print(ALL_PATHS)
    sum += len(min_path) * row_num
print(sum)
