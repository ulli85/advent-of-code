f = open("aoc2024-9-1-input.txt", "r")
memory = f.read()

# kazdy sudy cislo je volne misto
free_space = [int(x) for x in memory[1::2]]
files = list(enumerate([int(x) for x in memory[0::2]]))
print(f"files: {files}")
print(f"space: {free_space}")

sparse_mem = ''
while len(files) > 0:
    file = files[0]
    sparse_mem += str(file[0]) * int(file[1])
    files = files[1::]
    if len(free_space) > 0:  # do we have free space ?
        free_blocks = int(free_space[0])
        while free_blocks > 0 and len(files) > 0:
            last_file = files[-1]
            file_id = last_file[0]
            file_blocks = last_file[1]
            free_blocks_to_fill = min(free_blocks, file_blocks)
            sparse_mem += str(file_id) * free_blocks_to_fill
            file_blocks -= free_blocks_to_fill
            free_blocks -= free_blocks_to_fill

            if free_blocks == 0:
                free_space = free_space[1::]  # discard free space
            else:
                free_space[0] = free_blocks  # update free space block count

            if file_blocks == 0:
                files = files[0:len(files) - 1:]  # discard last file
            else:
                last_file = (file_id, file_blocks)  # update file block count
                files[-1] = last_file
print(sparse_mem)
solution = 0
for i in range(len(sparse_mem)):
    solution += i * int(sparse_mem[i])
print(f"solution = {solution}")
print(memory)
print(f"files: {files}")
print(f"space: {free_space}")
