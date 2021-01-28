#2021.01.28

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


    def _check_token(self, token, expected_type, expected_value):
        self.assertEqual(token.get_type(), expected_type)
        self.assertEqual(token.get_value(), expected_value)
