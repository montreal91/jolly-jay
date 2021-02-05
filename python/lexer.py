
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
LPAR = "LPAR"
RPAR = "RPAR"

ID = "ID"
ASSIGN = "ASSIGN"
SEMI = "SEMI"
DOT = "DOT"

EOF = "EOF"

OPERATORS = {
    "+": PLUS,
    "-": MINUS,
    "*": MULTIPLY,
    "/": DIVIDE,
}



class Token:
    def __init__(self, type_, value):
        self._type = type_
        self._value = value

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def __str__(self):
        return f"Token({self._type}, {self._value})"

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    "BEGIN": Token("BEGIN", "BEGIN"),
    "END": Token("END", "END"),
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
        if not self._has_more():
            return Token(EOF, None)

        current_char = self._get_current_char()

        if current_char.isdigit():
            return self._read_integer_token()

        if current_char in OPERATORS:
            return self._read_operator_token()

        if current_char == "(":
            token = Token(LPAR, "(")
            self._next_char()
            return token

        if current_char == ")":
            token = Token(RPAR, ")")
            self._next_char()
            return token

        if self._get_current_char().isalpha():
            return self._read_id_token()

        if self._get_current_char() == ":" and self._peek() == "=":
            self._next_char()
            self._next_char()
            return Token(ASSIGN, ":=")

        if self._get_current_char() == ";":
            self._next_char()
            return Token(SEMI, ";")

        if self._get_current_char() == ".":
            self._next_char()
            return Token(DOT, ".")

        self._throw_error()

    def _skip_whitespace(self):
        while self._has_more() and self._get_current_char().isspace():
            self._next_char()

    def _read_integer_token(self):
        val = ""
        while self._has_more() and self._get_current_char().isdigit():
            val += self._get_current_char()
            self._next_char()
        return Token(INTEGER, int(val))

    def _read_id_token(self):
        val = ""
        while self._has_more() and self._get_current_char().isalnum():
            val += self._get_current_char()
            self._next_char()
        token = RESERVED_KEYWORDS.get(val, Token(ID, val))
        return token

    def _read_operator_token(self):
        t = Token(
            OPERATORS[self._get_current_char()],
            self._get_current_char()
        )
        self._next_char()
        return t

    def _get_current_char(self):
        if self._pos < len(self._text):
            return self._text[self._pos]
        return None

    def _next_char(self):
        self._pos += 1

    def _has_more(self):
        return self._pos < len(self._text)

    def _peek(self):
        pp = self._pos + 1
        if pp < len(self._text):
            return self._text[pp]
        return None

    def _throw_error(self):
        raise Exception("Unexpected character")
