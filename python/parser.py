
from ast import BinaryOperation
from ast import Number
from lexer import INTEGER
from lexer import LPAR
from lexer import RPAR
from lexer import MULTIPLY
from lexer import DIVIDE
from lexer import PLUS
from lexer import MINUS


class Parser:
    def __init__(self, lexer):
        self._lexer = lexer

        # Set current token to the first token from the input
        self._current_token = self._lexer.get_next_token()

    def parse(self):
        return self._expr()

    def _expr(self):
        """
        Process expr production.

        expr    : operand ((PLUS | MINUS) opeand)*
        operand : factor ((MULTIPLY | DIVIDE) factor)*
        factor  : INTEGER | LPAR expr RPAR
        """

        node = self._operand()

        while self._current_token.get_type() in (PLUS, MINUS):
            token = self._current_token
            if token.get_type() == PLUS:
                self._eat(PLUS)
            elif token.get_type() == MINUS:
                self._eat(MINUS)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self._operand())
        return node

    def _operand(self):
        """
        Process operand production.

        operand : factor ((MULTIPLY | DIVIDE) factor)*
        factor  : INTEGER | LPAR expr RPAR
        """

        node = self._factor()

        while self._current_token.get_type() in (MULTIPLY, DIVIDE):
            token = self._current_token
            if token.get_type() == MULTIPLY:
                self._eat(MULTIPLY)
            elif token.get_type() == DIVIDE:
                self._eat(DIVIDE)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self._factor())
        return node

    def _factor(self):
        """
        Process factor prodution.

        factor  : INTEGER | LPAR expr RPAR
        """
        token = self._current_token
        if token.get_type() == INTEGER:
            self._eat(INTEGER)
            return Number(token)
        elif token.get_type() == LPAR:
            self._eat(LPAR)
            node = self._expr()
            self._eat(RPAR)
            return node
        self._error()

    def _eat(self, token_type):
        """
        'Eats' current token if it is of expected type.

        Compare the current token type with the passed token
        type and if they match then "eat" the current token
        and assign the next token to the self._current_token,
        otherwise raise an exception.
        """

        if self._current_token.get_type() == token_type:
            self._current_token = self._lexer.get_next_token()
        else:
            self._error()

    def _error(self):
        raise Exception("Invalid syntax")
