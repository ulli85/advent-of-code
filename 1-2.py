f = open("1-2-input.txt", "r")
content = f.read()
print(f.read())
lines = content.splitlines()
lst1 = []
lst2 = []
for line in lines:
    lnArray = line.split()
    lst1.append(int(lnArray[0]))
    lst2.append(int(lnArray[1]))
lst1.sort()
lst2.sort()
suma = 0
pom = 0
for left in lst1:
    multiplicator = 0
    for j in range(len(lines)):
        if left < lst2[j]:
            suma += abs(left * multiplicator)
            print(str(left) + '*' + str(multiplicator))
            break
        if left == lst2[j]:
            multiplicator += 1
        else:
            continue
print(suma)
