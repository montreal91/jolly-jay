
from unittest import TestCase

from lexer import Lexer
from parser import Parser
from symbol import BuiltinTypeSymbol
from symbol import VarSymbol
from symbol import SymbolTableBuilder


class SymbolTableTc(TestCase):
    def test_part11(self):
        with open("test/data/part11.pas") as source_file:
            stb = _make_builder(text=source_file.read())
            stb.build()

            s1 = stb.symtab.lookup("INTEGER")
            self.assertEqual(type(s1), BuiltinTypeSymbol)
            self.assertEqual(s1.get_name(), "INTEGER")
            self.assertEqual(s1.get_type(), None)

            s2 = stb.symtab.lookup("REAL")
            self.assertEqual(type(s2), BuiltinTypeSymbol)
            self.assertEqual(s2.get_name(), "REAL")
            self.assertEqual(s2.get_type(), None)

            s3 = stb.symtab.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), "INTEGER")

            s4 = stb.symtab.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), "REAL")

    def test_name_error(self):
        with open("test/data/name_error1.pas") as source_file:
            stb = _make_builder(text=source_file.read())
            with self.assertRaises(NameError):
                stb.build()


def _make_builder(text):
    return SymbolTableBuilder(parser=Parser(lexer=Lexer(text=text)))
