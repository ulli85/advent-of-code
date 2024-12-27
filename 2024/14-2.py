import re
import numpy as np

HEIGHT = 103
WIDTH = 101
STEPS = 100
X_HALF = (WIDTH - 1) // 2
Y_HALF = (HEIGHT - 1) // 2

res = re.findall("p=(\\d+),(\\d+) v=(-?\\d+),(-?\\d+)", open("input/14-1.txt").read())

longest_sequence = 0
best_step = 0
for step in range(1, WIDTH * HEIGHT + 1):
    lu = ld = ru = rd = 0
    visual = np.full((HEIGHT, WIDTH), '.', dtype=str)
    for robot in res:
        px, py, vx, vy = int(robot[0]), int(robot[1]), int(robot[2]), int(robot[3])
        xn, yn = (px + vx * step) % WIDTH, (py + vy * step) % HEIGHT
        visual[yn][xn] = '*'
    x = X_HALF + 1
    y = 0
    while y < HEIGHT:
        while y < HEIGHT and visual[y][x] == '.':
            y += 1
        sequence = 0
        while y < HEIGHT and visual[y][x] == '*':
            sequence += 1
            y += 1
        if sequence > longest_sequence:
            longest_sequence = sequence
            best_step = step
            for line in visual:
                print(''.join(line))
print(best_step)

