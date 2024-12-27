import re

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

    def eval(self) -> int:
        input_l = WIRES[self.input_l] if self.input_l in WIRES else Gate.GATES[self.input_l].eval()
        input_r = WIRES[self.input_r] if self.input_r in WIRES else Gate.GATES[self.input_r].eval()
        output_val = Gate.LOGIC[self.op](input_l, input_r)
        WIRES[self.out_wire] = output_val
        return output_val


# init WIRE values
i = 0
for i, line in enumerate(lines):
    if line == '': break
    wire = line.split(':')
    WIRES[wire[0]] = int(wire[1])

for j in range(i + 1, len(lines)):
    Gate(lines[j])

binary = ''.join([ str(x) for x in list(map(lambda output: Gate.GATES[output].eval(), sorted(filter(lambda x: x.startswith('z'), Gate.GATES.keys()), reverse=True)))])
print(int(binary, 2))