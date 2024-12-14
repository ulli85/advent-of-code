import re
import numpy as np

HEIGHT = 103
WIDTH = 101
STEPS = 100
X_HALF = (WIDTH - 1) // 2
Y_HALF = (HEIGHT - 1) // 2

res = re.findall("p=(\\d+),(\\d+) v=(-?\\d+),(-?\\d+)", open("input/14-1.txt").read())

min_mp = 999999999999999
best_step = 0
for step in range(1, WIDTH * HEIGHT + 1):
    lu = ld = ru = rd = 0
    visual = np.full((HEIGHT, WIDTH), '.', dtype=str)
    for robot in res:
        px, py, vx, vy = int(robot[0]), int(robot[1]), int(robot[2]), int(robot[3])
        xn, yn = (px + vx * step) % WIDTH, (py + vy * step) % HEIGHT
        visual[yn][xn] = '*'
        if yn < Y_HALF:
            if xn < X_HALF:
                lu += 1
            if xn > X_HALF:
                ru += 1
        if yn > Y_HALF:
            if xn < X_HALF:
                ld += 1
            if xn > X_HALF:
                rd += 1

    sm = lu * ld * ru * rd
    if sm < min_mp:
        min_mp = sm
        best_step = step
print(best_step)

