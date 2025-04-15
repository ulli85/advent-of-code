import re
from functools import reduce

print(sum([reduce(lambda x, y: x * y, row) for row in list(map(lambda r: [
    max([int(x) for x in re.findall('(\\d+) red', r)]),
    max([int(x) for x in re.findall('(\\d+) blue', r)]),
    max([int(x) for x in re.findall('(\\d+) green', r)])], open("input/2").read().splitlines()))]))
