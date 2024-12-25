lines = open("input/25-1.txt").read().splitlines()
print(lines)
KEYS = []
LOCKS = []
ROW_SZ = 5
COL_SZ = 7

obj = []
for i, line in enumerate(lines):
    if line != '': obj.append(line)
    elif line == '' or i == len(lines) - 1:
        digits = []
        for i in range(ROW_SZ):
            digit = -1
            for j in range(COL_SZ):
                if obj[j][i] == '#': digit += 1
            digits.append(digit)
        if obj[0][0] == '#':
            LOCKS.append(digits)
        else:
            KEYS.append(digits)
        obj.clear()

# compare keys and locks - they fit if any of all column does not overlap
pairs = 0
for lock in LOCKS:
    for key in KEYS:
        fit = True
        for i in range(ROW_SZ):
            if lock[i] + key[i] >= COL_SZ - 1:
                fit = False
                break
        if fit: pairs += 1
        print(f'Lock {",".join([str(x) for x in lock])} and key {",".join([str(x) for x in key])} {"fit" if fit else "overlap"}')
print(pairs)
