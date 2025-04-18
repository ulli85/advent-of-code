import math
import re

data = open("input/4").read().splitlines()
matches = map(lambda x: re.fullmatch('^Card\\s+\\d+:\\s+(?P<winning_nums>.*)\\|\\s+(?P<mine_nums>.*)$', x), data)
suma = 0
for match in matches:
    matched_numbers = {*match.group('winning_nums').split()}.intersection({*match.group('mine_nums').split()})
    suma += int(math.pow(2, len(matched_numbers) - 1))
print(suma)