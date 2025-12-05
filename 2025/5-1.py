data = open('input/5.txt').read().splitlines()
ranges = list(map(lambda x: list(map(int, x.split('-'))), data[0: data.index('')]))
ids = list(map(int, data[data.index('') + 1:]))
rotten = 0
for iid in ids:
    for r in ranges:
        if r[0] <= iid <= r[1]:
            rotten += 1
            break
print(rotten)
