# 2021.01.22

from lexer import Lexer

from lexer import (
    DIVIDE,
    INTEGER,
    MINUS,
    MULTIPLY,
    PLUS,
)

class Interpreter:
    def __init__(self, lexer):
        self._lexer = lexer
        self._current_token = self._lexer.get_next_token()


    def expr(self):
        """
        Arithmetic expression Parser/Interpreter.

        expr    : operand ((PLUS|MINUS) operand)
        operand : factor ((MULTIPLY | DIVIDE) factor)
        factor  : INTEGER
        """
        result = self._operand()
        while self._current_token.get_type() in (PLUS, MINUS):
            op = self._current_token
            if op.get_type() == PLUS:
                self._eat(PLUS)
                result += self._operand()
            elif op.get_type() == MINUS:
                self._eat(MINUS)
                result -= self._operand()
            else:
                self._throw_error()
        return result

    def _operand(self):
        """
        Operand Parser/Interpreter.

        operand : factor ((MULTIPLY | DIVIDE) factor)
        factor  : INTEGER
        """

        result = self._factor()
        while self._current_token.get_type() in (MULTIPLY, DIVIDE):
            op = self._current_token
            if op.get_type() == MULTIPLY:
                self._eat(MULTIPLY)
                result *= self._factor()
            elif op.get_type() == DIVIDE:
                self._eat(DIVIDE)
                result //= self._factor()
            else:
                self._throw_error()

        return result

    def _factor(self):
        """
        Return an INTEGER token value.

        factor : INTEGER
        """

        token = self._current_token
        self._eat(INTEGER)
        return token.get_value()

    def _throw_error(self):
        raise Exception("Error parsing input")

    def _eat(self, token_type):
        if self._current_token.get_type() == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self._throw_error()


def _evaluate(text):
    interpreter = Interpreter(Lexer(text))
    return interpreter.expr()


def main():
    print("Press Ctrl+C to quit.")
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print(
                "\n"
                "It is man's natural sickness "
                "to believe that he possesses the Truth."
                "\n"
            )

            break
        if not text:
            continue
        print(_evaluate(text))


if __name__ == "__main__":
    main()
