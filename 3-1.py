import re

f = open("input/3-1.txt", "r")
content = f.read()
res = re.findall("mul\\(\\d{1,3},\\d{1,3}\\)|don\'t\\(\\)|do\\(\\)", content)
suma = 0
sum_enabled = True
for operation in res:
    if operation.startswith("mul") and sum_enabled:
        numbers = [int(x) for x in operation[4:len(operation) - 1].split(',')]
        suma += numbers[0] * numbers[1]
    if operation == 'do()':
        sum_enabled = True
    if operation == 'don\'t()':
        sum_enabled = False
print(suma)
