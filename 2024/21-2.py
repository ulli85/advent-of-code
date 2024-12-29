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
    'AA': '', 'A<': ['v<<', '<v<'], 'Av': ['v<', '<v'], 'A>': 'v', 'A^': '<',
    '^^': '', '^A': '>', '^v': 'v', '^<': 'v<', '^>': ['>v', 'v>'],
    '<<': '', '<A': ['>>^', '>^>'], '<v': '>', '<^': '>^', '<>': '>>',
    '>>': '', '>A': '^', '>v': '<', '>^': ['^<', '<^'], '><': '<<',
    'vv': '', 'v<': '<', 'v>': '>', 'v^': '^', 'vA': ['>^', '^>']}


def numeric_path(start, row, out):
    ay, ax = NDPL[start]  # actual y,x
    ey, ex = NDPL[row[0]]  # end y, x
    dy = ey - ay
    dx = ex - ax
    leftright = '<' if dx < 0 else '>'
    updown = 'v' if dy > 0 else '^'

    # first row position is a gap, we need change column first and then row
    if NDPL_ARR[ay + dy][ax] is None:
        return leftright * abs(dx) + updown * abs(dy)

    # column position is a gap, we need change row first and then column
    if NDPL_ARR[ay][ax + dx] is None:
        return updown + abs(dy) + leftright * abs(dx)

    # for all other cases wee need to find out if is better to change column first and then row or otherwise
    # change row first and then the column
    # for both possibilities we do calculations. Based on this we choose the 'more perspective' one then
    # check if last output element is the same as first one of transition string which would be appended to the output
    # todo todo todo lada

    return updown * abs(dy) + leftright * abs(dx)


def arrow_path(start, row, out):
    mv = ARROWS[start + row[0]]

    # one possibility of transition from start to row[0]
    if type(mv) is str: return mv

    # 'mv' is an array with exactly two possibilities of transition
    # its length are the same, but the cost of transitions in next step could be different
    # we need to choose variant with minimal effort (count of characters) in next round as possible

    score0 = 0
    distance0 = 99
    # for both possibilities we do calculations. Based on this we choose the 'more perspective' one then
    # check if last output element is the same as first one of transition string which would be appended to the output
    if len(out) > 0 and out[-1] == mv[0][0]: score0 += 1
    if len(row) > 1:
        # check if next-first character of input is same as last character of output
        if row[1] == mv[0][-1]: score0 += 1
        next = ARROWS[mv[0][-1] + row[1]]
        # save distance from last output character to the next-first of input
        if type(next) is str:
            distance0 = len(next)
        else:
            distance0 = len(next[0])
    # do the same calculations for possibility number two
    score1 = 0
    distance1 = 99
    if len(out) > 0 and out[-1] == mv[1][0]: score1 += 1
    if len(row) > 1:
        if row[1] == mv[1][-1]: score1 += 1
        next = ARROWS[mv[1][-1] + row[1]]
        if type(next) is str:
            distance1 = len(next)
        else:
            distance1 = len(next[0])
    # comparing 'perspectivness' of possibilities and return the probably better one
    if score1 > score0: return mv[1]
    if distance1 < distance0: return mv[1]
    if mv[1].find('<<') >= 0 or mv[1].find('>>') >= 0: return mv[1]
    return mv[0]


def next_path(start: str, row: str, out, disp: Display) -> str:
    if Display.NUMERIC == disp:
        return numeric_path(start, row, out) + 'A'
    return arrow_path(start, row, out) + 'A'


def transform(start: str, row: str, disp: Display = Display.NUMERIC, out: str = '') -> str:
    if len(row) == 0: return out
    out += next_path(start, row, out, disp)
    return transform(row[0], row[1:], disp, out)


lines = open("input/21-1.txt").read().splitlines()
sum = 0
for line in lines:
    s1 = transform('A', line)
    assert '^A<<^^A>>AvvvA' == s1
    s2 = transform('A', s1, Display.ARROW)
    s3 = transform('A', s2, Display.ARROW)
    row_num = int(line[0:len(line) - 1])
    print(f'{s3} {len(s3)}')
    print(s2)
    print(s1)
    print(line)
    # print(f'{line} -> {s}')
    # print(f'{len(s)} * {row_num}')
    sum += len(s3) * row_num
print(sum)
