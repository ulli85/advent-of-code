l = open('input/5').read().splitlines()
seeds = [int(x) for x in l[0].split(':')[1].split()]
i = 1
mappings = []
s = []
while i < len(l[1:]):
    line = l[i]
    if line == '':
        if len(s) > 0:
            mappings.append(s)
            s = []
        i += 2
        continue

    s += [[int(x) for x in line.split(' ')]]
    i += 1
mappings.append(s)
res = []

for seed in seeds:
    cv = seed
    for tdarr in mappings:
        for dr, sr, rl in tdarr:
            if sr <= cv < sr + rl:
                cv += dr - sr
                break
    res += [cv]
print (min(res))