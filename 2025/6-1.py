import numpy as np

data = map(lambda x: x.split(' '), open('input/6.txt').read().splitlines())
d2 = []
for row in data:
    d2 += [list(filter(lambda x: x != '', row))]

data = np.transpose(d2, axes=None)
suma = 0
for col in data:
    op = str(col[-1])
    suma += eval(op.join(col[0:len(col) -1]))
print(suma)