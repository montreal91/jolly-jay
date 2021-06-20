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
    PROCEDURE = "PROCEDURE"
    PROGRAM = "PROGRAM"
    REAL = "REAL"
    REAL_DIV = "REAL_DIV"
    REAL_LITERAL = "REAL_LITERAL"
    RPAR = "RPAR"
    SEMI = "SEMI"
    VAR = "VAR"

    EOF = "EOF"


class Token:
    def __init__(self, type_, value, line_number=None, column=None):
        self._type = type_
        self._value = value
        self._line_number = line_number
        self._column = column

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def get_line_number(self):
        return self._line_number

    def get_column(self):
        return self._column

    def __str__(self):
        return (
            f"Token({self._type.value}, {self._value}, position={self._line_number}:{self._column})"
        )

    def __repr__(self):
        return self.__str__()


# Maps token symbol to the token type
ONE_SYMBOL_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.REAL_DIV,
    "(": TokenType.LPAR,
    ")": TokenType.RPAR,
    ";": TokenType.SEMI,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
}

# Maps token word to the token type
RESERVED_KEYWORDS = {
    "program": TokenType.PROGRAM,
    "procedure": TokenType.PROCEDURE,
    "var": TokenType.VAR,
    "integer": TokenType.INTEGER,
    "real": TokenType.REAL,
    "begin": TokenType.BEGIN,
    "end": TokenType.END,
    "div": TokenType.INTEGER_DIV,
}