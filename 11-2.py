def blink(num: int):
    if num == 0: return [1]
    if len(str(num)) % 2 == 0:
        half = int(len(str(num)) / 2)
        left = str(num)[0:half]
        right = str(num)[half::]
        return [int(left), int(right)]
    return [2024 * num]


def put_stone(stone_num: int, times: int, into: dict):
    if stone_num in into:
        into[stone_num] += times
    else:
        into[stone_num] = times

stones = {}
f = open("aoc2024-11-1-input.txt", "r")
for i in [int(x) for x in f.read().split()]:
    put_stone(i, 1, stones)

blink_cnt = 75
for i in range(blink_cnt):
    next_stones = {}
    for stone_num, count in stones.items():
        after_blink = blink(stone_num)
        for next_stone in after_blink:
            put_stone(next_stone, count, next_stones)
    stones = next_stones
print(sum(stones.values()))
