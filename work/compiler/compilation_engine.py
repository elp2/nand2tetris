from jack_tokenizer import JackTokenizer, JackToken
from symbol_table import SymbolTable, Symbol
from vm_writer import VMWriter

OPS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
UNARY_OPS = ["-", "~"]
KEYWORD_CONSTANTS = ["true", "false", "null", "this"]

class CompilationEngine:
    def __init__(self, content: str):
        """Initialize the compilation engine with Jack source content and output file"""
        self.content = content
        self.tokenizer = JackTokenizer(content)
        self.tokenizer.advance()
        self.output = []
        self.indent_level = 0

        self.class_symbol_table = SymbolTable()
        self.subroutine_symbol_table = SymbolTable()
        self.class_name = None
        self.subroutine_name = None

        self.vm_writer = VMWriter()

    def compile(self):
        """Compile the Jack code and write the output XML"""
        while self.tokenizer.has_more_tokens():
            self.compile_class()

    def compile_class(self):
        """Compile a class"""
        self.indent_level = 0
        self._write_rule_start("class")
        self.process(JackToken.TokenType.KEYWORD, "class")
        self.class_name = self.process(JackToken.TokenType.IDENTIFIER)
        self.process(JackToken.TokenType.SYMBOL, "{")
        while (self.tokenizer.get_current_token().get_token_type() == JackToken.TokenType.KEYWORD and 
               self.tokenizer.get_current_token().get_token() in ["static", "field"]):
            self.compile_class_var_dec()
        while (self.tokenizer.get_current_token().get_token_type() == JackToken.TokenType.KEYWORD and
               self.tokenizer.get_current_token().get_token() in ["constructor", "function", "method"]):
            self.compile_subroutine()
        self.process(JackToken.TokenType.SYMBOL, "}")
        self._write_rule_end("class")

    def compile_class_var_dec(self):
        """Compile a class variable declaration"""
        self._write_rule_start("classVarDec")
        STATIC_FIELD = {"static": Symbol.Kind.STATIC, "field": Symbol.Kind.FIELD}
        kind = STATIC_FIELD[self.process(JackToken.TokenType.KEYWORD, ["static", "field"])]

        var_type = self.process_var_type()
        var_names = []
        var_names.append(self.process(JackToken.TokenType.IDENTIFIER))
        while self.tokenizer.get_current_token().get_token() == ",":
            self.process(JackToken.TokenType.SYMBOL, ",")
            var_names.append(self.process(JackToken.TokenType.IDENTIFIER))

        self.process(JackToken.TokenType.SYMBOL, ";")
        for var_name in var_names:
            self.class_symbol_table.define(var_name, var_type, kind)
            self.output.append(f"{self._indent()}{var_name} {var_type} {kind.value} CREATED")

        self._write_rule_end("classVarDec")
    
    def compile_subroutine(self):
        """Compile a subroutine"""
        self._write_rule_start("subroutineDec")

        self.return_counter = 0

        self.constructor_function_method = self.process(JackToken.TokenType.KEYWORD, ["constructor", "function", "method"])
        
        if self.tokenizer.get_current_token().get_token() == "void":
            subroutine_return_type = self.process(JackToken.TokenType.KEYWORD)
        else:
            subroutine_return_type = self.process_var_type()

        self.subroutine_name = self.process(JackToken.TokenType.IDENTIFIER)
        self.subroutine_symbol_table = SymbolTable()

        if self.constructor_function_method == "method":
            self.subroutine_symbol_table.define("this", self.class_name, Symbol.Kind.ARG)
            self.output.append(f"{self._indent()}this {self.class_name} ARG CREATED")


        self.process(JackToken.TokenType.SYMBOL, "(")
        self.compile_parameter_list()
        self.process(JackToken.TokenType.SYMBOL, ")")

        self.compile_subroutine_body()

        self._write_rule_end("subroutineDec")

    def get_next_label(self, description: str):
        """Get the next label"""
        self.return_counter += 1
        return f"{self.class_name}.{self.subroutine_name}${description}{self.return_counter}"
    
    def compile_parameter_list(self):
        """Compile a parameter list"""
        self._write_rule_start("parameterList")
        if self.tokenizer.get_current_token().get_token() == ")":
            self._write_rule_end("parameterList")
            return

        var_type = self.process_var_type()
        var_name = self.process(JackToken.TokenType.IDENTIFIER)
        self.subroutine_symbol_table.define(var_name, var_type, Symbol.Kind.ARG)
        self.output.append(f"{self._indent()}{var_name} {var_type} ARG CREATED")

        while self.tokenizer.get_current_token().get_token() == ",":
            self.process(JackToken.TokenType.SYMBOL, ",")
            var_type = self.process_var_type()
            var_name = self.process(JackToken.TokenType.IDENTIFIER)
            self.subroutine_symbol_table.define(var_name, var_type, Symbol.Kind.ARG)
            self.output.append(f"{self._indent()}{var_name} {var_type} ARG CREATED")

        self._write_rule_end("parameterList")
    
    def compile_subroutine_body(self):
        """Compile a subroutine body"""
        self._write_rule_start("subroutineBody")
        self.process(JackToken.TokenType.SYMBOL, "{")

        vars = []
        while (self.tokenizer.get_current_token().get_token_type() == JackToken.TokenType.KEYWORD and
               self.tokenizer.get_current_token().get_token() in ["var"]):
            vars.append(self.compile_var_dec())
        for (var_type, var_names) in vars:
            for var_name in var_names:
                self.subroutine_symbol_table.define(var_name, var_type, Symbol.Kind.VAR)
                self.output.append(f"{self._indent()}{var_name} {var_type} VAR CREATED")
        self.vm_writer.write_function(self.class_name, self.subroutine_name, self.subroutine_symbol_table.get_n_locals(), self.constructor_function_method)
        
        if self.constructor_function_method == "constructor":
            self.vm_writer.write_push(Symbol.Kind.CONSTANT.to_vm_segment(), self.class_symbol_table.get_n_fields())
            self.vm_writer.write_call("Memory", "alloc", 1)
            self.vm_writer.write_pop(Symbol.Kind.POINTER.to_vm_segment(), 0)

        self.compile_statements()

        self.process(JackToken.TokenType.SYMBOL, "}")
        self._write_rule_end("subroutineBody")
    
    def compile_var_dec(self):
        """Compile a variable declaration"""
        self._write_rule_start("varDec")
        self.process(JackToken.TokenType.KEYWORD, "var")
        var_type = self.process_var_type()
        var_names = [self.process(JackToken.TokenType.IDENTIFIER)]
        while self.tokenizer.get_current_token().get_token() == ",":
            self.process(JackToken.TokenType.SYMBOL, ",")
            var_names.append(self.process(JackToken.TokenType.IDENTIFIER))
        self.process(JackToken.TokenType.SYMBOL, ";")
        self._write_rule_end("varDec")

        return (var_type, var_names)
    
    def compile_statements(self):
        """Compile a statement"""
        self._write_rule_start("statements")
        while True:
            if (self.tokenizer.get_current_token().get_token_type() == JackToken.TokenType.KEYWORD and
               self.tokenizer.get_current_token().get_token() in ["let", "if", "while", "do", "return"]):
                self.compile_statement()
            else:
                break
        self._write_rule_end("statements")

    def compile_statement(self):
        """Compile a statement"""

        {
            "let": self.compile_let_statement,
            "if": self.compile_if_statement,
            "while": self.compile_while_statement,
            "do": self.compile_do_statement,
            "return": self.compile_return_statement
        }[self.tokenizer.get_current_token().get_token()]()
    
    def compile_let_statement(self):
        """Compile a let statement"""
        self._write_rule_start("letStatement")
        self.process(JackToken.TokenType.KEYWORD, "let")
        var_name = self.process(JackToken.TokenType.IDENTIFIER)
        if self.tokenizer.get_current_token().get_token() == "[":
            # arrayName "[" expression "]"
            array_name = var_name
            self.process(JackToken.TokenType.SYMBOL, "[")
            self.compile_expression()
            self.process(JackToken.TokenType.SYMBOL, "]")
        self.process(JackToken.TokenType.SYMBOL, "=")
        self.compile_expression()

        symbol = self._get_from_symbol_table(var_name)
        self.vm_writer.write_pop(symbol.get_kind().to_vm_segment(), symbol.get_index())

        self.process(JackToken.TokenType.SYMBOL, ";")
        self._write_rule_end("letStatement")

    def compile_if_statement(self):
        """Compile an if statement"""
        self._write_rule_start("ifStatement")

        label_else = self.get_next_label("else")
        label_done = self.get_next_label("done")

        self.process(JackToken.TokenType.KEYWORD, "if")
        self.process(JackToken.TokenType.SYMBOL, "(")

        self.compile_expression()
        self.vm_writer.write_raw_TODO_REMOVE("not")
        self.vm_writer.write_if(label_else)

        self.process(JackToken.TokenType.SYMBOL, ")")
        self.process(JackToken.TokenType.SYMBOL, "{")

        self.compile_statements()
        self.vm_writer.write_goto(label_done)

        self.process(JackToken.TokenType.SYMBOL, "}")

        if self.tokenizer.get_current_token().get_token() == "else":
            self.vm_writer.write_label(label_else)
            self.process(JackToken.TokenType.KEYWORD, "else")
            self.process(JackToken.TokenType.SYMBOL, "{")
            self.compile_statements()
            self.process(JackToken.TokenType.SYMBOL, "}")
        else:
            self.vm_writer.write_label(label_else)

        self.vm_writer.write_label(label_done)

        self._write_rule_end("ifStatement")

    def compile_while_statement(self):
        """Compile a while statement"""
        self._write_rule_start("whileStatement")

        label_start = self.get_next_label("whileStart")
        label_end = self.get_next_label("whileEnd")

        self.process(JackToken.TokenType.KEYWORD, "while")
        self.process(JackToken.TokenType.SYMBOL, "(")

        self.vm_writer.write_label(label_start)
        self.compile_expression()
        self.vm_writer.write_raw_TODO_REMOVE("not")
        self.vm_writer.write_if(label_end)

        self.process(JackToken.TokenType.SYMBOL, ")")
        self.process(JackToken.TokenType.SYMBOL, "{")

        self.compile_statements()

        self.process(JackToken.TokenType.SYMBOL, "}")

        self.vm_writer.write_goto(label_start)
        self.vm_writer.write_label(label_end)

        self._write_rule_end("whileStatement")

    def compile_do_statement(self):
        """Compile a do statement"""
        self._write_rule_start("doStatement")
        self.process(JackToken.TokenType.KEYWORD, "do")

        self.compile_subroutine_call(self.process())

        self.process(JackToken.TokenType.SYMBOL, ";")
        self._write_rule_end("doStatement")

    def compile_return_statement(self):
        """Compile a return statement"""
        self._write_rule_start("returnStatement")
        self.process(JackToken.TokenType.KEYWORD, "return")
        void_return = True
        if self.tokenizer.get_current_token().get_token() != ";":
            self.compile_expression()
            void_return = False
        self.vm_writer.write_return(void_return)
        self.process(JackToken.TokenType.SYMBOL, ";")
        self._write_rule_end("returnStatement")
    
    def compile_expression(self):
        """Compile an expression"""
        self._write_rule_start("expression")
    
        self.compile_term()
        while self.tokenizer.get_current_token().get_token() in OPS:
            op = self.process(JackToken.TokenType.SYMBOL, OPS)
            self.compile_term()
            self.vm_writer.write_arithmetic(op)

        self._write_rule_end("expression")

    def compile_expression_list(self, target: str = None):
        """Compile an expression list"""
        self._write_rule_start("expressionList")

        if self._is_variable(target):
            var = self._get_from_symbol_table(target)
            self.vm_writer.write_push(var.get_kind().to_vm_segment(), var.get_index())
            n_expressions = 1
            target = self._get_from_symbol_table(target).get_type()
        elif target == "this" and self.constructor_function_method == "constructor":
            self.vm_writer.write_push(Symbol.Kind.POINTER.to_vm_segment(), 0)
            n_expressions = 1
        else:
            n_expressions = 0

        if self.tokenizer.get_current_token().get_token() == ")":
            self._write_rule_end("expressionList")
            return n_expressions

        self.compile_expression()
        n_expressions += 1
        while self.tokenizer.get_current_token().get_token() == ",":
            self.process(JackToken.TokenType.SYMBOL, ",")
            self.compile_expression()
            n_expressions += 1

        self._write_rule_end("expressionList")
        return n_expressions

    def compile_subroutine_call(self, t1: str):
        """Compile a subroutine call"""
        # Does not print rule name.
        next_token = self.tokenizer.get_current_token()

        if next_token.get_token() == ".":
            # (className | varName) "." subroutineName "(" expressionList ")"
            class_var_name = t1
            self.process(JackToken.TokenType.SYMBOL, ".")
            subroutine_name = self.process(JackToken.TokenType.IDENTIFIER)
            self.process(JackToken.TokenType.SYMBOL, "(")
            n_args = self.compile_expression_list(class_var_name)
            self.process(JackToken.TokenType.SYMBOL, ")")
        elif next_token.get_token() == "(":
            class_var_name = self.class_name
            subroutine_name = t1
            self.process(JackToken.TokenType.SYMBOL, "(")
            n_args = self.compile_expression_list("this" if self.constructor_function_method in ["method", "constructor"] else None)
            self.process(JackToken.TokenType.SYMBOL, ")")
        else:
            assert False
 
        if self._is_variable(class_var_name):
            class_var_name = self._get_from_symbol_table(class_var_name).get_type()
        self.vm_writer.write_call(class_var_name, subroutine_name, n_args)

    def compile_term(self):
        """Compile a term"""
        self._write_rule_start("term")

        # Lookahead for LL(2) parsing edge case.
        t1 = self.process_token()
        next_token = self.tokenizer.get_current_token()
        if next_token.get_token() == "[":
            # arrayName "[" expression "]"
            array_name = t1
            self.process(JackToken.TokenType.SYMBOL, "[")
            self.compile_expression()
            self.process(JackToken.TokenType.SYMBOL, "]")
        elif t1.get_token() == "(":
            # ( expression )
            self.compile_expression()
            self.process(JackToken.TokenType.SYMBOL, ")")
        elif t1.get_token() in UNARY_OPS:
            # unaryOp term
            self.compile_term()
            self.vm_writer.write_unary_op(t1.get_token())
        elif next_token.get_token() in [".", "("]:
            self.compile_subroutine_call(t1.get_token())
        elif t1.get_token_type() == JackToken.TokenType.INTEGER:
            self.vm_writer.write_push(Symbol.Kind.CONSTANT.to_vm_segment(), t1.get_token())
        elif t1.get_token_type() == JackToken.TokenType.STRING:
            # TODO: handle string constants.
            print("UNHANDLED STRING CONSTANT", t1)
            pass
        elif t1.get_token() in KEYWORD_CONSTANTS:
            self.vm_writer.write_keyword_constant(t1.get_token())
        else:
            var_name = t1.get_token()
            symbol = self._get_from_symbol_table(var_name)
            self.vm_writer.write_push(symbol.get_kind().to_vm_segment(), symbol.get_index())

        self._write_rule_end("term")

    def process_var_type(self):
        """Processes a variable type"""
        token = self.tokenizer.get_current_token()
        if token.get_token_type() == JackToken.TokenType.IDENTIFIER:
            return self.process(JackToken.TokenType.IDENTIFIER)
        return self.process(JackToken.TokenType.KEYWORD, ["int", "char", "boolean"])

    def process_token(self, expected_type: JackToken.TokenType = None, expected_values = None):
        """Processes a token, and compares it to expected. Returns the token for the caller to use if needed."""
        token = self.tokenizer.get_current_token()
        if expected_type and token.get_token_type() != expected_type:
            raise Exception(f"Expected Type {expected_type}, got {token.get_token_type()} [{token}] Context: [{self.tokenizer.get_context()}]")
        if expected_values:
            if type(expected_values) == str:
                expected_values = [expected_values]
            if token.get_token() not in expected_values:
                raise Exception(f"Expected Value {expected_values}, got {token.get_token()} [{token}] Context: [{self.tokenizer.get_context()}]")
        self._write_token(token)
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        return token

    def process(self, expected_type: JackToken.TokenType = None, expected_values = None):
        """Processes a token, and compares it to expected. Returns the token for the caller to use if needed."""
        return self.process_token(expected_type, expected_values).get_token()

    
    def write_output(self):
        """Write the compiled output to the XML file"""
        with open(self.output_file, 'w') as f:
            for line in self.output:
                f.write(line + "\r\n")
    
    def _indent(self):
        """Helper to indent the output"""
        return "  " * self.indent_level
    
    def _write_token(self, token: JackToken):
        """Helper to write an XML element with proper indentation"""
        self.output.append(f"{self._indent()}{token.xml_str()}")
    
    def _write_rule_start(self, rule: str):
        """Write the start of a rule"""
        self.output.append(f"{self._indent()}<{rule}>")
        self.indent_level += 1

    def _write_rule_end(self, rule: str):
        """Write the end of a rule"""
        self.indent_level -= 1
        self.output.append(f"{self._indent()}</{rule}>")

    def _is_variable(self, symbol: str):
        """Check if a symbol is a variable"""
        return symbol in self.subroutine_symbol_table or symbol in self.class_symbol_table

    def _get_from_symbol_table(self, symbol: str):
        """Get a symbol from the symbol table"""
        if symbol in self.subroutine_symbol_table:
            return self.subroutine_symbol_table[symbol]
        if symbol in self.class_symbol_table:
            return self.class_symbol_table[symbol]
        
        assert False, f"Symbol {symbol} not found in symbol table"
        return None
