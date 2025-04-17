import math
import re

data = map(lambda x: re.fullmatch('^Card\\s+\\d+:\\s+(?P<winning_numbers>.*)\\|\\s+(?P<mine_numbers>.*)$', x), open("input/4").read().splitlines())
suma = 0
for game in data:
    matched_numbers = {*game.group('winning_numbers').split()}.intersection({*game.group('mine_numbers').split()})
    suma += int(math.pow(2, len(matched_numbers) - 1))
print(suma)