lines = open('input/11').read().splitlines()

N = len(lines)
galaxies = []

for y in range(N):
    for x in range(N):
        if lines[y][x] == '#':
            galaxies.append((y, x))

y_set = set(map(lambda yx: yx[0], galaxies))
x_set = set(map(lambda yx: yx[1], galaxies))

y_expands = [0 if y in y_set else 1 for y in range(N)]
x_expands = [0 if x in x_set else 1 for x in range(N)]
total_distance = 0
for i in range(0, len(galaxies) - 1):
    for j in range(i + 1, len(galaxies)):
        g1, g2 = galaxies[i], galaxies[j]
        dy = abs(g1[0] - g2[0]) + sum(y_expands[min(g1[0], g2[0]): max(g1[0], g2[0])])
        dx = abs(g1[1] - g2[1]) + sum(x_expands[min(g1[1], g2[1]): max(g1[1], g2[1])])
        total_distance += dy + dx

print(total_distance)
