def prepare_grid_pos_agent(lines: list) -> tuple:
    agent_pos = []
    grid = []
    for i in range(len(lines)):
        grid.append([char for char in lines[i]]) # ze stringu udelam pole charu
        for j in (range(len(lines[0]))):
            if lines[i][j] in directions:
                agent_pos = [i, j]
    return agent_pos, grid

def outside_grid(lines: list, next_y: int, next_x) -> bool:
    if next_y == -1 or next_y == len(lines) or next_x == -1 or next_x == len(lines[0]):
        return True
    return False

f = open("aoc2024-6-2-input.txt", "r")
content = f.read()
lines = content.splitlines()
directions = {'>': [0, 1], '^': [-1, 0], 'v': [1, 0], '<': [0, -1]}
rotations = {'>': 'v', '^': '>', 'v': '<', '<': '^'}
preparation = prepare_grid_pos_agent(lines)
grid = preparation[1]
first_direction = grid[preparation[0][0]][preparation[0][1]]
solution_cnt = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == '.':
            grid[y][x] = 'O'
            actual_pos = preparation[0]
            path = {}
            grid[actual_pos[0]][actual_pos[1]] = first_direction
            start_pos = actual_pos
            visited_cnt = 1
            while True:
                direction = grid[actual_pos[0]][actual_pos[1]]
                next_y = actual_pos[0] + directions[direction][0]
                next_x = actual_pos[1] + directions[direction][1]
                if outside_grid(grid, next_y, next_x):
                    grid[actual_pos[0]][actual_pos[1]] = '.'
                    break

                # pokud naleznu opakujici se bod cesty ve stejnem smeru, pak jsem v cyklu a mohu ukoncit algoritmus
                unique = f"{next_y}-{next_x}-{direction}"
                if unique in path:
                    grid[actual_pos[0]][actual_pos[1]] = '.'
                    solution_cnt += 1
                    break
                else:
                    path[unique] = ''
                next_object = grid[next_y][next_x]
                if next_object == '.':
                    grid[next_y][next_x] = direction
                    grid[actual_pos[0]][actual_pos[1]] = '.'
                    actual_pos = [next_y, next_x]
                    if next_object == '.':
                        visited_cnt += 1
                elif next_object == '#' or next_object == 'O':
                    grid[actual_pos[0]][actual_pos[1]] = rotations[direction]
            if grid[y][x] == 'O':
                grid[y][x] = '.'
print(solution_cnt)