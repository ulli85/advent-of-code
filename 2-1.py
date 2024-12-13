
def is_safe_incremental(row:list, max_errors) -> bool:
    for i in range(1, len(row)):
        if row[i-1] < row[i] and (row[i] - row[i-1]) <= 3:
            continue
        else:
            if max_errors > 0:
                row_new1 = row.copy()
                del row_new1[i]
                row_new2 = row.copy()
                del row_new2[i-1]
                return is_safe_incremental(row_new1, max_errors - 1) or is_safe_incremental(row_new2, max_errors - 1)
            return False
    return True


def is_safe_decremental(row:list, max_errors) -> bool:
    for i in range(1, len(row)):
        if row[i-1] > row[i] and (row[i-1] - row[i]) <= 3:
            continue
        else:
            if max_errors > 0:
                row_new1 = row.copy()
                del row_new1[i]
                row_new2 = row.copy()
                del row_new2[i-1]
                return is_safe_decremental(row_new1, max_errors - 1) or is_safe_decremental(row_new2, max_errors - 1)
            return False
    return True


f = open("2-1-input.txt", "r")
content = f.read()
print(f.read())
lines = content.splitlines()
safeCnt = 0
for line in lines:
    row = [int(x) for x in line.split()]
    if is_safe_incremental(row, 1) or is_safe_decremental(row, 1):
        safeCnt += 1
print(safeCnt)
