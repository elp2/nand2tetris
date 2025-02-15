import glob
from sys import argv

class Function:
    def __init__(self, file_base, name):
        assert not file_base.endswith(".vm")
        self.file = file_base
        self.name = name
        if self.name.split(".")[0] == self.file:
            self.file, self.name = self.name.split(".")
        self.return_count = 0

    def function_label(self):
        return f"""{self.file}.{self.name}"""
    
    def goto_label(self, label):
        return f"""{self.file}.{self.name}${label}"""

    def next_return_label(self):
        rc = self.return_count = self.return_count + 1
        return f"""{self.file}.{self.name}$ret.{rc}"""


def D_EQ_REG(val_or_label):
    return f"""@{val_or_label}
D=M
"""

def PUSH_D_TO_SP():
    """Push D to SP"""
    return f"""@SP
A=M
M=D
@SP
M=M+1
"""

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
A=M""",
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

    def __init__(self, vm):
        self.cond_counter = 0
        self.vm = vm
        self.lines = []
        self.lines_pos = 0
        self.global_function = Function(self.vm, "GLOBAL")
        self.current_function = None

    def active_function(self):
        if self.current_function:
            return self.current_function
        else:
            return self.global_function

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
            ret = f"""@{i}
D=A
"""
        elif segment_label == "STATIC":
            ret = f"""@{self.vm}.{i}
D=M
"""
        elif segment_label == "TEMP":
            ret = f"""@{self.TEMP_OFFSET}
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
        elif segment_label == "STATIC":
            ret =f"@{self.vm}.{i}\nD=A\n"
            i = 0
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

    def label(self, split):
        _, name = split[:2]
        goto_label = self.active_function().goto_label(name)
        return f"({goto_label})"

    def if_goto(self, split):
        assert split[0] == "if-goto"
        true_label = self.active_function().goto_label(split[1])
        return f"""@{true_label}
D;JNE
"""

    def goto(self, label):
        goto_label = self.active_function().goto_label(label)
        return f"""@{goto_label}
0;JMP
"""

    def define(self):
        # TODO
        return f"""({self.name})
push 0
push 0
push 0
push 0
push 0
push 0
"""

    def call(self, functionname, nArgs):
        nArgs = int(nArgs)
        return_label = self.active_function().next_return_label()
        ret = f"""@{return_label}
D=A
"""
        ret += PUSH_D_TO_SP()
        ret += D_EQ_REG("LCL")
        ret += PUSH_D_TO_SP()
        ret += D_EQ_REG("ARG")
        ret += PUSH_D_TO_SP()
        ret += D_EQ_REG("THIS")
        ret += PUSH_D_TO_SP()
        ret += D_EQ_REG("THAT")
        ret += PUSH_D_TO_SP()

        # ARG = SP – 5 – nArgs // Repositions ARG
        ret += "@SP\nD=M\n"
        ret += f"@{nArgs + 5}\n"
        ret += "D=D-A\n"
        ret += "@ARG\nM=D\n"
        # LCL = SP // Repositions LCL
        ret += """@SP
D=M
@LCL
M=D
"""
        ret += f"""@{functionname}
0;JMP
"""
        ret += f"({return_label})\n"

        return ret


    def unpop_endframe(self, delta, destination):
        return f"""@{delta}
D=A
@R13
D=M-D
A=D
D=M
@{destination}
M=D
"""


    def function_return(self):
        # endFrame = LCL // gets the address at the frame’s end
        ret = ""
        ret += """@LCL
D=M
@R13
M=D
"""
        # retAddr = *(endFrame – 5) // gets the return address
        ret += """@5
D=D-A
A=D
D=M
@R14
M=D
"""
        # *ARG = pop() // puts the return value for the caller
        ret += self.expand(["POP_Y"])
        ret += """@ARG
A=M
M=D
"""

        # SP = ARG + 1 // repositions SP
        ret += """@ARG
D=M
D=D+1
@SP
M=D
"""
        ret += self.unpop_endframe(1, "THAT")
        ret += self.unpop_endframe(2, "THIS")
        ret += self.unpop_endframe(3, "ARG")
        ret += self.unpop_endframe(4, "LCL")
        # goto retAddr // jumps to the return address
        ret += """@R14
A=M
0;JMP
"""
        return ret

    def function(self, name, numLocals):
        self.current_function = Function(self.vm, name)

        ret = f"({self.active_function().function_label()})\n"
        if numLocals == 0:
            return ret
        
        # Set up that many local variables
        ret += """@LCL
A=M
"""
        for _ in range(numLocals):
            ret += """M=0
A=A+1
"""
        # Move SP Forward that many times.
        ret += "@SP\n"
        for _ in range(numLocals):
            ret += """M=M+1\n"""
        return ret

    def handle(self, line):
        line = line.replace("\t", " \t ")
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
        elif op == "label":
            return self.label(split)
        elif op == "if-goto":
            return self.if_goto(split)
        elif op == "goto":
            return self.goto(split[1])
        elif op == "call":
            return self.call(split[1], split[2])
        elif op == "function":
            return self.function(split[1], int(split[2]))
        elif op == "return":
            return self.function_return()
        else:
            assert False

    def next_line(self):
        if self.lines_pos >= len(self.lines):
            return None
        line = self.lines[self.lines_pos]
        line = line.strip()
        self.lines_pos += 1
        return line

    def translate_file(self, f):
        ret = []
        with open(f, "r") as vm:
            self.lines = vm.readlines()
        while True:
            line = self.next_line()
            if line is None:
                return "".join(ret)
            handled = self.handle(line)
            here = f"// VM: {line}\n{handled}\n"
            print(here)
            ret.append(here)

    def bootstrap(self):
        # SP = 256.
        ret = """// Boostrap Start.
@256
D=A
@SP
M=D
""" 
        ret += self.call("Sys.init", 0)
        ret += "// Bootstrap End.\n"
        return ret

if __name__ == "__main__":
    if len(argv) < 2:
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/StackArithmetic/SimpleAdd/SimpleAdd.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/StackArithmetic/StackTest/StackTest.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/BasicTest/BasicTest.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/BasicTest/BasicTest.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/PointerTest/PointerTest.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/7/MemoryAccess/StaticTest/StaticTest.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/8/ProgramFlow/BasicLoop/BasicLoop.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/8/ProgramFlow/FibonacciSeries/FibonacciSeries.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/8/FunctionCalls/NestedFunction/SimpleFunction.vm"
        # f = "/Users/edwardpalmer/dev/nand2tetris/projects/8/FunctionCalls/NestedCall/Sys.vm"
        f = "/Users/edwardpalmer/dev/nand2tetris/projects/8/FunctionCalls/FibonacciElement/"
    else:
        f = argv[1]
    if f.endswith(".vm"):
        vm = f.split("/")[-1].replace(".vm", "")
        translator = Translator(vm)
        out = translator.translate_file(f)
        outf = f.replace(".vm", ".asm")
        with open(outf, "w") as outfile:
            outfile.write(out)
            print("Wrote to", outf)
    elif f.endswith("/"):
        dirname = f.split("/")[-2]
        asm = f"{f}/{dirname}.asm"
        with open(asm, "w") as outfile:
            bootstrap = Translator("bootstrap")
            outfile.write(bootstrap.bootstrap())

            vms = glob.glob(f + "*.vm")
            for vm in vms:
                outfile.write(f"\n// Translating {vm}.")
                vmname = vm.split("/")[-1].replace(".vm", "")                                
                translator = Translator(vmname)
                out = translator.translate_file(vm)                
                outfile.write(out)
            print(f"Wrote {vms} to {asm}")
