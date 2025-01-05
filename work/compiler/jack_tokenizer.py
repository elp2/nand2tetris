KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

class JackToken:
    from enum import Enum
    
    class TokenType(Enum):
        KEYWORD = "KEYWORD"
        SYMBOL = "SYMBOL" 
        INTEGER = "INTEGER"
        STRING = "STRING"
        IDENTIFIER = "IDENTIFIER"
        
    def __init__(self, token: str, token_type: TokenType):
        self.token = token
        self.token_type = token_type
    
    def __str__(self):
        return f"Token: {self.token}, Type: {self.token_type}"
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.token == other.token and self.token_type == other.token_type
    
    def __hash__(self):
        return hash((self.token, self.token_type))

    def getToken(self) -> str:
        """Returns the token string"""
        return self.token

    def getTokenType(self) -> TokenType:
        """Returns the token type"""
        return self.token_type


class JackTokenizer:
    def __init__(self, content: str):
        """Initialize the tokenizer with a Jack source file"""
        self.content = content
        self.removeCommentsAndWhitespace()
        self.index = 0
        self.current_token = None

    def removeCommentsAndWhitespace(self) -> None:
        """Removes comments and whitespace from the content"""

        while True:
            if "/*" in self.content:
                start = self.content.find("/*") 
                end = self.content.find("*/")
                if end == -1:
                    raise Exception("Unterminated comment")
                self.content = self.content[:start] + self.content[end + 2:]
            else:
                break
        while True:
            if "//" in self.content:
                start = self.content.find("//")
                end = self.content.find("\n")
                if end == -1:
                    raise Exception("Unterminated comment")
                self.content = self.content[:start] + self.content[end:]
            else:
                break

        self.content = self.content.strip()

    def charAt(self, index: int) -> str:
        """Returns the character at the given index or None if out of bounds"""
        if index < 0 or index >= len(self.content):
            return None
        return self.content[index]

    def isKeyword(self, token: str) -> bool:
        """Returns true if the token is a keyword"""
        return token in KEYWORDS

    def isSymbol(self, token: str) -> bool:
        """Returns true if the token is a symbol"""
        return token in SYMBOLS

    def hasMoreTokens(self) -> bool:
        """Returns true if there are more tokens to process"""
        return self.index < len(self.content)

    def advance(self) -> None:
        """Advances to the next token. Should only be called if hasMoreTokens is true"""
        if not self.hasMoreTokens():
            raise Exception("No more tokens to process")
        
        # Skip whitespace
        while self.index < len(self.content) and self.content[self.index].isspace():
            self.index += 1
        
        next = self.content[self.index]
        
        if next in SYMBOLS:
            self.current_token = JackToken(next, JackToken.TokenType.SYMBOL)
            self.index += 1
        elif next.isdigit():
            token = ""
            while self.index < len(self.content) and self.content[self.index].isdigit():
                token += self.content[self.index]
                self.index += 1
            self.current_token = JackToken(token, JackToken.TokenType.INTEGER)
        elif next == '"':
            token = '"'
            self.index += 1  # Move past the opening quote
            while self.index < len(self.content) and self.content[self.index] != '"':
                token += self.content[self.index]
                self.index += 1
            self.index += 1 # Move past the closing quote
            self.current_token = JackToken(token[1:], JackToken.TokenType.STRING)
        elif next.isalpha() or next == '_':
            token = ""
            while self.index < len(self.content) and (self.content[self.index].isalnum() or self.content[self.index] == '_'):
                token += self.content[self.index]
                self.index += 1
            token_type = JackToken.TokenType.KEYWORD if self.isKeyword(token) else JackToken.TokenType.IDENTIFIER
            self.current_token = JackToken(token, token_type)
        else:
            raise Exception(f"Invalid character: {next}, context: {self.content[self.index-10:self.index+10]}")
            
    def currentToken(self) -> JackToken:
        """Returns the current token. Should only be called after advance"""
        return self.current_token

    def peek(self) -> str:
        """Returns the next character without advancing"""
        if self.index < len(self.content):
            return self.content[self.index]
        return None
