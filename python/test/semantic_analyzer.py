
from unittest import TestCase

from lexer import Lexer
from parser import Parser
from symbol import BuiltinTypeSymbol
from symbol import VarSymbol
from semantic_analyzer import SemanticAnalyzer
from semantic_analyzer import PascalNameError
from semantic_analyzer import PascalDuplicateIdentifier


class SemanticAnalyzerTc(TestCase):
    def test_part11(self):
        with open("test/data/part11.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            stb.analyze()

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
            stb = _make_semantic_analyzer(text=source_file.read())
            with self.assertRaises(PascalNameError):
                stb.analyze()

    def test_symtab2(self):
        with open("test/data/symtab2.pas") as source_file:
            sa = _make_semantic_analyzer(text=source_file.read())
            sa.analyze()

            s3 = sa.symtab.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), "INTEGER")

            s4 = sa.symtab.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), "INTEGER")

    def test_symtab4(self):
        with open("test/data/symtab4.pas") as source_file:
            sa = _make_semantic_analyzer(text=source_file.read())
            sa.analyze()

            s3 = sa.symtab.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), "INTEGER")

            s4 = sa.symtab.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), "INTEGER")

    def test_symtab5(self):
        with open("test/data/symtab5.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            with self.assertRaises(PascalNameError):
                stb.analyze()

    def test_symtab6(self):
        with open("test/data/symtab6.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            with self.assertRaises(PascalDuplicateIdentifier):
                stb.analyze()



def _make_semantic_analyzer(text):
    return SemanticAnalyzer(parser=Parser(lexer=Lexer(text=text)))
