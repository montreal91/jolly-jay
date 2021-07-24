
from unittest import TestCase

from spi.lexer import Lexer
from spi.token import TokenType


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
            token=token, expected_type=TokenType.BEGIN, expected_value="begin"
        )

    def test_lexer_begin_case_insensitive(self):
        lexer = _make_lexer("BeGiN")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.BEGIN, expected_value="begin"
        )

    def test_lexer_end(self):
        lexer = _make_lexer("END")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.END, expected_value="end"
        )

    def test_lexer_end_case_insensitive(self):
        lexer = _make_lexer("End")
        token = lexer.get_next_token()
        self._check_token(
            token=token, expected_type=TokenType.END, expected_value="end"
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

    def test_lexer_variable2_case_insensitivity(self):
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
        values = ["div"] * 3
        self._test_lexer("DIV div Div", zip(types, values))

    def test_program_token(self):
        types = [TokenType.PROGRAM] * 3
        values = ["program"] * 3
        self._test_lexer("PROGRAM program PrograM", zip(types, values))

    def test_procedure_token(self):
        types = [TokenType.PROCEDURE] * 3
        values = ["procedure"] * 3
        self._test_lexer("PROCEDURE procedure Procedure", zip(types, values))

    def test_var_token(self):
        types = [TokenType.VAR] * 3
        values = ["var"] * 3
        self._test_lexer("VAR var Var", zip(types, values))

    def test_integer_token(self):
        types = [TokenType.INTEGER] * 3
        values = ["integer"] * 3
        self._test_lexer("INTEGER integer Integer", zip(types, values))

    def test_real_token(self):
        types = [TokenType.REAL] * 3
        values = ("real", "real", "real")
        self._test_lexer("REAL real Real", zip(types, values))

    def test_skip_comment(self):
        types_and_values = (
            (TokenType.ID, "var_io"),
            (TokenType.ASSIGN, ":="),
            (TokenType.INTEGER_LITERAL, 42),
            (TokenType.SEMI, ";"),
            (TokenType.EOF, None),
        )
        self._test_lexer(
            (
                "VAR_IO {This is variable} := {unnecessary comment} 42; "
                "{stupid line}"
            ),
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
            (TokenType.BEGIN, "begin"),
            (TokenType.ID, "a"),
            (TokenType.ASSIGN, ":="),
            (TokenType.INTEGER_LITERAL, 2),
            (TokenType.SEMI, ";"),
            (TokenType.END, "end"),
            (TokenType.DOT, "."),
            (TokenType.EOF, None),
        )
        self._test_lexer("BEGIN a := 2; END.", types_and_values)

    def test_lines_and_columns(self):
        expected_data = (
            (TokenType.PROGRAM, "program", 2, 1),
            (TokenType.ID, "part15", 2, 9),
            (TokenType.SEMI, ";", 2, 15),
            (TokenType.VAR, "var", 4, 1),
            (TokenType.ID, "xp", 5, 5),
            (TokenType.COLON, ":", 5, 8),
            (TokenType.INTEGER, "integer", 5, 10),
            (TokenType.SEMI, ";", 5, 17),
            (TokenType.ID, "force", 6, 5),
            (TokenType.COLON, ":", 6, 11),
            (TokenType.REAL, "real", 6, 13),
            (TokenType.SEMI, ";", 6, 17),
            (TokenType.BEGIN, "begin", 8, 1),
            (TokenType.ID, "xp", 9, 5),
            (TokenType.ASSIGN, ":=", 9, 8),
            (TokenType.INTEGER_LITERAL, 12, 9, 11),
            (TokenType.SEMI, ";", 9, 13),
            (TokenType.ID, "force", 10, 5),
            (TokenType.ASSIGN, ":=", 10, 11),
            (TokenType.REAL_LITERAL, 18.5, 10, 14),
            (TokenType.SEMI, ";", 10, 18),
            (TokenType.END, "end", 11, 1),
            (TokenType.DOT, ".", 11, 4),
        )
        with open("test/data/part15.pas") as pas_file:
            self._test_extended_lexer(text=pas_file.read(), expected_data=expected_data)

    def test_lexer_16(self):
        expected_data = (
            (TokenType.PROGRAM, "program", 2, 1),
            (TokenType.ID, "part16", 2, 9),
            (TokenType.SEMI, ";", 2, 15),
            (TokenType.PROCEDURE, "procedure", 4, 1),
            (TokenType.ID, "alpha", 4, 11),
            (TokenType.LPAR, "(", 4, 16),
            (TokenType.ID, "a", 4, 17),
            (TokenType.COLON, ":", 4, 19),
            (TokenType.INTEGER, "integer", 4, 21),
            (TokenType.SEMI, ";", 4, 28),
            (TokenType.ID, "b", 4, 30),
            (TokenType.COLON, ":", 4, 32),
            (TokenType.INTEGER, "integer", 4, 34),
            (TokenType.RPAR, ")", 4, 41),
            (TokenType.SEMI, ";", 4, 42),
            (TokenType.VAR, "var", 5, 1),
            (TokenType.ID, "x", 5, 5),
            (TokenType.COLON, ":", 5, 7),
            (TokenType.INTEGER, "integer", 5, 9),
            (TokenType.SEMI, ";", 5, 16),
            (TokenType.BEGIN, "begin", 6, 1),
            (TokenType.ID, "x", 7, 4),
            (TokenType.ASSIGN, ":=", 7, 6),
            (TokenType.LPAR, "(", 7, 9),
            (TokenType.ID, "a", 7, 10),
            (TokenType.PLUS, "+", 7, 12),
            (TokenType.ID, "b", 7, 14),
            (TokenType.RPAR, ")", 7, 16),
            (TokenType.MULTIPLY, "*", 7, 18),
            (TokenType.INTEGER_LITERAL, 2, 7, 20),
            (TokenType.SEMI, ";", 7, 21),
            (TokenType.END, "end", 8, 1),
            (TokenType.SEMI, ";", 8, 4),
            (TokenType.PROCEDURE, "procedure", 10, 1),
            (TokenType.ID, "beta", 10, 11),
            (TokenType.SEMI, ";", 10, 15),
            (TokenType.VAR, "var", 11, 1),
            (TokenType.ID, "x", 11, 5),
            (TokenType.COLON, ":", 11, 7),
            (TokenType.REAL, "real", 11, 9),
            (TokenType.SEMI, ";", 11, 13),
            (TokenType.BEGIN, "begin", 12, 1),
            (TokenType.ID, "x", 13, 3),
            (TokenType.ASSIGN, ":=", 13, 5),
            (TokenType.REAL_LITERAL, 9.1, 13, 8),
            (TokenType.PLUS, "+", 13, 12),
            (TokenType.REAL_LITERAL, 4.3, 13, 14),
            (TokenType.SEMI, ";", 13, 17),
            (TokenType.END, "end", 14, 1),
            (TokenType.SEMI, ";", 14, 4),
            (TokenType.BEGIN, "begin", 16, 1),
            (TokenType.ID, "alpha", 18, 3),
            (TokenType.LPAR, "(", 18, 8),
            (TokenType.INTEGER_LITERAL, 3, 18, 9),
            (TokenType.PLUS, "+", 18, 11),
            (TokenType.INTEGER_LITERAL, 5, 18, 13),
            (TokenType.COMMA, ",", 18, 14),
            (TokenType.INTEGER_LITERAL, 7, 18, 16),
            (TokenType.RPAR, ")", 18, 17),
            (TokenType.SEMI, ";", 18, 18),
            (TokenType.ID, "beta", 19, 3),
            (TokenType.LPAR, "(", 19, 7),
            (TokenType.RPAR, ")", 19, 8),
            (TokenType.SEMI, ";", 19, 9),
            (TokenType.END, "end", 20, 1),
            (TokenType.DOT, ".", 20, 4),
        )
        with open("test/data/part16.pas") as pas_file:
            self._test_extended_lexer(
                text=pas_file.read(), expected_data=expected_data
            )

    def _check_token(
            self,
            token,
            expected_type,
            expected_value,
            expected_line=None,
            expected_column=None
    ):
        self.assertEqual(
            token.get_type(),
            expected_type,
            f"{token}\nExpected types are not equal."
        )
        self.assertEqual(
            token.get_value(),
            expected_value,
            f"{token}\nExpected token values are not equal."
        )
        if expected_line is not None:
            self.assertEqual(
                token.get_line_number(),
                expected_line,
                f"{token}\nExpected token lines are not equal."
            )
        if expected_column is not None:
            self.assertEqual(
                token.get_column(),
                expected_column,
                f"{token}\nExpected token columns are not equal."
            )

    def _test_lexer(self, text, types_and_values):
        lexer = _make_lexer(text)
        for t, v in types_and_values:
            self._check_token(
                token=lexer.get_next_token(),
                expected_type=t,
                expected_value=v
            )

    def _test_extended_lexer(self, text, expected_data):
        lexer = _make_lexer(text)
        for exp_type, exp_value, exp_line, exp_column in expected_data:
            self._check_token(
                token=lexer.get_next_token(),
                expected_type=exp_type,
                expected_value=exp_value,
                expected_column=exp_column,
                expected_line=exp_line
            )
