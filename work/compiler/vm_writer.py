class VMWriter:
    def __init__(self):
        self.output = []
        self.written_labels = set()

    def write_push(self, segment: str, index: int) -> None:
        self.output.append(f"push {segment} {index}")

    def write_pop(self, segment: str, index: int) -> None:
        self.output.append(f"pop {segment} {index}")

    def write_arithmetic(self, command: str) -> None:
        self.output.append(command)

    def write_label(self, label: str) -> None:
        assert label not in self.written_labels            
        self.written_labels.add(label)
        self.output.append(f"label {label}")
    
    def write_goto(self, label: str) -> None:
        self.output.append(f"goto {label}")
    
    def write_if(self, label: str) -> None:
        self.output.append(f"if-goto {label}")
    
    def write_call(self, class_name: str, subroutine_name: str, n_args: int) -> None:
        self.output.append(f"call {class_name}.{subroutine_name} {n_args}")
    
    def write_function(self, class_name: str, subroutine_name: str, n_vars: int, function_type: str) -> None:
        self.output.append(f"function {class_name}.{subroutine_name} {n_vars}")
        if function_type == "method":
            self.output.append("push argument 0")
            self.output.append("pop pointer 0")
    
    def write_return(self, void_return: bool) -> None:
        if void_return:
            self.output.append("push constant 0")
        self.output.append("return")

    def write_arithmetic(self, op: str) -> None:
        if op == "+":
            self.output.append("add")
        elif op == "-":
            self.output.append("sub")
        elif op == "*":
            self.output.append("call Math.multiply 2")
        elif op == "/":
            self.output.append("call Math.divide 2")
        elif op == "&":
            self.output.append("and")
        elif op == "|":
            self.output.append("or")
        elif op == "<":
            self.output.append("lt")
        elif op == ">":
            self.output.append("gt")
        elif op == "=":
            self.output.append("eq")
        else:
            assert False

    def write_keyword_constant(self, keyword_constant: str) -> None:
        if keyword_constant == "true":
            self.output.append("push constant 1")
            self.output.append("neg")
        elif keyword_constant == "false":
            self.output.append("push constant 0")
        elif keyword_constant == "null":
            self.output.append("push constant 0")
        elif keyword_constant == "this":
            self.output.append("push pointer 0")
        else:
            assert False

    def write_unary_op(self, op: str) -> None:
        if op == "-":
            self.output.append("neg")
        elif op == "~":
            self.output.append("not")
        else:
            assert False

    def write_string(self, string: str) -> None:
        self.output.append(f"push constant {len(string)}")
        self.output.append("call String.new 1")
        for char in string:
            self.output.append(f"push constant {ord(char)}")
            # This returns the string ptr, no need to repush to stack.
            self.output.append("call String.appendChar 2")

    def write_let_array(self) -> None:
        self.output.append("pop pointer 1 // THAT = address of b[j]")
        self.output.append("push that 0 // stack top = b[j]")
        self.output.append("pop temp 0 // temp 0 = b[j]")
        self.output.append("pop pointer 1 // THAT = address of a[i]")
        self.output.append("push temp 0 // stack top = b[j]")
        self.output.append("pop that 0 // a[i] = b[j]")


    def write_raw_TODO_REMOVE(self, line: str) -> None:
        self.output.append(line)

    def write(self, output_file: str) -> None:
        with open(output_file, 'w') as f:
            for line in self.output:
                f.write(line + "\r\n")
