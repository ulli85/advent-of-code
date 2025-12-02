sequences = open('input/2.txt').read().replace('\n', '').split(',')
suma = 0
for seq in sequences:
    mm, mm2 = map(int, seq.split('-'))
    for i in range(mm, mm2 + 1):
        nms = str(i)
        lh = len(nms) // 2
        if nms[0:lh + len(nms) % 2] == nms[lh + len(nms) % 2:]:
            suma += i
print(suma)
