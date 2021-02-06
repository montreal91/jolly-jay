
# from lexer import ASSIGN
# from lexer import BEGIN
# from lexer import END
# from lexer import DIVIDE
# from lexer import DOT
# from lexer import EOF
# from lexer import ID
# from lexer import INTEGER
# from lexer import LPAR
# from lexer import MINUS
# from lexer import MULTIPLY
# from lexer import PLUS
# from lexer import RPAR
# from lexer import SEMI
from lexer import TokenType
from spi_ast import Assign
from spi_ast import Compound
from spi_ast import BinaryOperation
from spi_ast import NoOp
from spi_ast import Number
from spi_ast import Var
from spi_ast import UnaryOperation


class Parser:
    def __init__(self, lexer):
        self._lexer = lexer

        # Set current token to the first token from the input
        self._current_token = self._lexer.get_next_token()

    def parse(self):
        node = self._program()
        if self._current_token.get_type() != TokenType.EOF:
            self._error()
        return node

    def _program(self):
        """
        program : compound_statement DOT
        """

        node = self._compound_statement()
        self._eat(TokenType.DOT)
        return node

    def _compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self._eat(TokenType.BEGIN)
        nodes = self._statement_list()
        self._eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def _statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self._statement()
        results = [node]

        while self._current_token.get_type() == TokenType.SEMI:
            self._eat(TokenType.SEMI)
            results.append(self._statement())

        if self._current_token.get_type() == TokenType.ID:
            self._error()

        return results

    def _statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  |  empty
        """

        if self._current_token.get_type() == TokenType.BEGIN:
            node = self._compound_statement()
        elif self._current_token.get_type() == TokenType.ID:
            node = self._assignment_statement()
        else:
            node = self._empty()
        return node

    def _assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self._variable()
        token = self._current_token
        self._eat(TokenType.ASSIGN)
        right = self._expr()
        return Assign(left=left, op=token, right=right)

    def _variable(self):
        """
        variable : ID
        """
        node = Var(self._current_token)
        self._eat(TokenType.ID)
        return node

    def _empty(self):
        """
        An empty production.
        """
        return NoOp()

    def _expr(self):
        """
        Process expr production.

        expr    : operand ((PLUS | MINUS) opeand)*
        """

        node = self._operand()

        while self._current_token.get_type() in (TokenType.PLUS, TokenType.MINUS):
            token = self._current_token
            if token.get_type() == TokenType.PLUS:
                self._eat(TokenType.PLUS)
            elif token.get_type() == TokenType.MINUS:
                self._eat(TokenType.MINUS)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self._operand())
        return node

    def _operand(self):
        """
        Process operand production.

        operand : factor ((MULTIPLY | DIVIDE) factor)*
        """

        node = self._factor()

        while self._current_token.get_type() in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self._current_token
            if token.get_type() == TokenType.MULTIPLY:
                self._eat(TokenType.MULTIPLY)
            elif token.get_type() == TokenType.DIVIDE:
                self._eat(TokenType.DIVIDE)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self._factor())
        return node

    def _factor(self):
        """
        Process factor prodution.

        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAR expr RPAR
               | variable
        """
        token = self._current_token
        if token.get_type() in (TokenType.PLUS, TokenType.MINUS):
            self._eat(token.get_type())
            return UnaryOperation(op=token, right=self._factor())
        elif token.get_type() == TokenType.INTEGER:
            self._eat(TokenType.INTEGER)
            return Number(token)
        elif token.get_type() == TokenType.LPAR:
            self._eat(TokenType.LPAR)
            node = self._expr()
            self._eat(TokenType.RPAR)
            return node
        elif token.get_type() == TokenType.ID:
            # ???
            return self._variable()
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
