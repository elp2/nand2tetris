import unittest
from symbol_table import SymbolTable, Symbol

class TestSymbolTable(unittest.TestCase):
    def test_double_define_raises_error(self):
        table = SymbolTable()
        table.define("x", "int", Symbol.Kind.VAR)
        with self.assertRaises(ValueError):
            table.define("x", "int", Symbol.Kind.VAR)

    def test_multiple_locals_and_arg_indexed_separately(self):
        table = SymbolTable()
        
        # Add an argument
        table.define("arg1", "boolean", Symbol.Kind.ARG)
        self.assertEqual(table.var_count(Symbol.Kind.ARG), 1)
        
        # Add some locals
        table.define("local1", "int", Symbol.Kind.VAR)
        table.define("local2", "char", Symbol.Kind.VAR)
        table.define("local3", "int", Symbol.Kind.VAR)
        
        self.assertEqual(table.var_count(Symbol.Kind.VAR), 3)
        self.assertEqual(table.var_count(Symbol.Kind.ARG), 1)
        
        # Check indexes are assigned correctly
        self.assertEqual(table.by_name["local1"].index, 0)
        self.assertEqual(table.by_name["local2"].index, 1)
        self.assertEqual(table.by_name["local3"].index, 2)
        self.assertEqual(table.by_name["arg1"].index, 0)

    def test_simple_local_variable(self):
        table = SymbolTable()
        table.define("counter", "int", Symbol.Kind.VAR)
        
        symbol = table.by_name["counter"]
        self.assertEqual(symbol.name, "counter")
        self.assertEqual(symbol.type, "int")
        self.assertEqual(symbol.kind, Symbol.Kind.VAR)
        self.assertEqual(symbol.index, 0)
        self.assertEqual(table.var_count(Symbol.Kind.VAR), 1)

    def test_class_type_arg(self):
        table = SymbolTable()
        table.define("point", "Point", Symbol.Kind.ARG)
        
        symbol = table.by_name["point"]
        self.assertEqual(symbol.name, "point")
        self.assertEqual(symbol.type, "Point") 
        self.assertEqual(symbol.kind, Symbol.Kind.ARG)
        self.assertEqual(symbol.index, 0)
        self.assertEqual(table.var_count(Symbol.Kind.ARG), 1)

if __name__ == '__main__':
    unittest.main()
