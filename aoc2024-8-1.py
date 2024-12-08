import numpy as np
from numpy import linalg as la


def in_grid(lines: list[[any]], point: [int]) -> bool:
    if point[0] == -1 or point[0] >= len(lines) or point[1] == -1 or point[1] >= len(lines[0]):
        return False
    return True


f = open("aoc2024-8-1-input.txt", "r")
content = f.read()
lines = content.splitlines()
solution = 0
antennas = {}
processed = {}
view_antennas = np.array(lines)
view = np.full((len(lines), len(lines)), '.', dtype=str)
antinode_at = np.full((len(lines), len(lines)), False, dtype=bool)
antinodes_cnt = 0
debug = True
for y in range(len(lines)):
    for x in range(len(lines)):
        if lines[y][x].isalnum():
            if lines[y][x] in antennas:
                # pokud uz takto pojmenovana antena je, musim ji vyrusit se vsemi jiz znamymi
                for antenna in antennas[lines[y][x]]:
                    a1 = [y, x]
                    a2 = [antenna[0], antenna[1]]
                    # vector (a1 - a2) + A1 souradnice prvniho bodu pro blokovani
                    vect_a1_a2 = [a1[0] - a2[0], a1[1] - a2[1]]
                    antinode_a1 = [a1[0] + vect_a1_a2[0], a1[1] + vect_a1_a2[1]]
                    # vector (a2 - a1) + A2 souradnice druheho bodu pro blokovani
                    vect_a2_a1 = [a2[0] - a1[0], a2[1] - a1[1]]
                    antinode_a2 = [a2[0] + vect_a2_a1[0], a2[1] + vect_a2_a1[1]]
                    if in_grid(lines, antinode_a1) and not antinode_at[antinode_a1[0]][antinode_a1[1]]:
                        antinode_at[antinode_a1[0]][antinode_a1[1]] = True
                        antinodes_cnt += 1
                    if in_grid(lines, antinode_a2) and not antinode_at[antinode_a2[0]][antinode_a2[1]]:
                        antinode_at[antinode_a2[0]][antinode_a2[1]] = True
                        antinodes_cnt += 1
                # pridam novou, jiz vyrusenou s ostatnimi antenami do seznamu
                antennas[lines[y][x]].append([y, x])
            else:  # antena je prvni s danym oznacenim je prvni, zalozim novy seznam
                antennas[lines[y][x]] = [[y, x]]
if debug:
    print('\n'.join(lines))

    for key in antennas.keys():
        for antena in antennas[key]:
            view[antena[0]][antena[1]] = key
    for y in range(len(lines)):
        for x in range(len(lines)):
            if antinode_at[y][x]:
                view[y][x] = '~' if str(view[y][x]).isalnum() else '#'
    view_compact = []
    for y in range(len(lines)):
        view_compact.append(''.join(view[y]))
    print('\n')
    print('\n'.join(view_compact))
print(antinodes_cnt) # funguje na vzorovych prikladech ale ne pro velky input :-(