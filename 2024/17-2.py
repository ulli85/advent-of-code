import re


def execute(prog_part: [int], answer: int = 0) -> int:
    if len(prog_part) == 0:
        return answer
    for i in range(8):
        A = (answer << 3) + i # value '3' based on running first part as a parameter of adv combo
        B = 0
        C = 0
        a_next = A

        def combo(o: int) -> int:
            if o == 4:
                return A
            elif o == 5:
                return B
            elif o == 6:
                return C
            return o

        for ptr in range(0, len(program) - 2, 2):
            ins = program[ptr]
            param = program[ptr + 1]
            if ins == 0:
                A = A >> combo(param)
            elif ins == 1:
                B = B ^ param
            elif ins == 2:
                B = combo(param) % 8
            elif ins == 3:
                raise ValueError('JNZ instruction inside program body')
            elif ins == 4:
                B = B ^ C
            elif ins == 5:
                output = combo(param) % 8
                if output == prog_part[-1]:
                    sol = execute(prog_part[:-1], a_next)
                    if sol is None: continue
                    return sol
            elif ins == 6:
                B = A >> combo(param)
            elif ins == 7:
                C = A >> combo(param)
            else:
                raise Exception(f'Unknown instruction {ins}.')


program = [int(x) for x in re.findall("-?\\d+", open("input/17-1.txt").read())[3:]]
print(execute(program))
