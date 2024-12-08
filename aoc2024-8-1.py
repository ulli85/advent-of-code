import numpy as np


def in_grid(lines: list[[any]], point: [int]) -> bool:
    if (point[0] < 0 or point[0] >= len(lines)) or (point[1] < 0 or point[1] >= len(lines[0])):
        return False
    return True


f = open("aoc2024-8-1-input.txt", "r")
content = f.read()
grid = content.splitlines()
antennas = {}
antinode_at = np.full((len(grid), len(grid)), False, dtype=bool)
antinodes_cnt = 0
for y in range(len(grid)):
    for x in range(len(grid)):
        char = grid[y][x]
        if char.isalnum():
            # byla uz takova antena nalezena drive?
            if char in antennas:
                for antenna in antennas[char]:
                    r1, c1 = [y, x]  # antena 1
                    r2, c2 = antenna  # antena 2

                    # vypocet potencionalniho umisteni antinodu
                    row_diff, col_diff = r2 - r1, c2 - c1
                    # antinode, kde antena 1 je blize
                    antinode1 = [r1 - row_diff, c1 - col_diff]
                    # antinode, kde antena 2 je blize
                    antinode2 = [r2 + row_diff, c2 + col_diff]

                    if in_grid(grid, antinode1) and not antinode_at[antinode1[0]][antinode1[1]]:
                        antinode_at[antinode1[0]][antinode1[1]] = True
                        antinodes_cnt += 1
                    if in_grid(grid, antinode2) and not antinode_at[antinode2[0]][antinode2[1]]:
                        antinode_at[antinode2[0]][antinode2[1]] = True
                        antinodes_cnt += 1
                # nova antena, pridam mezi ostatni, antinody spocitany
                antennas[char].append([y, x])
            else:  # nova antena prvni sveho druhu
                antennas[char] = [[y, x]]

print(antinodes_cnt)  # funguje na vzorovych prikladech a pro velky input vraci 389, coz pry neni spravna hodnota. Proc?!?!
debug = True # todo lada vyhod celej spodek po vyreseni
if debug:  ## nemam poneti co s tim, chybu nevidim, tak si to alespon hezky vytisknu
    solution_view = np.full((len(grid), len(grid)), '.', dtype=str)
    for key in antennas.keys():
        for antena in antennas[key]:
            solution_view[antena[0]][antena[1]] = key
    for y in range(len(grid)):
        for x in range(len(grid)):
            if antinode_at[y][x]:
                solution_view[y][x] = '~' if str(solution_view[y][
                                                     x]).isalnum() else '#'  # pokud antinode prekryva antenu vytiskni ~, jinak znak anteny
    view_entry_and_solution_side_by_side = []
    for y in range(len(grid)):
        view_entry_and_solution_side_by_side.append(grid[y] + '    ' + ''.join(solution_view[y]))
    print('\n')
    print('\n'.join(view_entry_and_solution_side_by_side))
    print(antennas)
