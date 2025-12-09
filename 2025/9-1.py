points = list(map(int, open('input/9.txt').read().replace('\n', ',').split(',')))
points = list(zip(points[0::2], points[1::2]))
areas = []
for r, c in points:
    for _r, _c in points:
        dy, dx = r - _r, c - _c
        dy, dx = abs(dy) + 1, abs(dx) + 1
        areas += [dy * dx]
print(max(areas))