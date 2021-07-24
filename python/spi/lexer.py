from spi.errors import LexerError
from spi.token import (
    TokenType,
    Token,
    ONE_SYMBOL_TOKENS,
    RESERVED_KEYWORDS
)


class Lexer:
    def __init__(self, text):
        self._text = text
        self._pos = 0

        self._line_number = 1
        self._column = 1

    def get_current_char(self):
        return self._text[self._pos]

    def get_next_token(self):
        """
        Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for braking a sentence apart into tokens.
        One token at a time.
        """

        self._skip_whitespace()

        while self._get_current_char() == "{":
            self._skip_comment()
        if not self._has_more():
            return Token(TokenType.EOF, None, None, None)

        current_char = self._get_current_char()

        if current_char.isdigit():
            return self._read_number_literal_token()

        if self._is_alpha_underscore():
            return self._read_alphanumeric_token()

        if self._get_current_char() == ":" and self._peek() == "=":
            self._advance()
            self._advance()
            return Token(
                TokenType.ASSIGN,
                ":=",
                line_number=self._line_number,
                column=self._column - 2
            )

        if current_char in ONE_SYMBOL_TOKENS:
            return self._read_operator_token()

        self._throw_error()

    def _skip_whitespace(self):
        while self._has_more() and self._get_current_char().isspace():
            self._advance()

    def _skip_comment(self):
        while self._has_more() and self._get_current_char() != "}":
            self._advance()
        self._advance()
        self._skip_whitespace()

    def _read_number_literal_token(self):
        val = ""
        while self._has_more() and self._get_current_char().isdigit():
            val += self._get_current_char()
            self._advance()

        if self._get_current_char() != ".":
            return Token(
                TokenType.INTEGER_LITERAL,
                int(val),
                line_number=self._line_number,
                column=self._column-len(val)
            )

        val += self._get_current_char()
        self._advance()
        while self._has_more() and self._get_current_char().isdigit():
            val += self._get_current_char()
            self._advance()
        return Token(
            TokenType.REAL_LITERAL,
            float(val),
            line_number=self._line_number,
            column=self._column - len(val)
        )

    def _read_alphanumeric_token(self):
        val = ""
        while self._has_more() and self._is_good_id_char():
            val += self._get_current_char()
            self._advance()
        token_type = RESERVED_KEYWORDS.get(val.lower(), TokenType.ID)
        return Token(
            type_=token_type,
            value=val.lower(),
            line_number=self._line_number,
            column=self._column - len(val)
        )

    def _read_operator_token(self):
        token_type = ONE_SYMBOL_TOKENS[self._get_current_char()]
        token = Token(
            type_=token_type,
            value=self._get_current_char(),
            line_number=self._line_number, column=self._column
        )
        self._advance()
        return token

    def _get_current_char(self):
        if self._pos < len(self._text):
            return self._text[self._pos]
        return None

    def _advance(self):
        if self._get_current_char() == "\n":
            self._line_number += 1
            self._column = 0

        self._pos += 1
        self._column += 1

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
        message = (
            f"Lexer error on '{self.get_current_char()}' "
            f"line: {self._line_number}, "
            f"column: {self._column}"
        )
        raise LexerError(message=message)
