lines = open('input/1-1.txt').read().splitlines()
print(lines)

v = 50
sum_zeros = 0
for line in lines:
    sign = 1 if line[0] == 'R' else -1
    offset = int(line[1:])
    v = (v + (sign * offset)) % 100
    sum_zeros += 1 if v == 0 else 0
print(sum_zeros)
