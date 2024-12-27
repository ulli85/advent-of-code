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
    'AA': '', 'A<': 'v<<', 'Av': ['v<', '<v'], 'A>': 'v', 'A^': '<',
    '^^': '', '^A': '>', '^v': 'v', '^<': 'v<', '^>': ['>v', 'v>'],
    '<<': '', '<A': ['>>^', '>^>'], '<v': '>', '<^': '>^', '<>': '>>',
    '>>': '', '>A': '^', '>v': '<', '>^': ['^<', '<^'], '><': '<<',
    'vv': '', 'v<': '<', 'v>': '>', 'v^': '^', 'vA': ['>^', '^>']}


def numeric_path(start, row):
    s_pos = NDPL[start]
    e_pos = NDPL[row[0]]

    dy = e_pos[0] - s_pos[0]
    dx = e_pos[1] - s_pos[1]

    char = NDPL_ARR[s_pos[0] + dy][s_pos[1]]
    leftright = '<' if dx < 0 else '>'
    updown = 'v' if dy > 0 else '^'
    if char is None:
        return leftright * abs(dx) + updown * abs(dy)
    return updown * abs(dy) + leftright * abs(dx)


def arrow_path(start, row):
    mv = ARROWS[start + row[0]]

    if type(mv) is str: return mv

    # last character, it doesn't matter what we pick up
    if len(row) == 1: return mv[0]
    # 'mv' is an array so we have more possibilities,
    # we need to lookup further at row to pick up optimal solution for shorther path

    path = mv[0]
    for case in mv:
        if case[-1] == row[1]:
            path = case
            break
    return path


def next_path(start: str, row: str, disp: Display) -> str:
    if Display.NUMERIC == disp:
        return numeric_path(start, row) + 'A'
    return arrow_path(start, row) + 'A'


def transform(start: str, row: str, result: str = '', disp: Display = Display.NUMERIC) -> str:
    if len(row) == 0: return result
    return transform(row[0], row[1:], result + next_path(start, row, disp), disp)


lines = open("input/21-1.txt").read().splitlines()
sum = 0
for line in lines:
    s1 = transform('A', line)
    s2 = transform('A', s1, '', Display.ARROW)
    s3 = transform('A', s2, '', Display.ARROW)
    row_num = int(line[0:len(line) - 1])
    print(s3)
    print(s2)
    print(s1)
    print(line)
    # print(f'{line} -> {s}')
    # print(f'{len(s)} * {row_num}')
    sum += len(s3) * row_num
print(sum)
