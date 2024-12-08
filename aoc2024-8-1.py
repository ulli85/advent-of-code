import numpy as np


def in_grid(lines: list[[any]], point: [int]) -> bool:
    if point[0] == -1 or point[0] >= len(lines) or point[1] == -1 or point[1] >= len(lines[0]):
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
            if char in antennas:
                # mam uz zalozeny seznam souradnic predchozich anten pro takovy znak?
                for antenna in antennas[char]:  # pro vsechny stavajici anteny umistim antinode
                    a1 = [y, x]
                    a2 = [antenna[0], antenna[1]]
                    # vector (a1 - a2) + A1 spocitam souradnice prvniho bodu pro umisteni antinode
                    vect_a1_a2 = [a1[0] - a2[0], a1[1] - a2[1]]
                    antinode_a1 = [a1[0] + vect_a1_a2[0], a1[1] + vect_a1_a2[1]]
                    # vector (a2 - a1) + A2 souradnice druheho druheho bodu pro umisteni antinode
                    vect_a2_a1 = [a2[0] - a1[0], a2[1] - a1[1]]
                    antinode_a2 = [a2[0] + vect_a2_a1[0], a2[1] + vect_a2_a1[1]]
                    if in_grid(grid, antinode_a1) and not antinode_at[antinode_a1[0]][antinode_a1[1]]:
                        antinode_at[antinode_a1[0]][antinode_a1[1]] = True
                        antinodes_cnt += 1
                    if in_grid(grid, antinode_a2) and not antinode_at[antinode_a2[0]][antinode_a2[1]]:
                        antinode_at[antinode_a2[0]][antinode_a2[1]] = True
                        antinodes_cnt += 1
                # pridam novou, jiz vyrusenou s ostatnimi antenami do seznamu
                antennas[char].append([y, x])
            else:  # tato antena je prvni s timto popiskem, zalozim pro ni novy seznam
                antennas[char] = [[y, x]]

print(antinodes_cnt)  # funguje na vzorovych prikladech ale hodnota pro velky input neni spravna. Proc?!?!
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
