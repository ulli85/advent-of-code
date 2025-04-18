"""

INPUTS
     x o-------------o--------｜‾‾‾｜
                     ｜       ｜XOR｜>--------------------o--------------------｜‾‾‾｜
     y o---------o---｜-------｜___｜                     ｜                   ｜XOR｜--------o Z_xy
                 ｜  ｜                    ｜‾‾‾‾‾‾‾‾‾‾‾‾‾｜‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾｜___｜
                 ｜  ｜                    ｜             ｜
       o‾‾‾‾‾‾‾‾‾｜‾‾｜‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾｜             ｜
     carry_in    ｜  ｜                    ｜              ‾‾｜‾‾‾｜
                 ｜  ｜                     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾｜AND｜‾‾‾‾‾‾‾‾‾‾‾‾｜‾‾｜
                 ｜  ｜‾‾‾‾‾‾‾‾｜‾‾‾｜                        ｜___｜            ｜OR｜--------o carry_out
                  ‾‾‾‾‾‾‾‾‾‾‾‾｜AND｜‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾｜___｜
                              ｜___｜
                                                                                            OUTPUTS
"""

# formulas = [str(x) for x in list(filter(lambda x: x.find('->') >= 0, open("input/24-1").read().splitlines()))]
# swap = []
# all_outputs = list(filter(lambda f: f.find('-> z') > 0, formulas))
# wrong_outputs = list(filter(lambda o: o.find('XOR') == -1, all_outputs))
# print(wrong_outputs)  # should be xor, but it is


import re
import typing

lines = [str(x) for x in open("input/24-1.txt").read().splitlines()]
WIRES = {}


class Gate:
    GATES = {}
    LOGIC = {
        'AND': lambda lval, rval: lval & rval,
        'OR': lambda lval, rval: lval | rval,
        'XOR': lambda lval, rval: lval ^ rval}

    def __init__(self, line: str):
        res = re.findall('(\\w+) (AND|OR|XOR) (\\w+) -> (\\w+)', line)
        self.input_l = res[0][0]
        self.op = res[0][1]
        self.input_r = res[0][2]
        self.out_wire = res[0][3]
        Gate.GATES[self.out_wire] = self

    def __str__(self):
        return f'{self.input_l} {self.op} {self.input_r}'

    def eval(self) -> int:
        input_l = WIRES[self.input_l] if self.input_l in WIRES else Gate.GATES[self.input_l].eval()
        input_r = WIRES[self.input_r] if self.input_r in WIRES else Gate.GATES[self.input_r].eval()
        output_val = Gate.LOGIC[self.op](input_l, input_r)
        WIRES[self.out_wire] = output_val
        return output_val


class Gate:
    GATES = {}
    FORMULAS = {}
    LOGIC = {
        'AND': lambda lval, rval: lval & rval,
        'OR': lambda lval, rval: lval | rval,
        'XOR': lambda lval, rval: lval ^ rval}

    def __init__(self, line: str):
        res = re.findall('(\\w+) (AND|OR|XOR) (\\w+) -> (\\w+)', line)
        self.input_l = res[0][0]
        self.op = res[0][1]
        self.input_r = res[0][2]
        self.out_wire = res[0][3]
        Gate.GATES[self.out_wire] = self
        Gate.FORMULAS[f'{self.input_l} {self.op} {self.input_r}'] = self.out_wire

    def eval(self) -> int:
        input_l = WIRES[self.input_l] if self.input_l in WIRES else Gate.GATES[self.input_l].eval()
        input_r = WIRES[self.input_r] if self.input_r in WIRES else Gate.GATES[self.input_r].eval()
        output_val = Gate.LOGIC[self.op](input_l, input_r)
        WIRES[self.out_wire] = output_val
        return output_val


class TreeNode:

    def __init__(self, gate: Gate, parent: typing.Optional['TreeNode'] = None):
        self.gate = gate
        self.parent = parent
        self.child_left = None
        self.child_right = None
        if not (gate.input_l.startswith('x') or gate.input_l.startswith('y')):
            self.child_left = TreeNode(Gate.GATES[gate.input_l], self)
            CircuitTree.traversal += f'LEFT: {gate.input_l} {gate.op} {gate.input_r} -> {gate.out_wire}\n'
        else:
            CircuitTree.traversal += f'{gate.input_l} {gate.op} '

        if not (gate.input_r.startswith('x') or gate.input_r.startswith('y')):
            self.child_right = TreeNode(Gate.GATES[gate.input_r], self)
            CircuitTree.traversal += f'RIGHT: {gate.input_l} {gate.op} {gate.input_r} -> {gate.out_wire}\n'
        else:
            CircuitTree.traversal += f'{gate.input_r} -> {gate.out_wire} \n'

    def __str__(self):
        return str(self.gate)


class CircuitTree:
    traversal = ''

    def __init__(self, output: str):
        self.output = output
        self.oidx = int(self.output[1:])
        self.root = TreeNode(Gate.GATES[output])
        self.out = []

    def xn_1_and_yn_1(self):
        idx = f'{self.oidx - 1:02}'
        #if self.traversal.find(f'x{idx} AND y{idx}')


    def check_carry_in(self) -> bool:
        idx = f'{self.oidx - 1:02}'
        return self.traversal.find(f'x{idx} AND y{idx}') >= 0 or self.traversal.find(f'y{idx} AND x{idx}') >= 0

    def check_xn_2_and_yn_2(self):
        idx = f'{self.oidx - 2:02}'


    # init WIRE values
    def check_output_bit(self) -> bool:
        idx = f'{self.oidx:02}'
        return self.traversal.find(f'x{idx} XOR y{idx}') >= 0 or self.traversal.find(f'y{idx} XOR x{idx}') >= 0





    def check_carry_out(self):
        pass


i = 0

for i, line in enumerate(lines):
    if line == '': break
    wire = line.split(':')
    WIRES[wire[0]] = int(wire[1])

for j in range(i + 1, len(lines)):
    Gate(lines[j])

for x, y in [[0, 0], [0, 1], [1, 0], [1, 1]]:
    pass

for i in range(3, 4):
    output = f'z{i:02}'
    tree = CircuitTree(output)
    print(CircuitTree.traversal)

    error = False
    if not tree.check_carry_in():
        print(f'Carry check fail for {output}')
        error = True
    if not tree.check_output_bit():
        print(f'Output bit check fail for {output}')
        error = True

    if error:
        print(CircuitTree.traversal)
        print('-------------------')

binary = ''.join([str(x) for x in list(map(lambda output: Gate.GATES[output].eval(),
                                           sorted(filter(lambda x: x.startswith('z'), Gate.GATES.keys()),
                                                  reverse=True)))])

print(binary)
print(int(binary, 2))
