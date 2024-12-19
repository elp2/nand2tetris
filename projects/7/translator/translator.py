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
        "and": "D=D&M",
        "or": "D=D|M",
    }
    LOGICAL_OPS = {
        # (Comparison Op, Jump to True condition).
        "eq": ["D=M-D", "JEQ"],
        "gt": ["D=M-D", "JGT"],
        "lt": ["D=M-D", "JLT"],
    }
    UNARY_OPS = {
        "neg": "D=-D",
        "not": "D=!D",
    }
    PUSH_POP_SEGMENTS = {
        "constant": "constant",
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "static": "STATIC",
        "temp": "TEMP",
        "pointer": "POINTER",
    }
    TEMP_OFFSET = 5

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
        assert segment in self.PUSH_POP_SEGMENTS
        segment_label = self.PUSH_POP_SEGMENTS[segment]

        # Put the value of that into D.
        if segment_label == "constant":
            ret = f"@{i}\nD=A\n"
        elif segment_label == "TEMP":
            ret = f"""@{self.TEMP_OFFSET}\n
D=A
@{i}
A=D+A
D=M
"""
        elif segment_label == "POINTER":
            thisthat = ["THIS", "THAT"][i]
            ret = f"""@{thisthat}
D=M
"""
        else:
            ret = f"""@{segment_label}
D=M
@{i}
A=D+A
D=M
"""

        ret += self.expand(["RAM_SP_EQ_D", "SP_INC"])
        return ret

    def pop(self, split):
        segment = split[1]
        i = int(split[2])
        assert segment in self.PUSH_POP_SEGMENTS
        assert segment != "constant"
        segment_label = self.PUSH_POP_SEGMENTS[segment]

        # Calculate base address into D.
        if segment == "temp":
            ret = f"""@{self.TEMP_OFFSET}
D=A
"""
        elif segment_label == "POINTER":
            ret = self.expand(["POP_Y"])
            thisthat = ["THIS", "THAT"][i]
            ret += f"""@{thisthat}
M=D
"""
            return ret
        else:
            ret = f"""@{segment_label}
D=M
"""
        # Add the offset from the base and store into temp register.
        ret += f"""@{i}
D=D+A
@R13
M=D
"""
        # Pop SP into D
        ret += self.expand(["POP_Y"])
        ret += f"""@R13
A=M
M=D
"""
        return ret


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
    # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/StackArithmetic/SimpleAdd/SimpleAdd.vm"
    # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/StackArithmetic/StackTest/StackTest.vm"
    # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/BasicTest/BasicTest.vm"
    # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/BasicTest/BasicTest.vm"
    f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/PointerTest/PointerTest.vm"
    assert f.endswith(".vm")
    translator = Translator()
    out = translator.translate(f)
    outf = f.replace(".vm", ".asm")
    with open(outf, "w") as outfile:
        outfile.write(out)
        print("Wrote to", outf)