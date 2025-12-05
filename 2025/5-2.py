data = open('input/5.txt').read().splitlines()
rng = sorted(list(map(lambda x: list(map(int, x.split('-'))), data[0: data.index('')])), key=lambda x: x[0])
res = []
i = 0
while i < len(rng) - 1:
    if rng[i][1] >= rng[i + 1][0]:
        new_range = [rng[i][0], max(rng[i][1], rng[i + 1][1])]
        rng = rng[0:i] + [new_range] + rng[i + 2:]
    else: i += 1
print(sum(map(lambda x: x[1] - x[0] + 1, rng)))