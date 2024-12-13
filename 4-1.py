f = open("aoc2024-4-1-input.txt", "r")
content = f.read()
lines = content.splitlines()
x_indexes = []

directions = [[0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]

# hledam vsechna XMAS - diagonalne vertikalne
# najdu vsechna X a ulozim jako indexy
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == 'X':
            x_indexes.append([y, x])
xmas_cnt = 0
word = 'X'
for x_index in x_indexes:
    for direction in directions:
        if word == 'XMAS':
            xmas_cnt += 1
        word = 'X'
        actual_pos = x_index.copy()
        for w_len in range(len('XMAS') - 1):
            actual_pos[0] += direction[0]
            actual_pos[1] += direction[1]
            if actual_pos[0] < 0 or actual_pos[1] < 0 or actual_pos[0] >= len(lines) or actual_pos[1] >= len(lines[0]):
                break
            word += lines[actual_pos[0]][actual_pos[1]]

if word == 'XMAS':
    xmas_cnt += 1
print(xmas_cnt)
