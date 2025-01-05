from jack_tokenizer import JackTokenizer, JackToken

class CompilationEngine:
    def __init__(self, content: str, output_filename: str):
        """Initialize the compilation engine with Jack source content and output file"""
        self.content = content
        self.output_file = output_filename
        self.tokenizer = JackTokenizer(content)
        self.tokenizer.advance()
        self.output = []
        self.indent_level = 0
        
    def compile(self):
        """Compile the Jack code and write the output XML"""
        while self.tokenizer.has_more_tokens():
            self.compile_class()

    def compile_class(self):
        """Compile a class"""
        self.indent_level = 0
        self._write_rule_start("class")
        self.process(JackToken.TokenType.KEYWORD, "class")
        className = self.process(JackToken.TokenType.IDENTIFIER)
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
        static_field = self.process(JackToken.TokenType.KEYWORD, 
                                   "static" if self.tokenizer.get_current_token().get_token() == "static" else "field")
        var_type = self.process_var_type()
        var_names = []
        var_names.append(self.process(JackToken.TokenType.IDENTIFIER))
        while self.tokenizer.get_current_token().get_token() == ",":
            self.process(JackToken.TokenType.SYMBOL, ",")
            var_names.append(self.process(JackToken.TokenType.IDENTIFIER))
        self.process(JackToken.TokenType.SYMBOL, ";")
        self._write_rule_end("classVarDec")
    
    def compile_subroutine(self):
        """Compile a subroutine"""
        pass
    
    def compile_parameter_list(self):
        """Compile a parameter list"""
        pass
    
    def compile_subroutine_body(self):
        """Compile a subroutine body"""
        pass
    
    def compile_var_dec(self):
        """Compile a variable declaration"""
        pass
    
    def compile_statements(self):
        """Compile a statement"""
        pass

    def compile_let_statement(self):
        """Compile a let statement"""
        pass

    def compile_if_statement(self):
        """Compile an if statement"""
        pass

    def compile_while_statement(self):
        """Compile a while statement"""
        pass

    def compile_do_statement(self):
        """Compile a do statement"""
        pass

    def compile_return_statement(self):
        """Compile a return statement"""
        pass
    
    def compile_expression(self):
        """Compile an expression"""
        pass

    def compile_expression_list(self):
        """Compile an expression list"""
        pass

    def compile_term(self):
        """Compile a term"""
        pass

    def process_var_type(self):
        """Processes a variable type"""
        token = self.tokenizer.get_current_token()
        if token.get_token_type() == JackToken.TokenType.IDENTIFIER:
            return self.process(JackToken.TokenType.IDENTIFIER)
        elif token.get_token_type() == JackToken.TokenType.KEYWORD:
            if token.get_token() in ["int", "char", "boolean"]:
                return self.process(JackToken.TokenType.KEYWORD)
            else:
                raise Exception(f"Expected Type {JackToken.TokenType.KEYWORD} to be int/char/boolean, got [{token}]")
        else:
            raise Exception(f"Expected Type {JackToken.TokenType.IDENTIFIER} or {JackToken.TokenType.KEYWORD}, got {token.get_token_type()} [{token}]")

    def process(self, expected_type: JackToken.TokenType = None, expected_value: str = None):
        """Processes a token, and compares it to expected. Returns the token for the caller to use if needed."""
        token = self.tokenizer.get_current_token()
        if expected_type and token.get_token_type() != expected_type:
            raise Exception(f"Expected Type {expected_type}, got {token.get_token_type()} [{token}]")
        if expected_value and token.get_token() != expected_value:
            raise Exception(f"Expected Value {expected_value}, got {token.get_token()} [{token}]")
        self._write_terminal(token)
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
        return token
    
    def write_output(self):
        """Write the compiled output to the XML file"""
        with open(self.output_file, 'w') as f:
            for line in self.output:
                f.write(line + "\r\n")
    
    def _indent(self):
        """Helper to indent the output"""
        return "  " * self.indent_level
    
    def _write_element(self, tag: str, content: str):
        """Helper to write an XML element with proper indentation"""
        self.output.append(f"{self._indent()}<{tag}> {content} </{tag}>")
    
    def _write_rule_start(self, rule: str):
        """Write the start of a rule"""
        self.output.append(f"{self._indent()}<{rule}>")
        self.indent_level += 1

    def _write_rule_end(self, rule: str):
        """Write the end of a rule"""
        self.indent_level -= 1
        self.output.append(f"{self._indent()}</{rule}>")

    # TODO: Remove this???
    def _write_terminal(self, token: JackToken):
        """Write a terminal token element"""
        token_type = token.get_token_type().value.lower()
        token_value = token.get_token()
        
        # Handle special XML characters
        if token_type == "symbol":
            if token_value == "<":
                token_value = "&lt;"
            elif token_value == ">":
                token_value = "&gt;" 
            elif token_value == "&":
                token_value = "&amp;"
                
        if token_type == "integer":
            token_type = "integerConstant"
        elif token_type == "string":
            token_type = "stringConstant"
            
        self._write_element(token_type, token_value)
