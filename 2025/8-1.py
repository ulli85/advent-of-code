import math
from functools import reduce


def distance(c1, c2):
    return round(math.sqrt(pow(c1[0] - c2[0], 2) + pow(c1[1] - c2[1], 2) + pow(c1[2] - c2[2], 2)), 3)


data = list(map(lambda x: tuple(map(int, x.split(','))), open('input/8.txt').read().splitlines()))
DISTANCES = {}

for k in data:
    for j in data:
        if k != j and (k, j) not in DISTANCES and (j, k) not in DISTANCES:
            DISTANCES[(k, j)] = distance(k, j)


DISTANCES_SORTED = {k: v for k, v in sorted(DISTANCES.items(), key=lambda item: item[1])}
COORD_2_GRP_ID = dict(zip(data, [i for i in range(0, len(data))]))
GRP_ID_2_COORDS = dict(zip([i for i in range(0, len(data))], [set() for i in range(0, len(data))]))
connection_limit = 1000
actual_connection = 0
dst_iter = iter(DISTANCES_SORTED)

while actual_connection < connection_limit:
    actual_connection += 1
    c1, c2 = next(dst_iter)
    # print(f'#{actual_connection} {c1} -> {c2} Dst: {DISTANCES_SORTED[(c1, c2)]}')
    gr_id1, gr_id2 = COORD_2_GRP_ID[c1], COORD_2_GRP_ID[c2]
    if gr_id1 == gr_id2:
        # print('Same group, skip. Connection counts')
        continue
    COORD_2_GRP_ID[c2] = gr_id1
    group1, group2 = GRP_ID_2_COORDS[gr_id1], GRP_ID_2_COORDS[gr_id2]
    group1 = group1.union([c2])
    group2 = group2.union([c1])
    for c_in_g2 in group2:
        COORD_2_GRP_ID[c_in_g2] = gr_id1
    united_groups = group1.union(group2)
    GRP_ID_2_COORDS[gr_id1] = united_groups
    GRP_ID_2_COORDS.pop(gr_id2)
    print(list(sorted(filter(lambda g: g > 0, map(len, GRP_ID_2_COORDS.values())), reverse=True)))

res = list(sorted(filter(lambda g: g > 0, map(len, GRP_ID_2_COORDS.values())), reverse=True))
# print(res)
print(reduce(lambda a, b: a * b, res[0:3]))
