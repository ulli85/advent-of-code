import re
print(sum(list(map(lambda numbers: int(numbers[0] + numbers[-1]), map(lambda line: re.findall('\\d', line), open("input/1-1.txt", "r").read().splitlines())))))
