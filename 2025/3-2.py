banks = open('input/3.txt').read().splitlines()

sum_banks = 0

for joltage in banks:
    max_voltage_str = ['0'] * 12
    index = 0
    for i in range(0, 12):
        voltage_actual = int(max_voltage_str[i])
        voltage_max = 0
        for j in range(index, len(joltage) - (12 - i) + 1):
            voltage = int(joltage[j])
            if voltage > voltage_actual and voltage > voltage_max:
                voltage_max = voltage
                index = j + 1
        max_voltage_str[i] = str(voltage_max)
    max_joltage = int(''.join(max_voltage_str))
    sum_banks += max_joltage
print(sum_banks)