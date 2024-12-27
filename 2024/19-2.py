input = open("input/19-1.txt").read().splitlines()
PATTERNS = set(input[0].split(', '))
PATTERN_MAX_LEN = max(map(len, PATTERNS))
DESIGNS = input[2::]
CACHE = {}


def combination_cnt(design: str) -> int:
    if len(design) == 0:
        return 1

    if design in CACHE: return CACHE[design]
    combinations = 0

    for i in range(1, min(PATTERN_MAX_LEN, len(design)) + 1):
        if design[0:i] in PATTERNS:
            combinations += combination_cnt(design[i:])
    CACHE[design] = combinations
    return combinations

print(sum(combination_cnt(x) for x in DESIGNS))
