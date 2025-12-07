import numpy as np

data = open('input/7.txt').read().splitlines()
grid = list(map(list, data))

s = data[0].index('S')
width = len(data[0])

beams = [0] * width
beams[s] = 1

for i, r in enumerate(grid[1:], 1):
    beams_n = [0] * width
    for k, b in enumerate(beams):
        if beams[k] == 0: continue
        if r[k] == '^':
            beams_n[k + 1] = beams[k]
            beams_n[k - 1] = beams[k] + beams[k - 1]
            if r[k - 2] == '^':
                beams_n[k - 1] += beams[k - 2]
        else:
            beams_n[k] += beams[k]
    beams = beams_n
print(sum(beams))