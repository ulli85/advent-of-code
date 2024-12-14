import re

HEIGHT = 103
WIDTH = 101
STEPS = 100
X_QUADRANT = (WIDTH - 1) // 2
Y_QUADRANT = (HEIGHT - 1) // 2

def pos_n(pos: int, velocity: int, steps: int, max: int):
    pos = (pos + velocity * steps) % max
    if pos < 0: pos += max
    return pos

res = re.findall("p=(\\d+),(\\d+) v=(-?\\d+),(-?\\d+)", open("input/14-1.txt").read())
ld_count = lt_count = rd_count = rt_count = 0
for i, robot in enumerate(res):
    px, py, vx, vy = int(robot[0]), int(robot[1]), int(robot[2]), int(robot[3])
    xn, yn = (px + vx * STEPS) % WIDTH, (py + vy * STEPS) % HEIGHT

    if yn < Y_QUADRANT:
        if xn < X_QUADRANT:
            lt_count += 1
        if xn > X_QUADRANT:
            rt_count += 1
    if yn > Y_QUADRANT:
        if xn < X_QUADRANT:
            ld_count += 1
        if xn > X_QUADRANT:
            rd_count += 1
print(lt_count * rt_count * ld_count * rd_count)
