
from unittest import TestCase

from spi.lexer import Lexer
from spi.parser import Parser
from spi.semantic_analyzer import SemanticAnalyzer
from spi.semantic_analyzer import PascalNameError
from spi.semantic_analyzer import PascalDuplicateIdentifier
from spi.symbol import BuiltinTypeSymbol
from spi.symbol import ProcedureSymbol
from spi.symbol import VarSymbol

INTEGER_NAME = "integer"
INTEGER_TYPE = "integer"
PROCEDURE_TYPE = "procedure"
REAL_NAME = "real"
REAL_TYPE = "real"


class SemanticAnalyzerTc(TestCase):
    def test_part11(self):
        with open("test/data/part11.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            stb.analyze()

            s1 = stb.scope.lookup(INTEGER_NAME)
            self.assertEqual(type(s1), BuiltinTypeSymbol)
            self.assertEqual(s1.get_name(), INTEGER_NAME)
            self.assertEqual(s1.get_type(), None)

            s2 = stb.scope.lookup(REAL_NAME)
            self.assertEqual(type(s2), BuiltinTypeSymbol)
            self.assertEqual(s2.get_name(), REAL_NAME)
            self.assertEqual(s2.get_type(), None)

            s3 = stb.scope.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), INTEGER_TYPE)

            s4 = stb.scope.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), REAL_NAME)

    def test_name_error(self):
        with open("test/data/name_error1.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            with self.assertRaises(PascalNameError):
                stb.analyze()

    def test_symtab2(self):
        with open("test/data/symtab2.pas") as source_file:
            sa = _make_semantic_analyzer(text=source_file.read())
            sa.analyze()

            s3 = sa.scope.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), INTEGER_TYPE)

            s4 = sa.scope.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), INTEGER_TYPE)

    def test_symtab4(self):
        with open("test/data/symtab4.pas") as source_file:
            sa = _make_semantic_analyzer(text=source_file.read())
            sa.analyze()

            s3 = sa.scope.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), INTEGER_TYPE)

            s4 = sa.scope.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), INTEGER_TYPE)

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

    def test_nested_scopes02(self):
        with open("test/data/nestedscopes02.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            stb.analyze()

            s1 = stb.scope.lookup(INTEGER_NAME)
            self.assertEqual(type(s1), BuiltinTypeSymbol)
            self.assertEqual(s1.get_name(), INTEGER_NAME)
            self.assertEqual(s1.get_type(), None)

            s2 = stb.scope.lookup(REAL_NAME)
            self.assertEqual(type(s2), BuiltinTypeSymbol)
            self.assertEqual(s2.get_name(), REAL_NAME)
            self.assertEqual(s2.get_type(), None)

            s3 = stb.scope.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), REAL_NAME)

            s4 = stb.scope.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), REAL_TYPE)

            s5 = stb.scope.lookup("alpha")
            self.assertEqual(type(s5), ProcedureSymbol)
            self.assertEqual(s5.get_type().get_name(), PROCEDURE_TYPE)

    def test_nested_scopes03(self):
        with open("test/data/nestedscopes03.pas") as source_file:
            stb = _make_semantic_analyzer(text=source_file.read())
            stb.analyze()

            s1 = stb.scope.lookup(INTEGER_NAME)
            self.assertEqual(type(s1), BuiltinTypeSymbol)
            self.assertEqual(s1.get_name(), INTEGER_NAME)
            self.assertEqual(s1.get_type(), None)

            s2 = stb.scope.lookup(REAL_NAME)
            self.assertEqual(type(s2), BuiltinTypeSymbol)
            self.assertEqual(s2.get_name(), REAL_NAME)
            self.assertEqual(s2.get_type(), None)

            s3 = stb.scope.lookup("x")
            self.assertEqual(type(s3), VarSymbol)
            self.assertEqual(s3.get_type().get_name(), REAL_TYPE)

            s4 = stb.scope.lookup("y")
            self.assertEqual(type(s4), VarSymbol)
            self.assertEqual(s4.get_type().get_name(), REAL_TYPE)

            s5 = stb.scope.lookup("alphaa")
            self.assertEqual(type(s5), ProcedureSymbol)
            self.assertEqual(s5.get_type().get_name(), PROCEDURE_TYPE)

            s6 = stb.scope.lookup("alphab")
            self.assertEqual(type(s6), ProcedureSymbol)
            self.assertEqual(s6.get_type().get_name(), PROCEDURE_TYPE)


def _make_semantic_analyzer(text):
    return SemanticAnalyzer(parser=Parser(lexer=Lexer(text=text)))
