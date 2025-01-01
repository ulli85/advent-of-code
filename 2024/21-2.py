from collections import deque
from functools import cache
from itertools import product

## source
## https://www.youtube.com/watch?v=dqzAaj589cM

numeric_keypad = (('7', '8', '9'),
                  ('4', '5', '6'),
                  ('1', '2', '3'),
                  (None, '0', 'A'))

directional_keypad = ((None, '^', 'A'),
                      ('<', 'v', '>'))


def compute_seqs(keypad) -> set[tuple[str, str]: 'str']:
    pos = {}
    for r in range(len(keypad)):
        for c in range(len(keypad[r])):
            if keypad[r][c] is not None:
                pos[keypad[r][c]] = (r, c)
    seqs = {}
    for x in pos:
        for y in pos:
            if x == y:
                seqs[(x, y)] = ['A']
                continue
            possibilities = []
            q = deque([(pos[x], '')])
            optimal = float('inf')
            while q:
                (r, c), moves = q.popleft()
                for nr, nc, nm in [(r - 1, c, '^'), (r, c + 1, '>'), (r + 1, c, 'v'), (r, c - 1, '<')]:
                    if nr < 0 or nc < 0 or nr >= len(keypad) or nc >= len(keypad[0]): continue
                    if keypad[nr][nc] is None: continue
                    if keypad[nr][nc] == y:
                        if optimal < len(moves) + 1: break
                        optimal = len(moves) + 1
                        possibilities.append(moves + nm + 'A')
                    else:
                        q.append(((nr, nc), moves + nm))
                else:
                    continue
                break
            seqs[(x, y)] = possibilities
    return seqs


def solve(string, seqs):
    options = [seqs[(x, y)] for x, y in zip('A' + string, string)]
    return [''.join(x) for x in product(*options)]

@cache
def compute_length(x, y, depth=25):
    if depth == 1:
        return dir_lengths[(x, y)]
    optimal = float('inf')
    for seq in dir_seqs[(x, y)]:
        length = 0
        for a, b in zip('A' + seq, seq):
            length += compute_length(a, b, depth - 1)
        optimal = min(optimal, length)
    return optimal

def compute_length(seq, depth=25):

    if depth == 1:
        return dir_lengths[(x, y)]
    optimal = float('inf')
    for seq in dir_seqs[(x, y)]:
        length = 0
        for a, b in zip('A' + seq, seq):
            length += compute_length(a, b, depth - 1)
        optimal = min(optimal, length)
    return optimal


num_seqs = compute_seqs(numeric_keypad)
dir_seqs = compute_seqs(directional_keypad)
dir_lengths = {key: len(value[0]) for key, value in dir_seqs.items()}

total = 0

for line in open("input/21-1.txt").read().splitlines():
    inputs = solve(line, num_seqs)
    optimal = float('inf')
    for seq in inputs:
        length = 0
        for x, y in zip('A' + seq, seq):
            length += compute_length(x, y)
        print(length)
        optimal = min(optimal, length)
    total += optimal * int(line[:-1])
print(total)

