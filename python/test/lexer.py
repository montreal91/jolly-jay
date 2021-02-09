
from unittest import TestCase

from lexer import Lexer
from lexer import TokenType


def _make_lexer(text):
    return Lexer(text)


class LexerTc(TestCase):
    def test_integer_literal(self):
        lexer = _make_lexer("42")
        token = lexer.get_next_token()
        self._check_token(
            token=token,
            expected_type=TokenType.INTEGER_LITERAL,
            expected_value=42
        )

    def test_real_literal(self):
        lexer = _make_lexer("42.42")
        token = lexer.get_next_token()
        self._check_token(
            token=token,
            expected_type=TokenType.REAL_LITERAL,
            expected_value=42.42
        )

    def test_lexer_div(self):
        lexer = _make_lexer("/")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.REAL_DIV, expected_value="/"
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

    def test_comma_token(self):
        lexer = _make_lexer(",")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.COMMA, expected_value=","
        )

    def test_colon_token(self):
        lexer = _make_lexer(":")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.COLON, expected_value=":"
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

    def test_integer_div_token(self):
        types = [TokenType.INTEGER_DIV] * 3
        values = ["DIV"] * 3
        self._test_lexer("DIV div Div", zip(types, values))

    def test_program_token(self):
        types = [TokenType.PROGRAM] * 3
        values = ["PROGRAM"] * 3
        self._test_lexer("PROGRAM program PrograM", zip(types, values))

    def test_var_token(self):
        expected = [(TokenType.VAR, "VAR")] * 3
        self._test_lexer("VAR var Var", expected)

    def test_integer_token(self):
        types = [TokenType.INTEGER] * 3
        values = ["INTEGER"] * 3
        self._test_lexer("INTEGER integer IntegeR", zip(types, values))

    def test_real_token(self):
        types = [TokenType.REAL] * 3
        values = ["REAL"] * 3
        self._test_lexer("REAL real Real", zip(types, values))

    def test_skip_comment(self):
        types_and_values = (
            (TokenType.ID, "vario"),
            (TokenType.ASSIGN, ":="),
            (TokenType.INTEGER_LITERAL, 42),
            (TokenType.SEMI, ";"),
            (TokenType.EOF, None),
        )
        self._test_lexer(
            "VARIO {This is variable} := {unnecessary comment} 42; {stupid line}",
            types_and_values
        )

    def test_expression(self):
        types_and_values = (
            (TokenType.INTEGER_LITERAL, 10),
            (TokenType.PLUS, "+"),
            (TokenType.INTEGER_LITERAL, 11),
            (TokenType.MINUS, "-"),
            (TokenType.INTEGER_LITERAL, 12),
            (TokenType.MULTIPLY, "*"),
            (TokenType.INTEGER_LITERAL, 13),
            (TokenType.REAL_DIV, "/"),
            (TokenType.INTEGER_LITERAL, 2),
            (TokenType.EOF, None),
        )
        self._test_lexer("10 + 11 - 12 * 13 / 2", types_and_values)

    def test_begin_assign_end(self):
        types_and_values = (
            (TokenType.BEGIN, "BEGIN"),
            (TokenType.ID, "a"),
            (TokenType.ASSIGN, ":="),
            (TokenType.INTEGER_LITERAL, 2),
            (TokenType.SEMI, ";"),
            (TokenType.END, "END"),
            (TokenType.DOT, "."),
            (TokenType.EOF, None),
        )
        self._test_lexer("BEGIN a := 2; END.", types_and_values)

    def _check_token(self, token, expected_type, expected_value):
        self.assertEqual(token.get_type(), expected_type)
        self.assertEqual(token.get_value(), expected_value)

    def _test_lexer(self, text, types_and_values):
        lexer = _make_lexer(text)
        for etype, evalue in types_and_values:
            self._check_token(
                token=lexer.get_next_token(),
                expected_type=etype,
                expected_value=evalue
            )
