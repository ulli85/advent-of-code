import numpy as np


def in_grid(y: int, x: int) -> bool:
    if (y < 0 or y >= len(field)) or (x < 0 or x >= len(field[0])):
        return False
    return True


class Region:
    ID = 0
    all_regions: ['Region'] = []

    def __init__(self, plant_type: str):
        self.plant_type = plant_type
        self.regions = 0
        self.fence = 0

    def __str__(self):
        return f"{self.regions} x {self.fence}"


def dfs_go(y, x, region: Region):
    if arr[y][x] != -1:
        return
    region.regions += 1
    arr[y][x] = Region.ID
    adjacents = []
    for dy, dx in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        adjy = y + dy
        adjx = x + dx
        if not in_grid(adjy, adjx):
            region.fence += 1
        elif region.plant_type != field[adjy][adjx]:
            region.fence += 1
        else:
            dfs_go(adjy, adjx, region)


f = open("input/12-1.txt", "r")
field = f.read().splitlines()
field_id = 0
arr = np.full((len(field), len(field[0])), -1, dtype=int)

for y in range(len(field)):
    for x in range(len(field[0])):
        if arr[y][x] == -1:
            plant_type = field[y][x]
            r = Region(plant_type)
            Region.all_regions.append(r)
            dfs_go(y, x, r)
sum = 0
for region in Region.all_regions:
    sum += region.regions * region.fence
print(sum)
