from sys import argv

class Translator:
    def __init__(self):
        pass

    def push(self, split):
        segment = split[1]
        i = int(split[2])
        assert i >= 0

        assert segment == "constant"
        lines = f"""// D = i
@{i}
D=A
// RAM[SP] =D
@SP
A=M
M=D
// SP++
@SP
M=M+1
"""
        return lines

    def pop(self, split):
        segment = split[1]
        pass

    def add(self, split):
        lines = f"""// D = SP--
@SP
M=M-1
A=M
D=M 
// Pop and add
@SP
M=M-1
A=M
D=D+M
// RAM[SP]=D
@SP
A=M
M=D
// SP++
@SP
M=M+1
"""
        return lines


    def handle(self, line):
        split = line.split(" ")
        if split[0] == "push":
            return self.push(split)
        elif split[0] == "pop":
            return self.pop(split)
        elif split[0] == "add":
            return self.add(split)
        elif split[0] == "//" or split[0] == "":
            return ""
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
    f = argv[1]
    assert f.endswith(".vm")
    translator = Translator()
    out = translator.translate(f)
    outf = f.replace(".vm", ".asm")
    with open(outf, "w") as outfile:
        outfile.write(out)
        print("Wrote to", outf)