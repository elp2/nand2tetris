from sys import argv

A0COMP = ["0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-1", "A-1", "D+A", "D-A", "A-D", "D&A", "D|A"]
A1COMP = [None, None, None, None, "M", None, "!M", None, "-M", None, "M+1", None, "M-1", "D+M", "D-M", "M-D", "D&M", "D|M"]
COMPS = ["101010", "111111", "111010", "001100", "110000", "001101", "110001", "001111", "110011", "011111", "110111", "001110", "110010", "000010", "010011", "000111", "000000", "010101"]

assert len(A1COMP) == len(A0COMP)
assert len(A1COMP) == len(COMPS)

JMP_TABLE = {
    "": "000",
    "JGT": "001", # if comp > 0 jump
    "JEQ": "010", # if comp = 0 jump
    "JGE": "011", # if comp ≥ 0 jump
    "JLT": "100", # if comp < 0 jump
    "JNE": "101", # if comp ≠ 0 jump
    "JLE": "110", # if comp ≤ 0 jump
    "JMP": "111", # Unconditional jump
}

DEST_TABLE = {
    "0":     "000",
    "M":    "001",
    "D":    "010",
    "DM":   "011",
    "MD":   "011",
    "A":    "100",
    "AM":   "101",
    "AD":   "110",
    "ADM":  "111",
}

class Assembler:
    def __init__(self):
        self.symbol_dict = {
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
        }
        for r in range(16):
            self.symbol_dict["R" + str(r)] = r
        self.next_symbol_pos = 16

    def create_reference(self, name, val=None):
        assert name not in self.symbol_dict
        if val == None:
            val = self.next_symbol_pos
            self.next_symbol_pos += 1
        
        self.symbol_dict[name] = val
        # TODO if not have reference, add a placeholder to array, then come back at end and put in


    def get_reference(self, name, create=True):
        if name not in self.symbol_dict:
            if not create:
                return None
            self.create_reference(name)
        
        return self.symbol_dict[name]


    def a_instruction(self, line):
        assert line[0] == "@"
        astr = line[1:]
        if astr[0] in "0123456789":
            a = int(astr)
        else:
            a = self.get_reference(astr, create=True)
        
        assert a >= 0
        assert a < pow(2, 15)

        ret = bin(a)[2:]
        while len(ret) < 16:
            ret = "0" + ret
        return ret


    def c_instruction(self, line):
        assert line[0] != "@"

        if ";" not in line:
            line = line + ";"
        deq, jmp = line.split(";")
        if "=" not in deq:
            d, eq = "0", deq
        else:
            d, eq = deq.split("=")
            
        # 1 1 1 a c c c c c c d d d j j j
        ret = "111"
        if eq in A1COMP:
            comp = COMPS[A1COMP.index(eq)]
            a = "1"
        elif eq in A0COMP:
            a = "0"
            comp = COMPS[A0COMP.index(eq)]
        else:
            print("Unknown eq clause:[", eq, "]", deq)
            assert False
        ret += a + comp
        ret += DEST_TABLE[d]
        ret += JMP_TABLE[jmp]

        return ret

    def parse_label(self, line, pc):
        assert line[0] == "("
        assert line[-1] == ")"
        label = line[1:-1]
        self.create_reference(label, pc)

    
    def assemble_file(self, name):
        lines = open(name).readlines()

        asm = []
        pc = 0
        for line in lines:
            line = line.strip()
            if not len(line):
                continue
            if line[0] == "@":
                asm.append(line) # Do in second pass.
                pc += 1
            elif line[0] == "(":
                self.parse_label(line, pc)
            elif line[:2] == "//":
                continue
            else:
                asm.append(self.c_instruction(line))
                pc += 1

        for ai, a in enumerate(asm):
            if a == "@ponggame.0":
                print("??")
            if a[0] == "@":
                print(a)
                if "@pong" in a:
                    print("???")
                after= self.a_instruction(a)
                asm[ai] = after
        return "\n".join(asm)


if __name__ == "__main__":
    f = argv[1]
    asm = Assembler()
    out = asm.assemble_file(f)
    outf = f.replace(".asm", ".hack")
    with open(outf, "w") as outfile:
        outfile.write(out)
        print("Wrote to", outf)
