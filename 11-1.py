from collections import deque

def blink(num: int):
    if num == 0: return [1]
    if len(str(num)) % 2 == 0:
        half = int(len(str(num)) / 2)
        left = str(num)[0:half]
        right = str(num)[half::]
        return [int(left), int(right)]
    return [2024 * num]


f = open("11-1-input.txt", "r")
input = [int(x) for x in f.read().split()]
stones = deque(input)
blink_cnt = 25
for i in range(blink_cnt):
    stones_nxt = deque()
    for stone in stones:
        st_nxt = blink(stone)
        for nxt in st_nxt:
            stones_nxt.append(nxt)
    stones = stones_nxt
print(len(stones))