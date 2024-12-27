import numpy as np

WALL = '#'
DIRECTIONS = {'>': [0, 1], '<': [0, -1], 'v': [1, 0], '^': [-1, 0]}


def transformed_line(row: int, line) -> [str]:
    new_line = []
    for x, tile in enumerate(line):
        if tile == WALL:
            new_line.append(WALL)
            new_line.append(WALL)
        elif tile == 'O':
            new_line.append('[')
            new_line.append(']')
            bl = Block((row, 2 * x), (row, 2 * x + 1))
            Block.BLOCKS[bl.l_pos] = bl
            Block.BLOCKS[bl.r_pos] = bl
        elif tile == '.':
            new_line.append('.')
            new_line.append('.')
        else:
            new_line.append('@')
            new_line.append('.')
    return new_line


class Block:
    BLOCKS = {}

    def __init__(self, l_pos: tuple([int]), r_pos: tuple([int])):
        self.l_pos = l_pos
        self.r_pos = r_pos
        Block.BLOCKS[l_pos] = Block.BLOCKS[r_pos] = self

    def __hash__(self):
        return 1000 * hash(self.l_pos) + hash(self.r_pos)
    def __str__(self):
        return f'L:{self.l_pos}, R:{self.r_pos}'

    def move(self, direction: str, just_check: bool = False):
        l_new = tuple(np.add(self.l_pos, DIRECTIONS[direction]))
        r_new = tuple(np.add(self.r_pos, DIRECTIONS[direction]))
        nxtpos = []
        if tuple(l_new) != self.r_pos: nxtpos.append(l_new)
        if tuple(r_new) != self.l_pos: nxtpos.append(r_new)
        blocks2mv: [Block] = set() # need to be set othervise same block could be inserted twice
        move_possible = True
        for new_pos in nxtpos:
            if not move_possible: break
            if WALL == MAP[new_pos[0]][new_pos[1]]: move_possible = False  # at the wall
            elif '.' == MAP[new_pos[0]][new_pos[1]]: # free space
                continue
            else:  # must be a block
                adj_blk = Block.BLOCKS[tuple(new_pos)]
                if adj_blk.move(direction, True):
                    blocks2mv.add(adj_blk)  # can move only if other block can too
                else:
                    move_possible = False
        if just_check or not move_possible: return move_possible  # just check that block move is possible or move is not possible
        # physically move the blocks - (set up the MAP)
        for blck2mv in blocks2mv:
            blck2mv.move(direction)
        # adjust coords and update BLOCKS
        Block.BLOCKS.pop(self.l_pos)
        Block.BLOCKS.pop(self.r_pos)
        Block.BLOCKS[l_new] = self
        Block.BLOCKS[r_new] = self
        # update map positions before move
        MAP[self.l_pos[0]][self.l_pos[1]] = '.'
        MAP[self.r_pos[0]][self.r_pos[1]] = '.'
        self.l_pos = l_new
        self.r_pos = r_new
        # update map positions after move
        MAP[self.l_pos[0]][self.l_pos[1]] = '['
        MAP[self.r_pos[0]][self.r_pos[1]] = ']'
        return move_possible


MAP = []
INSTRUCTIONS = ''
RB_POS = []

for row, line in enumerate(open("input/15-1.txt").read().splitlines()):
    if line == '': continue
    if line[0] == WALL:
        new_line = transformed_line(row, line)
        MAP.append(new_line)
        rb_pos_x = ''.join(new_line).find('@')
        if rb_pos_x > -1:
            RB_POS = [row, rb_pos_x]
    else:
        INSTRUCTIONS += line
# print(f"Robot at:{rb_pos}\n{np.array(map)}\n{instructions}")
for line in MAP:
    print(''.join(line))

for direction in INSTRUCTIONS:
    nxt_pos = np.add(RB_POS, DIRECTIONS[direction])
    nxt_pos = (nxt_pos[0], nxt_pos[1])
    tile = MAP[nxt_pos[0]][nxt_pos[1]]
    if WALL == tile: continue
    if '.' == tile:
        MAP[nxt_pos[0]][nxt_pos[1]] = '@'
        MAP[RB_POS[0]][RB_POS[1]] = '.'
        RB_POS = nxt_pos
    else:
        block = Block.BLOCKS[nxt_pos]
        if block.move(direction, True):
            block.move(direction)
            MAP[nxt_pos[0]][nxt_pos[1]] = '@'
            MAP[RB_POS[0]][RB_POS[1]] = '.'
            RB_POS = nxt_pos
    print(direction)
    for line in MAP:
        print(''.join(line))

sum_boxes = 0
for block in Block.BLOCKS.values():
    sum_boxes += 100 * block.l_pos[0] + block.l_pos[1]
print(sum_boxes // 2)
