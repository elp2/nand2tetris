from sys import argv

class Translator:
    TEMPLATES = {
        "RAM_SP_EQ_D": """// RAM[SP] = D
@SP
A=M
M=D""",
        "SP_INC": """// SP++
@SP
M=M+1""",
        "POP_Y": """@SP
M=M-1
A=M
D=M""",
        "POP_X": """@SP
M=M-1
A=M"""
    }
    ARITHMETIC_OPS = {
        "add": "D=D+M",
        "sub": "D=M-D",
        
    }
    # Jump to True
    LOGICAL_OPS = {
        # Operation
        "eq": ["D=M-D", "JEQ"],
        "gt": ["D=M-D", "JGT"],
        "lt": ["D=M-D", "JLT"],
        "and": ["D=D&M", "JNE"],
        "or": ["D=D|M", "JNE"],
    }
    UNARY_OPS = {
        "neg": "D=-D",
        "not": "D=!D",
    }

    def __init__(self):
        self.cond_counter = 0
        pass

    def inc_cond_counter(self):
        self.cond_counter += 1
        return self.cond_counter

    def expand(self, ops):
        s = ""
        for op in ops:
            s += self.TEMPLATES[op] + "\n"
        return s

    def push(self, split):
        segment = split[1]
        i = int(split[2])
        if segment == "constant":
            return f"""// push constant {i}
@{i}
D=A
{self.expand(["RAM_SP_EQ_D", "SP_INC"])}
"""
    def arithmetic(self, op):
        assert op in self.ARITHMETIC_OPS
        return f"""{self.expand(["POP_Y","POP_X"])}
{self.ARITHMETIC_OPS[op]}
{self.expand(["RAM_SP_EQ_D","SP_INC"])}
"""

    def logical(self, op):
        assert op in self.LOGICAL_OPS
        alu_instruction, true_jmp = self.LOGICAL_OPS[op]
        counter = self.inc_cond_counter()
        true_label = f"TRUE_COND.{counter}"
        end_label = f"END_COND.{counter}"

        return f"""{self.expand(["POP_Y","POP_X"])}
{alu_instruction}
@{true_label}
D;{true_jmp}
D=0
@{end_label}
0;JMP
({true_label})
D=-1
({end_label})
{self.expand(["RAM_SP_EQ_D","SP_INC"])}
"""

    def unary(self, op):
        assert op in self.UNARY_OPS
        return f"""{self.expand(["POP_Y"])}
{self.UNARY_OPS[op]}
{self.expand(["RAM_SP_EQ_D","SP_INC"])}
"""

    def handle(self, line):
        split = line.split(" ")
        if split[0] == "//" or split[0] == "":
            return ""
        
        op = split[0]

        if op == "push":
            return self.push(split)
        elif op == "pop":
            return self.pop(split)
        elif op in self.ARITHMETIC_OPS:
            return self.arithmetic(op)
        elif op in self.LOGICAL_OPS:
            return self.logical(op)
        elif op in self.UNARY_OPS:
            return self.unary(op)        
        else:
            assert False

    def translate(self, f):
        ret = ""
        with open(f, "r") as vm:
            for line in vm.readlines():
                line = line.strip()
                handled = self.handle(line)

                here = f"// VM: {line}\n{handled}\n"
                print(here)
                ret += here
        return ret


if __name__ == "__main__":
    # f = argv[1]
    f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/StackArithmetic/StackTest/StackTest.vm"
    assert f.endswith(".vm")
    translator = Translator()
    out = translator.translate(f)
    outf = f.replace(".vm", ".asm")
    with open(outf, "w") as outfile:
        outfile.write(out)
        print("Wrote to", outf)