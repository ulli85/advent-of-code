banks = open('input/3.txt').read().splitlines()
print(banks)
sum_banks = 0

for joltage in banks:
    max_voltage = 0
    for i in range(0, len(joltage) - 1):
        for j in range(i + 1, len(joltage)):
            v = int(joltage[i] + joltage[j])
            max_voltage = max(max_voltage, v)
    sum_banks += max_voltage
print(sum_banks)

