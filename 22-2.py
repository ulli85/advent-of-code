from collections import deque

input = [int(x) for x in open("input/22-1.txt").read().splitlines()]


def evolve(sn: int) -> int:
    sn = ((sn << 6) ^ sn) % 16777216
    sn = ((sn >> 5) ^ sn) % 16777216
    sn = ((sn << 11) ^ sn) % 16777216
    return sn


sequence_map = {}
sequence_arr = deque()
max_bananas_cnt = 0
sum_of_secrets = 0
for snid, sn in enumerate(input):
    last_digit_before = sn % 10
    unique = set()
    k = 0
    for i in range(0, 2000):
        sn = evolve(sn)
        if sn not in unique:
            unique.add(sn)
            # sum_of_secrets += secret_n
            last_digit = sn % 10
            bananas_change = last_digit - last_digit_before
            last_digit_before = last_digit
            sequence_arr.append(bananas_change)
            sequence = ''.join(map(str, sequence_arr))
            # print(f'{sn}: {last_digit} ({bananas_change}) Seq: {sequence}')
            if len(sequence_arr) > 3:
                sequence_arr.popleft()
                if sequence in sequence_map:
                    snid_prev, bananas_cnt_prev = sequence_map[sequence]
                    if snid_prev != snid:
                        new_bananas_cnt = bananas_cnt_prev + last_digit
                        sequence_map[sequence] = (snid, new_bananas_cnt)
                        if max_bananas_cnt < new_bananas_cnt:
                            max_bananas_cnt = new_bananas_cnt
                else:
                    sequence_map[sequence] = (snid, last_digit)
                    if max_bananas_cnt < last_digit:
                        max_bananas_cnt = last_digit

# for i in sequence_map.items():
#    print(f'{i[1]}x {i[0]}')
# print(sum_of_secrets)
print(max_bananas_cnt)
