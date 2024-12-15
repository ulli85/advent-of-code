import numpy as np

BOX = 'O'
WALL = '#'
DIRECTIONS = {'>': [0, 1], '^': [-1, 0], 'v': [1, 0], '<': [0, -1]}

def nxt(position: [int], direction: str) -> [int]:
    offset = DIRECTIONS[direction]
    return np.add(position, offset)


def move(position: [int], direction: str) -> bool:
    offset = DIRECTIONS[direction]
    o = map[position[0]][position[1]]
    nxtpos = np.add(position, offset)
    o_nxt = map[nxtpos[0]][nxtpos[1]]
    if o_nxt == WALL: return False
    if o_nxt == BOX and not move(nxtpos, direction): return False
    map[nxtpos[0]][nxtpos[1]] = o
    return True


map = []
instructions = ''
rb_pos = []
for y, line in enumerate(open("input/15-1.txt").read().splitlines()):
    if line == '': continue
    if line[0] == WALL:
        map.append([i for i in line])
        rb_pos_x = line.find('@')
        if rb_pos_x > -1:
            rb_pos = [y, rb_pos_x]
    else:
        instructions += line
#print(f"Robot at:{rb_pos}\n{np.array(map)}\n{instructions}")

for ins in instructions:
    if move(rb_pos, ins):
        map[rb_pos[0]][rb_pos[1]] = '.'
        rb_pos = nxt(rb_pos, ins)
#        print(f"{ins}")
#        print(f"{np.array(map)}")
sum_boxes = 0
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] == BOX: sum_boxes += (100 * y) + x
print(sum_boxes)
