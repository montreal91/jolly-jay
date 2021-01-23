# 2021.01.22

INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
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


class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def expr(self):
        self.current_token = self._get_next_token()

        left = self.current_token.get_value()
        self._eat(INTEGER)

        while self.current_token.get_type() != EOF:
            op = self.current_token
            if op.get_type() in OPERATORS.values():
                self._eat(op.get_type())
            else:
                self._throw_error()
            right = self.current_token
            self._eat(INTEGER)
            left = _calculate(
                left, op.get_type(), right.get_value()
            )
        return left

    def _throw_error(self):
        raise Exception("Error parsing input")

    def _get_next_token(self):
        """
        Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for braking a sentence apart into tokens.
        One token at a time.
        """
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        self._skip_whitespace()

        current_char = text[self.pos]

        if current_char.isdigit():
            return self._read_integer_token()

        if current_char in OPERATORS:
            return self._read_operator_token()

        self._throw_error()

    def _eat(self, token_type):
        if self.current_token.get_type() == token_type:
            self.current_token = self._get_next_token()
        else:
            self._throw_error()

    def _skip_whitespace(self):
        while self._get_current_char().isspace():
            self._next_char()

    def _read_integer_token(self):
        val = ""
        while self._has_more() and self._get_current_char().isdigit():
            val += self._get_current_char()
            self._next_char()
        return Token(INTEGER, int(val))

    def _read_operator_token(self):
        t = Token(
            OPERATORS[self._get_current_char()],
            self._get_current_char()
        )
        self._next_char()
        return t

    def _get_current_char(self):
        return self.text[self.pos]

    def _next_char(self):
        self.pos += 1

    def _has_more(self):
        return self.pos < len(self.text)


def _calculate(left, operator_type, right):
    if operator_type == PLUS:
        return left + right
    elif operator_type == MINUS:
        return left - right
    elif operator_type == MULTIPLY:
        return left * right
    elif operator_type == DIVIDE:
        return left // right
    Exception("Incorrect operator type.")


def main():
    print("Press Ctrl+C to quit.")
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print(
                "\nIt is man's natural sickness "
                "to believe that he possesses the Truth."
            )

            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
