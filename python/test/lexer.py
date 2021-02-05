
from unittest import TestCase

from lexer import Lexer


def _make_lexer(text):
    return Lexer(text)


class LexerTc(TestCase):
    def test_lexer_integer(self):
        from lexer import INTEGER
        lexer = _make_lexer("42")
        token = lexer.get_next_token()
        self._check_token(token=token, expected_type=INTEGER, expected_value=42)

    def test_lexer_div(self):
        lexer = _make_lexer("/")
        token = lexer.get_next_token()
        from lexer import DIVIDE
        self._check_token(token=token, expected_type=DIVIDE, expected_value="/")

    def test_lexer_minus(self):
        lexer = _make_lexer("-")
        token = lexer.get_next_token()
        from lexer import MINUS
        self._check_token(token=token, expected_type=MINUS, expected_value="-")

    def test_lexer_mul(self):
        lexer = _make_lexer("*")
        token = lexer.get_next_token()
        from lexer import MULTIPLY
        self._check_token(
            token=token, expected_type=MULTIPLY, expected_value="*"
        )

    def test_lexer_plus(self):
        lexer = _make_lexer("+")
        token = lexer.get_next_token()
        from lexer import PLUS
        self._check_token(token=token, expected_type=PLUS, expected_value="+")

    def test_lexer_lpar(self):
        lexer = _make_lexer("(")
        token = lexer.get_next_token()
        from lexer import LPAR
        self._check_token(token=token, expected_type=LPAR, expected_value="(")

    def test_lexer_rpar(self):
        lexer = _make_lexer(")")
        token = lexer.get_next_token()
        from lexer import RPAR
        self._check_token(token=token, expected_type=RPAR, expected_value=")")

    def test_lexer_begin(self):
        lexer = _make_lexer("BEGIN")
        token = lexer.get_next_token()
        from lexer import BEGIN
        self._check_token(
            token=token, expected_type=BEGIN, expected_value="BEGIN"
        )

    def test_lexer_begin(self):
        lexer = _make_lexer("END")
        token = lexer.get_next_token()
        from lexer import END
        self._check_token(
            token=token, expected_type=END, expected_value="END"
        )

    def test_lexer_dot(self):
        lexer = _make_lexer(".")
        token = lexer.get_next_token()
        from  lexer import DOT
        self._check_token(token=token, expected_type=DOT, expected_value=".")

    def test_lexer_assign(self):
        lexer = _make_lexer(":=")
        token = lexer.get_next_token()
        from lexer import ASSIGN
        self._check_token(
            token=token, expected_type=ASSIGN, expected_value=":="
        )

    def test_lexer_semi(self):
        lexer = _make_lexer(";")
        token = lexer.get_next_token()
        from lexer import SEMI
        self._check_token(token=token, expected_type=SEMI, expected_value=";")

    def test_lexer_variable1(self):
        lexer = _make_lexer("x")
        token = lexer.get_next_token()
        from lexer import ID
        self._check_token(token=token, expected_type=ID, expected_value="x")

    def test_lexer_variable2(self):
        lexer = _make_lexer("vario")
        token = lexer.get_next_token()
        from lexer import ID
        self._check_token(token=token, expected_type=ID, expected_value="vario")

    def test_lexer_expression(self):
        lexer = _make_lexer("10 + 11 - 12 * 13 / 2")
        from lexer import (
            INTEGER,
            DIVIDE,
            PLUS,
            MINUS,
            MULTIPLY,
            EOF,
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=INTEGER,
            expected_value=10
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=PLUS,
            expected_value="+"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=INTEGER,
            expected_value=11
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=MINUS,
            expected_value="-"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=INTEGER,
            expected_value=12
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=MULTIPLY,
            expected_value="*"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=INTEGER,
            expected_value=13
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=DIVIDE,
            expected_value="/"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=INTEGER,
            expected_value=2
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=EOF,
            expected_value=None
        )

    def test_begin_assign_end(self):
        lexer = _make_lexer("BEGIN a := 2; END.")
        from lexer import (
            ASSIGN,
            DOT,
            ID,
            INTEGER,
            SEMI,
            EOF,
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type="BEGIN",
            expected_value="BEGIN"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=ID,
            expected_value="a"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=ASSIGN,
            expected_value=":="
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=INTEGER,
            expected_value=2
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=SEMI,
            expected_value=";"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type="END",
            expected_value="END"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=DOT,
            expected_value="."
        )

    def _check_token(self, token, expected_type, expected_value):
        self.assertEqual(token.get_type(), expected_type)
        self.assertEqual(token.get_value(), expected_value)
