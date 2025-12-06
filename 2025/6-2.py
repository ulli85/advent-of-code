import re

data = open('input/6.txt').read().splitlines()
numbers = []

for row in data[0:len(data) - 1]:
    numbers += [re.findall('\\d+', row)]

paddings = []
for c in range(len(numbers[0])):
    pad = 0
    for r in range(len(numbers)):
        pad = max(pad, len(numbers[r][c]))
    paddings += [pad]

dp = []
for row in data[0:len(data) - 1]:
    padded_row = []
    pos = 0
    for padding in paddings:
        padded_row += [row[pos: pos + padding].rjust(padding, ' ')]
        pos = pos + padding + 1
    dp += [padded_row]

formulas = []
pos = 0
for c in range(pos, len(dp[0])):
    operands = []
    for p in range(0, paddings[c]):
        digits = ''
        for r in range(0, len(numbers)):
            value = dp[r][c][p]
            if value != ' ':
                digits += value
        operands += [digits]
    formulas += [operands]

suma = 0
operations = data[-1].replace(' ', '')[:]
for i, operands in enumerate(formulas):
    op = operations[i]
    operands = filter(lambda x: x != '', operands)
    res = eval(op.join(operands))
    suma += res
print(suma)
