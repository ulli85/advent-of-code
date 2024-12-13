def in_range(value: int, min: int, max: int) -> bool:
    return min <= value < max

f = open("aoc2024-4-2-input.txt", "r")
content = f.read()
lines = content.splitlines()
a_indexes = []

max_y = len(lines)
max_x = len(lines[0])
xmas_cnt = 0

for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == 'A':
            a_indexes.append([y, x])

for a_index in a_indexes:
    tl_y1 = a_index[0] - 1
    tl_x1 = a_index[1] - 1
    tl_y2 = a_index[0] + 1
    tl_x2 = a_index[1] + 1

    if not in_range(tl_y1, 0, max_y) or not in_range(tl_y2, 0, max_y) or not in_range(tl_x1, 0, max_x) or not in_range(
            tl_x2, 0, max_x):
        continue

    mas_top_left = lines[tl_y1][tl_x1] + 'A' + lines[tl_y2][tl_x2]

    if not (mas_top_left == 'MAS' or mas_top_left == 'SAM'):
        continue

    tr_y1 = a_index[0] + 1
    tr_x1 = a_index[1] - 1
    tr_y2 = a_index[0] - 1
    tr_x2 = a_index[1] + 1

    if not in_range(tr_y1, 0, max_y) or not in_range(tr_y2, 0, max_y) or not in_range(tr_x1, 0, max_x) or not in_range(
            tr_x2, 0, max_x):
        continue

    mas_top_right = lines[tr_y1][tr_x1] + 'A' + lines[tr_y2][tr_x2]

    if mas_top_right == 'MAS' or mas_top_right == 'SAM':
        xmas_cnt += 1
print(xmas_cnt)
