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
        engine = CompilationEngine(input_content)
        engine.compile()
        self.assertEqual(engine.output, expected_output)

    def test_simple_if_statement(self):
        # Test input with a simple class containing class variable declarations
        input_content = """if (((y + size) < 254) & ((x + size) < 510)) {}"""
        
        expected_output = [
            "<ifStatement>",
            "  <keyword> if </keyword>",
            "  <symbol> ( </symbol>",
            "  <expression>",
            "    <term>",
            "      <symbol> ( </symbol>",
            "      <expression>",
            "        <term>",
            "          <symbol> ( </symbol>",
            "          <expression>",
            "            <term>",
            "              <identifier> y </identifier>",
            "            </term>",
            "            <symbol> + </symbol>",
            "            <term>",
            "              <identifier> size </identifier>",
            "            </term>",
            "          </expression>",
            "          <symbol> ) </symbol>",
            "        </term>",
            "        <symbol> &lt; </symbol>",
            "        <term>",
            "          <integerConstant> 254 </integerConstant>",
            "        </term>",
            "      </expression>",
            "      <symbol> ) </symbol>",
            "    </term>",
            "    <symbol> &amp; </symbol>",
            "    <term>",
            "      <symbol> ( </symbol>",
            "      <expression>",
            "        <term>",
            "          <symbol> ( </symbol>",
            "          <expression>",
            "            <term>",
            "              <identifier> x </identifier>",
            "            </term>",
            "            <symbol> + </symbol>",
            "            <term>",
            "              <identifier> size </identifier>",
            "            </term>",
            "          </expression>",
            "          <symbol> ) </symbol>",
            "        </term>",
            "        <symbol> &lt; </symbol>",
            "        <term>",
            "          <integerConstant> 510 </integerConstant>",
            "        </term>",
            "      </expression>",
            "      <symbol> ) </symbol>",
            "    </term>",
            "  </expression>",
            "  <symbol> ) </symbol>",
            "  <symbol> { </symbol>",
            "  <statements>",
            "  </statements>",
            "  <symbol> } </symbol>",
            "</ifStatement>"
        ]
        engine = CompilationEngine(input_content)
        engine.compile_if_statement()
        self.assertEqual(engine.output, expected_output)

    def test_simple_while_statement(self):
        input_content = """while (~(key = 0)) {}"""
        
        expected_output = [
            "<whileStatement>",
            "  <keyword> while </keyword>",
            "  <symbol> ( </symbol>",
            "  <expression>",
            "    <term>",
            "      <symbol> ~ </symbol>",
            "      <term>",
            "        <symbol> ( </symbol>",
            "        <expression>",
            "          <term>",
            "            <identifier> key </identifier>",
            "          </term>",
            "          <symbol> = </symbol>",
            "          <term>",
            "            <integerConstant> 0 </integerConstant>",
            "          </term>",
            "        </expression>",
            "        <symbol> ) </symbol>",
            "      </term>",
            "    </term>",
            "  </expression>",
            "  <symbol> ) </symbol>",
            "  <symbol> { </symbol>",
            "  <statements>",
            "  </statements>",
            "  <symbol> } </symbol>",
            "</whileStatement>",
        ]
        engine = CompilationEngine(input_content)
        engine.compile_while_statement()
        self.assertEqual(engine.output, expected_output)

if __name__ == '__main__':
    unittest.main()
