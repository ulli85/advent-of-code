f = open("aoc2024-1-1-input.txt", "r")
content = f.read()
print(f.read())
lines = content.splitlines()
lst1 = []
lst2 = []
for line in lines:
    lnArray = line.split()
    lst1.append(int(lnArray[0]))
    lst2.append(int(lnArray[1]))
print(lst1)
print(lst2)
lst1.sort()
lst2.sort()
print('---------')
print(lst1)
print(lst2)
suma = 0
for i in range(len(lines)):
    suma += abs(lst2[i] - lst1[i])
print(suma)
