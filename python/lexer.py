
from enum import Enum


class TokenType(Enum):
    ASSIGN = "ASSIGN"
    BEGIN = "BEGIN"
    COLON = "COLON"
    COMMA = "COMMA"
    DOT = "DOT"
    END = "END"
    ID = "ID"
    INTEGER = "INTEGER"
    INTEGER_DIV = "INT_DIV"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    LPAR = "LPAR"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    PLUS = "PLUS"
    PROGRAM = "PROGRAM"
    REAL = "REAL"
    REAL_DIV = "REAL_DIV"
    REAL_LITERAL = "REAL_LITERAL"
    RPAR = "RPAR"
    SEMI = "SEMI"
    VAR = "VAR"

    EOF = "EOF"




class Token:
    def __init__(self, type_, value):
        self._type = type_
        self._value = value

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def __str__(self):
        return f"Token({self._type.value()}, {self._value})"

    def __repr__(self):
        return self.__str__()


ONE_SYMBOL_TOKENS = {
    "+": Token(TokenType.PLUS, "+"),
    "-": Token(TokenType.MINUS, "-"),
    "*": Token(TokenType.MULTIPLY, "*"),
    "/": Token(TokenType.REAL_DIV, "/"),
    "(": Token(TokenType.LPAR, "("),
    ")": Token(TokenType.RPAR, ")"),
    ";": Token(TokenType.SEMI, ";"),
    ":": Token(TokenType.COLON, ":"),
    ",": Token(TokenType.COMMA, ","),
    ".": Token(TokenType.DOT, ".")
}


RESERVED_KEYWORDS = {
    "program": Token(TokenType.PROGRAM, "PROGRAM"),
    "var": Token(TokenType.VAR, "VAR"),
    "integer": Token(TokenType.INTEGER, "INTEGER"),
    "real": Token(TokenType.REAL, "REAL"),
    "begin": Token(TokenType.BEGIN, "BEGIN"),
    "end": Token(TokenType.END, "END"),
    "div": Token(TokenType.INTEGER_DIV, "DIV"),
}


class Lexer:
    def __init__(self, text):
        self._text = text
        self._pos = 0

    def get_next_token(self):
        """
        Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for braking a sentence apart into tokens.
        One token at a time.
        """

        self._skip_whitespace()

        if self._get_current_char() == "{":
            self._skip_comment()
        if not self._has_more():
            return Token(TokenType.EOF, None)

        current_char = self._get_current_char()

        if current_char.isdigit():
            return self._read_number_literal_token()

        if self._is_alpha_underscore():
            return self._read_alphanumeric_token()

        if self._get_current_char() == ":" and self._peek() == "=":
            self._next_char()
            self._next_char()
            return Token(TokenType.ASSIGN, ":=")

        if current_char in ONE_SYMBOL_TOKENS:
            return self._read_operator_token()

        self._throw_error()

    def _skip_whitespace(self):
        while self._has_more() and self._get_current_char().isspace():
            self._next_char()

    def _skip_comment(self):
        while self._has_more() and self._get_current_char() != "}":
            self._next_char()
        self._next_char()
        self._skip_whitespace()

    def _read_number_literal_token(self):
        val = ""
        while self._has_more() and self._get_current_char().isdigit():
            val += self._get_current_char()
            self._next_char()

        if self._get_current_char() != ".":
            return Token(TokenType.INTEGER_LITERAL, int(val))

        val += self._get_current_char()
        self._next_char()
        while self._has_more() and self._get_current_char().isdigit():
            val += self._get_current_char()
            self._next_char()
        return Token(TokenType.REAL_LITERAL, float(val))

    def _read_alphanumeric_token(self):
        val = ""
        while self._has_more() and self._is_good_id_char():
            val += self._get_current_char()
            self._next_char()
        val = val.lower()
        token = RESERVED_KEYWORDS.get(val, Token(TokenType.ID, val))
        return token

    def _read_operator_token(self):
        token = ONE_SYMBOL_TOKENS[self._get_current_char()]
        self._next_char()
        return token

    def _get_current_char(self):
        if self._pos < len(self._text):
            return self._text[self._pos]
        return None

    def _next_char(self):
        self._pos += 1

    def _has_more(self):
        return self._pos < len(self._text)

    def _is_alpha_underscore(self):
        if self._get_current_char().isalpha():
            return True
        return self._get_current_char() == "_"

    def _is_good_id_char(self):
        if self._get_current_char().isalnum():
            return True
        return self._get_current_char() == "_"

    def _peek(self):
        pp = self._pos + 1
        if pp < len(self._text):
            return self._text[pp]
        return None

    def _throw_error(self):
        raise Exception("Unexpected character")
