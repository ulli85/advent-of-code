import re
cubes={'red':12, 'green':13, 'blue':14}
game_ids_sum = 0
for row in open("input/2").read().splitlines():
    game_id = int(re.findall('Game \\d+', row)[0].split()[1])
    is_valid = True
    for game in row.split(';'):
        if not is_valid: break
        col2val = dict(zip(re.findall('[a-z]+', game), [int(x) for x in re.findall('\\d+', game)]))
        for color in cubes.keys():
            if color in col2val and cubes[color] < col2val[color]:
                is_valid = False
                break
    if is_valid:
        game_ids_sum += game_id
print(game_ids_sum)