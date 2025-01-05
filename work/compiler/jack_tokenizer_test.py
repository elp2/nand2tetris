import unittest
from jack_tokenizer import JackTokenizer, JackToken

class TestJackTokenizer(unittest.TestCase):
    def test_remove_comments(self):
        # Test block comment removal
        content = "class SlashStar /* this is a \n comment */ {"
        tokenizer = JackTokenizer(content)
        self.assertEqual(tokenizer.content.strip(), "class SlashStar  {")

        # Test line comment removal 
        content = "class SlashSlash // this is a comment\nlet x = 42"
        tokenizer = JackTokenizer(content)
        self.assertEqual(tokenizer.content.strip(), "class SlashSlash \nlet x = 42")

    def test_let_statement(self):
        content = "let bar = true"
        tokenizer = JackTokenizer(content)
        
        expected_tokens = [
            JackToken("let", JackToken.TokenType.KEYWORD),
            JackToken("bar", JackToken.TokenType.IDENTIFIER), 
            JackToken("=", JackToken.TokenType.SYMBOL),
            JackToken("true", JackToken.TokenType.KEYWORD)
        ]

        tokens = []
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            tokens.append(tokenizer.currentToken())

        self.assertEqual(tokens, expected_tokens)

    def test_do_statement(self):
        content = "do dino.jump()"
        tokenizer = JackTokenizer(content)

        expected_tokens = [
            JackToken("do", JackToken.TokenType.KEYWORD),
            JackToken("dino", JackToken.TokenType.IDENTIFIER),
            JackToken(".", JackToken.TokenType.SYMBOL), 
            JackToken("jump", JackToken.TokenType.IDENTIFIER),
            JackToken("(", JackToken.TokenType.SYMBOL),
            JackToken(")", JackToken.TokenType.SYMBOL)
        ]

        tokens = []
        while tokenizer.hasMoreTokens():
            tokenizer.advance() 
            tokens.append(tokenizer.currentToken())

        self.assertEqual(tokens, expected_tokens)

    def test_string_token(self):
        content = 'let message = "Hello World!"'
        tokenizer = JackTokenizer(content)

        expected_tokens = [
            JackToken("let", JackToken.TokenType.KEYWORD),
            JackToken("message", JackToken.TokenType.IDENTIFIER),
            JackToken("=", JackToken.TokenType.SYMBOL),
            JackToken("Hello World!", JackToken.TokenType.STRING)
        ]

        tokens = []
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            tokens.append(tokenizer.currentToken())

        self.assertEqual(tokens, expected_tokens)

    def test_integer_token(self):
        content = "let x = 42"
        tokenizer = JackTokenizer(content)

        expected_tokens = [
            JackToken("let", JackToken.TokenType.KEYWORD),
            JackToken("x", JackToken.TokenType.IDENTIFIER),
            JackToken("=", JackToken.TokenType.SYMBOL),
            JackToken("42", JackToken.TokenType.INTEGER)
        ]

        tokens = []
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            tokens.append(tokenizer.currentToken())

        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
