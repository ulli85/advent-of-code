from collections import Counter

disk = []
fid = 0

f = open("aoc2024-9-1-input.txt", "r")
memory = f.read()
for i, char in enumerate(memory):
    x = int(char)
    if i % 2 == 0:
        disk += [fid] * x
        fid += 1
    else:
        disk += [-1] * x

blanks = [i for i, x in enumerate(disk) if x == -1]
memgap = {}
i = 0
while i < len(blanks):
    sz = 0
    while i + sz < len(blanks):
        if i + sz + 1 >= len(blanks): break
        if blanks[i + sz] + 1 < blanks[i + sz + 1]: break
        sz += 1
    memgap[blanks[i]] = sz + 1
    i += sz + 1

flen = 0
c = Counter(disk)
i = len(disk) - 1
while i > 0:
    fid = disk[i]
    if fid == -1:
        i -= 1
        continue
    flen = c.get(fid)
    keys_sorted = sorted(memgap.keys())
    if len(keys_sorted) == 0 or i <= keys_sorted[0]:
        break

    for gap_idx in keys_sorted:
        if gap_idx > i:
            continue
        if memgap[gap_idx] >= flen:
            # moving file
            for x in range(flen):
                disk[gap_idx + x] = fid
                disk[i - x] = - 1
            if memgap[gap_idx] - flen > 0:
                memgap[gap_idx + flen] = memgap[gap_idx] - flen
            memgap.pop(gap_idx)
            break
    i -= flen

sum = 0
k = 0
for k, i in enumerate(disk):
        if disk[k] != -1:
            sum += k * i
print(sum)
