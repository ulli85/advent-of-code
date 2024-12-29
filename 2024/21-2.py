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

ALL_PATHS = set()


def numeric_path(start, row):
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


def arrow_path(start, row, out) -> str:
    mv = ARROWS[start + row[0]]

    # one possibility of transition from start to row[0]
    if type(mv) is str: return out + mv

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
    if score1 > score0: return out + mv[1]
    if distance1 < distance0: return out + mv[1]
    if mv[1].find('<<') >= 0 or mv[1].find('>>') >= 0: return out + mv[1]
    return out + mv[0]


def transform(start, row: str, out: str = '') -> str:
    if len(row) == 0: return out
    out = arrow_path(start, row, out) + 'A'
    return transform(row[0], row[1:], out)


def transform_numeric_brutal_force(start: str, row: str, out: str = ''):
    if len(row) == 0:
        ALL_PATHS.add(out)
        return
    for path in numeric_path(start, row):
        transform_numeric_brutal_force(row[0], row[1:], out + path + 'A')


lines = open("input/21-1.txt").read().splitlines()
sum = 0
for line in lines:
    ALL_PATHS.clear()
    transform_numeric_brutal_force('A', line)
    shortest = 99999999
    shortest_path = ''
    for path in list(ALL_PATHS):
        s1 = transform('A', path)
        if len(s1) < shortest:
            shortest = len(s1)
            shortest_path = path
    s1 = shortest_path
    s2 = transform('A', s1)
    s3 = transform('A', s2)
    row_num = int(line[0:len(line) - 1])
    print(f'{s3} {len(s3)}')
    print(s2)
    print(s1)
    print(line)
    # print(f'{line} -> {s}')
    # print(f'{len(s)} * {row_num}')
    sum += len(s3) * row_num
print(sum)
