import re


class Pc:
    DEBUG = True
    INS_PTR = 0
    INSTRUCTIONS = [
        lambda o: pc.adv(o), lambda o: pc.bxl(o), lambda o: pc.bst(o), lambda o: pc.jnz(o),
        lambda o: pc.bxc(o), lambda o: pc.out(o), lambda o: pc.bdv(o), lambda o: pc.cdv(o)]
    OUTPUT: [str] = []

    def __init__(self, instr: [int]):
        self.instr = instr
        self.__pr('#-1#', -1)

    def __inc_ptr__(self):
        Pc.INS_PTR += 2
    def __dec_ptr__(self, ins_ptr):
        Pc.INS_PTR -= 2

    def __pr(self, instr_nm: str, op: int):
        if Pc.DEBUG:
            print(f"{instr_nm}({op}), Regs = {REG}, PTR_I: {Pc.INS_PTR}")
            if instr_nm == 'out':
                print(f"{self.instr}")
                print(f"OUT: {Pc.OUTPUT}")

    def __combo__(self, o: int) -> int:
        return REG[0] if o == 4 else REG[1] if o == 5 else REG[2] if o == 6 else o

    def adv(self, o: int):
        self.__inc_ptr__()
        REG[0] = REG[0] // (2 ** self.__combo__(o))
        self.__pr('adv', o)

    def adv_i(self, o:int):
        REG[0] = REG[0] << (self.__combo__(o))

    def bxl(self, o: int):
        REG[1] = REG[1] ^ o  # -> B
        self.__pr('bxl', o)

    def bst(self, o: int):
        REG[1] = self.__combo__(o) % 8  # -> B
        self.__pr('bst', o)

    def jnz(self, o: int):
        if REG[0] == 0:
            self.__pr('jnz-loop', o)
            return
        Pc.INS_PTR = 2 * o
        Pc.LTR_PTR = Pc.INS_PTR + 1
        self.__pr('jnz', o)

    def bxc(self, o: int):
        REG[1] = REG[1] ^ REG[2]
        self.__pr('bxc', o)

    def out(self, o: int):
        self.__inc_ptr__()
        Pc.OUTPUT.append(str(self.__combo__(o) % 8))
        self.__pr('out', o)

    def bdv(self, o: int):
        self.__inc_ptr__()
        REG[1] = REG[0] // (2 ** self.__combo__(o))
        self.__pr('bdv', o)

    def bdv_i(self, o: int):
        REG[1] = REG[0] << (self.__combo__(o))
        self.__pr('bdv', o)

    def cdv(self, o: int):
        REG[2] = REG[0] // (2 ** self.__combo__(o))
        self.__pr('cdv', o)

    def cdv_i(self, o: int):
        REG[2] = REG[0] << (self.__combo__(o))
        self.__pr('cdv', o)

    def execute(self):
        while pc.INS_PTR < len(self.instr):
            instr_idx = self.instr[pc.INS_PTR]
            instr = Pc.INSTRUCTIONS[instr_idx]
            param = self.instr[pc.INS_PTR + 1]
            instr(param)
            # jnz endless loop
            if instr_idx == 3 and REG[0] == 0:
                break
    def execute_inverse(self):
        Pc.INS_PTR = len(self.instr) - 2





r = [int(x) for x in re.findall("-?\\d+", open("input/17-1.txt").read())]
REG = r[0:3]
pc = Pc(r[3:])



pc.execute()
print(','.join(Pc.OUTPUT))
