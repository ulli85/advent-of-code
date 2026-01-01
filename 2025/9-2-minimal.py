from collections import defaultdict


INPUT = list(map(int, open('input/9.txt').read().replace('\n', ',').split(',')))
POINTS = list(zip(INPUT[0::2], INPUT[1::2]))
POINTS += [POINTS[0]]
EDGES = list(zip(POINTS[::1], POINTS[1::]))
H_EDGES = defaultdict(set)
V_EDGES = defaultdict(set)

for i in range(len(EDGES)):
    (x1, y1), (x2, y2) = EDGES[i - 1]
    if y1 == y2:
        H_EDGES[y1].add((min(x1, x2), max(x1, x2)))
    else:
        V_EDGES[x1].add((min(y1, y2), max(y1, y2)))


def is_on_edge(xp, yp):
    if len(list(filter(lambda e: e[0] <= xp <= e[1], H_EDGES[yp]))) > 0:
        return True

    if len(list(filter(lambda e: e[0] <= yp <= e[1], V_EDGES[xp]))) > 0:
        return True
    return False


def is_point_inside_polygon(xp, yp, edges):
    """Ray casting algorithm explained here https://www.youtube.com/watch?v=RSXM9bgqxJM"""
    if is_on_edge(xp, yp):
        return True
    cnt = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp - y1) / (y2 - y1)) * (x2 - x1):
            cnt += 1

    return cnt % 2 == 1

def is_rectangle_inside_polygon(x1, y1, x2, y2):
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)

    # check corner
    if not is_point_inside_polygon(x2, y1, EDGES):
        return False

    # check corner
    if not is_point_inside_polygon(x1, y2, EDGES):
        return False

    # check middle point
    ymiddle, xmiddle = ymax - ((ymax - ymin) // 2), xmax - (xmax - ((xmax - xmin) // 2))
    if not is_point_inside_polygon(xmiddle, ymiddle, EDGES):
        return False


    # check rectangle vertical edges
    for y in range(ymin, ymax + 1):
        for x in [xmin, xmax]:
            if not is_point_inside_polygon(x, y, EDGES):
                return False

    # check rectangle horizontal edges
    for x in range(xmin, xmax + 1):
        for y in [ymin, ymax]:
            if not is_point_inside_polygon(x, y, EDGES):
                return False
    return True


def area_of_rectangle(pt1, pt2):
    _dx = max(pt1[0], pt2[0]) - min(pt1[0], pt2[0])
    _dy = max(pt1[1], pt2[1]) - min(pt1[1], pt2[1])
    if _dx > 0 and _dy > 0:
        return (_dx + 1) * (_dy + 1)
    return 0


def get_rectangles_desc():
    explored = set()
    area_2_points = defaultdict(list)
    for i in range(len(POINTS)):
        for j in range(len(POINTS)):
            if i == j: continue
            pt_i, pt_j = POINTS[i], POINTS[j]
            area_sz = area_of_rectangle(pt_i, pt_j)
            if area_sz == 0: continue
            if (pt_i, pt_j) in explored or (pt_j, pt_i) in explored: continue
            area_2_points[area_sz] += [(pt_i, pt_j)]
            explored.add((pt_i, pt_j))
            explored.add((pt_j, pt_i))
    return dict(sorted(area_2_points.items(), reverse=True))


aor = get_rectangles_desc()
rectangle_found = False
it = iter(aor)

while not rectangle_found:
    area = next(it)
    points_list = aor[area]
    for (x1, y1), (x2, y2) in points_list:
        if is_rectangle_inside_polygon(x1, y1, x2, y2):
            rectangle_found = True
            print(f'({x1}, {y1}) x ({x2}, {y2}) -> {area}')
            break
