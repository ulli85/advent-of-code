maze = open('input/4.txt').read().splitlines()

all_rolls = 0
for y in range(0, len(maze)):
    for x in range(0, len(maze)):
        if maze[y][x] != '@': continue
        adj_pap = 0
        for ay, ax in [(y - 1, x), (y - 1, x - 1), (y - 1, x + 1), (y, x - 1),
                       (y, x + 1), (y + 1, x), (y + 1, x - 1), (y + 1, x + 1)]:
            if 0 <= ay < len(maze) and 0 <= ax < len(maze):
                adj_pap += 1 if maze[ay][ax] == '@' else 0
        if adj_pap < 4:
            all_rolls += 1
print(all_rolls)
