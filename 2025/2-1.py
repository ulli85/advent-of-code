lines = open('input/1-1.txt').read().splitlines()

v = 50
sum_zeros = 0
for line in lines:
    sign = 1 if line[0] == 'R' else -1
    offset = int(line[1:])
    hundred_times = offset // 100
    offset -= hundred_times * 100
    sum_zeros += hundred_times
    if v != 0:
        if sign == -1 and offset >= v or sign == 1 and v + offset >= 100:
            sum_zeros += 1
    v = (v + (sign * offset)) % 100
print(sum_zeros)
