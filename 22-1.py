input = [int(x) for x in open("input/22-1.txt").read().splitlines()]
print(input)
def evolve(sn: int) -> int:
    sn = ((sn << 6) ^ sn) % 16777216 # (multiply secret by 64) XOR secret number
    sn = ((sn >> 5) ^ sn) % 16777216
    sn = ((sn << 11) ^ sn) % 16777216
    return sn


sum_of_secrets = 0
for secret_n in input:
    unique = set()
    for i in range(0, 2000):
        secret_n = evolve(secret_n)
    if secret_n not in unique:
        unique.add(secret_n)
        sum_of_secrets += secret_n
print(sum_of_secrets)

