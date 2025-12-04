maze = list(map(list, open('input/4.txt').read().splitlines()))

all_rolls = 0
removed_rolls = -1

while removed_rolls != 0:
    removed_rolls = 0
    for y in range(0, len(maze)):
        for x in range(0, len(maze)):
            if maze[y][x] != '@': continue
            adj_rolls = 0
            for ay, ax in [(y - 1, x), (y - 1, x - 1), (y - 1, x + 1), (y, x - 1),
                           (y, x + 1), (y + 1, x), (y + 1, x - 1), (y + 1, x + 1)]:
                if 0 <= ay < len(maze) and 0 <= ax < len(maze):
                    adj_rolls += 1 if maze[ay][ax] == '@' else 0
            if adj_rolls < 4:
                removed_rolls += 1
                maze[y][x] = '.'
    all_rolls += removed_rolls
print(all_rolls)
