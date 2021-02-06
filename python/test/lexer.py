
from unittest import TestCase

from lexer import Lexer
from lexer import TokenType


def _make_lexer(text):
    return Lexer(text)


class LexerTc(TestCase):
    def test_lexer_integer(self):
        lexer = _make_lexer("42")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.INTEGER, expected_value=42
        )

    def test_lexer_div(self):
        lexer = _make_lexer("/")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.DIVIDE, expected_value="/"
        )

    def test_lexer_minus(self):
        lexer = _make_lexer("-")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.MINUS, expected_value="-"
        )

    def test_lexer_mul(self):
        lexer = _make_lexer("*")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.MULTIPLY, expected_value="*"
        )

    def test_lexer_plus(self):
        lexer = _make_lexer("+")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.PLUS, expected_value="+"
        )

    def test_lexer_lpar(self):
        lexer = _make_lexer("(")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.LPAR, expected_value="("
        )

    def test_lexer_rpar(self):
        lexer = _make_lexer(")")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.RPAR, expected_value=")"
        )

    def test_lexer_begin(self):
        lexer = _make_lexer("BEGIN")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.BEGIN, expected_value="BEGIN"
        )

    def test_lexer_begin_case_insensitive(self):
        lexer = _make_lexer("BeGiN")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.BEGIN, expected_value="BEGIN"
        )

    def test_lexer_end(self):
        lexer = _make_lexer("END")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.END, expected_value="END"
        )

    def test_lexer_end_case_insensitive(self):
        lexer = _make_lexer("End")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.END, expected_value="END"
        )

    def test_lexer_dot(self):
        lexer = _make_lexer(".")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.DOT, expected_value="."
        )

    def test_lexer_assign(self):
        lexer = _make_lexer(":=")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.ASSIGN, expected_value=":="
        )

    def test_lexer_semi(self):
        lexer = _make_lexer(";")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.SEMI, expected_value=";"
        )

    def test_lexer_variable1(self):
        lexer = _make_lexer("x")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.ID, expected_value="x"
        )

    def test_lexer_variable2(self):
        lexer = _make_lexer("vario")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.ID, expected_value="vario"
        )

    def test_lexer_variable2_case_insensitiviy(self):
        lexer = _make_lexer("vArIO")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.ID, expected_value="vario"
        )

    def test_variable_starts_with_underscore(self):
        lexer = _make_lexer("_vario")
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.ID,
            expected_value="_vario"
        )

    def test_variable_ends_with_underscore(self):
        lexer = _make_lexer("vario_")
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.ID,
            expected_value="vario_"
        )

    def test_integer_div(self):
        lexer = _make_lexer("DIV")
        token = lexer.get_next_token()
        self._check_token(
            token=token,
            expected_type=TokenType.INT_DIVIDE,
            expected_value="DIV"
        )

    def test_lexer_expression(self):
        lexer = _make_lexer("10 + 11 - 12 * 13 / 2")
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.INTEGER,
            expected_value=10
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.PLUS,
            expected_value="+"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.INTEGER,
            expected_value=11
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.MINUS,
            expected_value="-"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.INTEGER,
            expected_value=12
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.MULTIPLY,
            expected_value="*"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.INTEGER,
            expected_value=13
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.DIVIDE,
            expected_value="/"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.INTEGER,
            expected_value=2
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.EOF,
            expected_value=None
        )

    def test_begin_assign_end(self):
        lexer = _make_lexer("BEGIN a := 2; END.")
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.BEGIN,
            expected_value="BEGIN"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.ID,
            expected_value="a"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.ASSIGN,
            expected_value=":="
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.INTEGER,
            expected_value=2
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.SEMI,
            expected_value=";"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.END,
            expected_value="END"
        )
        self._check_token(
            token=lexer.get_next_token(),
            expected_type=TokenType.DOT,
            expected_value="."
        )

    def _check_token(self, token, expected_type, expected_value):
        self.assertEqual(token.get_type(), expected_type)
        self.assertEqual(token.get_value(), expected_value)
