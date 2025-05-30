lines = open('input/9').read().splitlines()
total_sum = 0
for line in lines:
    numbers = [list(map(int, line.split()))]
    final = False
    while not final:
        final = True
        diffs = []
        actual = numbers[-1]
        for i in range(1, len(actual)):
            difference = actual[i - 1] - actual[i]
            diffs += [difference]
            if difference != 0: final = False
        numbers += [diffs]
    next_num = 0
    for number_row in numbers[::-1]:
        next_num += number_row[0]
    total_sum += next_num
print(total_sum)