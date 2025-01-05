import unittest
from compilation_engine import CompilationEngine

class TestCompilationEngine(unittest.TestCase):
    def test_simple_class_with_var_dec(self):
        # Test input with a simple class containing class variable declarations
        input_content = """
        class Test {
            static int x, y;
            field boolean flag;
        }
        """
        
        expected_output = [
            "<class>",
            "  <keyword> class </keyword>",
            "  <identifier> Test </identifier>", 
            "  <symbol> { </symbol>",
            "  <classVarDec>",
            "    <keyword> static </keyword>",
            "    <keyword> int </keyword>",
            "    <identifier> x </identifier>",
            "    <symbol> , </symbol>",
            "    <identifier> y </identifier>",
            "    <symbol> ; </symbol>",
            "  </classVarDec>",
            "  <classVarDec>",
            "    <keyword> field </keyword>",
            "    <keyword> boolean </keyword>",
            "    <identifier> flag </identifier>",
            "    <symbol> ; </symbol>",
            "  </classVarDec>",
            "  <symbol> } </symbol>",
            "</class>"
        ]
        engine = CompilationEngine(input_content, "test_output.xml")
        engine.compile()
        self.assertEqual(engine.output, expected_output)

if __name__ == '__main__':
    unittest.main()
