import re

import pulp

lines = open('input/10.txt').read().splitlines()
all_clicks = 0
for i, line in enumerate(lines):
    B_eq = re.findall('\\{\\d[,\\d]*\\}', line)[0][1:-1].split(',')
    B_eq = list(map(int, B_eq))
    A_eq = []
    for operands in re.findall('\\(\\d[,\\d]*\\)', line):
        btn_behaviour = map(int, operands[1:-1].split(','))
        coeficients = [0] * len(B_eq)
        for idx in btn_behaviour:
            coeficients[idx] = 1
        A_eq += [coeficients]

    A_eq = list(zip(*A_eq))
    problem = pulp.LpProblem("AOC_10_2", pulp.LpMinimize)
    variables = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(len(A_eq[0]))]

    for r in range(len(A_eq)):
        _sum = []
        for c in range(len(A_eq[0])):
            if A_eq[r][c] != 0:
                _sum += variables[c]
        constraint = pulp.lpSum(_sum)
        problem += constraint == B_eq[r], f"Row_{r}"
    problem.solve()

    assert pulp.LpStatus[problem.status] == 'Optimal'
    s = list(int(pulp.value(var)) for var in variables)
    #print(s)
    all_clicks += sum(s)
print(all_clicks)
