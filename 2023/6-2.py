from functools import reduce


def find_min(min_, max_, race_time, distance, sol=-1):
    if min_ + 1 == max_: return sol
    hold_time = (max_ + min_) // 2
    if (race_time - hold_time) * hold_time > distance:
        return find_min(min_, hold_time, race_time, distance, hold_time)
    return find_min(hold_time, max_, race_time, distance, sol)


def find_max(min_, max_, race_time, distance, sol=-1):
    if min_ + 1 == max_: return sol
    hold_time = (max_ + min_) // 2
    if (race_time - hold_time) * hold_time > distance:
        return find_max(hold_time, max_, race_time, distance, sol)
    return find_max(min_, hold_time, race_time, distance, hold_time)


l = open('input/6-2').read().splitlines()
times = map(int, l[0].split(':')[1].split())
distances = map(int, l[1].split(':')[1].split())

sol_cnts = map(lambda x: find_max(1, x[0], x[0], x[1]) - find_min(1, x[0], x[0], x[1]), zip(times, distances))
print(reduce(lambda x, y: x * y, sol_cnts))
