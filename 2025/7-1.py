data = open('input/7.txt').read().splitlines()
grid = list(map(list, data))

s = data[0].index('S')
width = len(data[0])

beams, beams_n, paths = [0] * width, [0] * width, [0] * width
beams[s] = 1

total = 0
for i, r in enumerate(grid[1:], 1):
    for k, b in enumerate(beams):
        if beams[k] == 0: continue
        if r[k] == '^':
            beams_n[k - 1] = 1
            beams_n[k + 1] = 1
        else:
            beams_n[k] = 1
    total += len(list(filter(lambda x: x == (1, 0), zip(beams, beams_n))))
    beams = beams_n.copy()
    beams_n = [0] * width
print(total)
