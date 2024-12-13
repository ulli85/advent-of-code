import numpy as np


def in_field(y: int, x: int) -> bool:
    if (y < 0 or y >= len(field)) or (x < 0 or x >= len(field[0])):
        return False
    return True


class Region:
    ID = 0
    all_regions: ['Region'] = []

    def __init__(self, plant_type: str):
        self.id = Region.ID
        self.plant_type = plant_type
        self.regions = 0
        self.fence = 0
        Region.ID += 1

    def __str__(self):
        return f"{self.regions} x {self.fence}"

    def up(self, y: int, x: int)-> bool:
        return not self.no_up(y, x)

    def down(self, y: int, x: int)-> bool:
        return not self.no_down(y, x)

    def left(self, y: int, x: int)-> bool:
        return not self.no_left(y, x)

    def right(self, y: int, x: int)-> bool:
        return not self.no_right(y, x)

    def no_up(self, y: int, x: int) -> bool:
        if y - 1 < 0 or arr[y - 1][x] != self.id: return True
        return False

    def no_down(self, y: int, x: int) -> bool:
        if y + 1 >= len(arr) or arr[y + 1][x] != self.id: return True
        return False

    def no_right(self, y: int, x: int) -> bool:
        if x + 1 >= len(arr[0]) or arr[y][x + 1] != self.id: return True
        return False

    def no_left(self, y: int, x: int) -> bool:
        if x - 1 < 0 or arr[y][x - 1] != self.id: return True
        return False


def dfs_go(y, x, region: Region):
    if arr[y][x] != -1:
        return
    region.regions += 1
    arr[y][x] = region.id
    for dy, dx in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        adjy = y + dy
        adjx = x + dx
        if in_field(adjy, adjx) and region.plant_type == field[adjy][adjx]:
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

for r in Region.all_regions:
    # vodorovne hrany - prochazim matici po radcich smerem doprava
    for y in range(len(field)):
        for x in range(len(field[0])):
            if arr[y][x] == r.id:
                if (r.no_left(y, x) or (r.left(y, x) and r.up(y, x - 1))) and r.no_up(y, x): r.fence += 1  # horni vodorovna
                if (r.no_left(y, x) or (r.left(y, x) and r.down(y, x - 1))) and r.no_down(y, x): r.fence += 1  # spodni vodorovna

    # svisle hrany - prochazim matici po sloupcich smerem dolu
    for x in range(len(arr[0])):
        for y in range(len(field)):
            if arr[y][x] == r.id:
                if (r.no_up(y, x) or (r.up(y, x) and r.left(y - 1, x))) and r.no_left(y, x): r.fence += 1  # leva svisla
                if (r.no_up(y, x) or (r.up(y, x) and r.right(y - 1, x))) and r.no_right(y, x): r.fence += 1  # prava svisla
sum = 0
for region in Region.all_regions:
    reg_sum = region.regions * region.fence
    sum +=reg_sum
    print(f"{region.plant_type}({region.id}) {region.regions} x {region.fence} = {reg_sum}")
print(sum)
