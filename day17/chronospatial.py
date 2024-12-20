import sys

class Computer:
    def __init__(self, A, B, C, prog):
        self.A = A
        self.B = B
        self.C = C
        self.prog = prog

    def combo(self, value):
        if 0 <= value <= 3:
            return value
        elif value == 4:
            return self.A
        elif value == 5:
            return self.B
        elif value == 6:
            return self.C
        else:
            print(f'error, {value=}')

    def run(self):
        ip = 0
        while ip < len(self.prog):
            if self.prog[ip] == 0:
                num = self.A
                denom = 2**self.combo(self.prog[ip+1])
                self.A = num // denom
                ip += 2
            elif self.prog[ip] == 1:
                self.B ^= self.prog[ip+1]
                ip += 2
            elif self.prog[ip] == 2:
                self.B = self.combo(self.prog[ip+1]) % 8
                ip += 2
            elif self.prog[ip] == 3:
                if self.A != 0:
                    ip = self.prog[ip+1]
                else:
                    ip += 2
            elif self.prog[ip] == 4:
                self.B ^= self.C
                ip += 2
            elif self.prog[ip] == 5:
                yield self.combo(self.prog[ip+1]) % 8
                ip += 2
            elif self.prog[ip] == 6:
                num = self.A
                denom = 2**self.combo(self.prog[ip+1])
                self.B = num // denom
                ip += 2
            elif self.prog[ip] == 7:
                num = self.A
                denom = 2**self.combo(self.prog[ip+1])
                self.C = num // denom
                ip += 2

def main():
    with open(sys.argv[1]) as f:
        for line in f:
            toks = line.rstrip().split(': ')
            if len(toks) == 1:
                continue
            if 'A' in toks[0]:
                reg_a = int(toks[1])
            elif 'B' in toks[0]:
                reg_b = int(toks[1])
            elif 'C' in toks[0]:
                reg_c = int(toks[1])
            else:
                prog = [int(x) for x in toks[1].split(',')]

    computer = Computer(reg_a, reg_b, reg_c, prog)

#    for val in computer.run():
#        print(val)
    output = [str(val) for val in computer.run()]
    print('Part 1:', ",".join(output))
    
main()