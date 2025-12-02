from collections import Counter

sequences = open('input/2.txt').read().replace('\n', '').split(',')

def check_repetition(digit_count:int, number:str)->int:
    totalln = len(number)
    times = totalln // digit_count
    if times * digit_count < totalln:
        return 0
    arr = number.split(number[0:digit_count])
    for item in arr:
        if len(item) > 0:
            return 0
    return int(number)


suma = 0
for seq in sequences:
    mm, mm2 = map(int, seq.split('-'))
    for i in range(mm, mm2 + 1):
        nms = str(i)
        counter = Counter(nms)
        if len(nms) > 1 and len(counter.keys()) == 1:
            suma += i
            continue
        lh = len(nms) // 2
        for j in range(1, (lh + len(nms) % 2) + 1):
            rpr = check_repetition(j, nms)
            if rpr > 0:
                if rpr >= 11:
                    suma += rpr
                break
print(suma)
