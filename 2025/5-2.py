data = open('input/5.txt').read().splitlines()
ranges = list(map(lambda x: list(map(int, x.split('-'))), data[0: data.index('')]))

interchange = True
arr = ranges[:]
arr = sorted(arr, key=lambda x: x[0])
while interchange:
    interchange = False
    for i in range(0, len(arr) - 1):
        if arr[i][1] >= arr[i + 1][0]:
            new_range = [arr[i][0], max(arr[i][1], arr[i + 1][1])]
            arr = arr[0:i] + [new_range] + arr[i + 2:]
            interchange = True
            break

result = sum(map(lambda x: x[1] - x[0] + 1, arr))
print(result)
