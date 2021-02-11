
from lexer import TokenType
from spi_ast import Assign
from spi_ast import Block
from spi_ast import Compound
from spi_ast import BinaryOperation
from spi_ast import NoOp
from spi_ast import Number
from spi_ast import ProcedureDeclaration
from spi_ast import Program
from spi_ast import Var
from spi_ast import VarDeclaration
from spi_ast import Type
from spi_ast import UnaryOperation


class Parser:
    def __init__(self, lexer):
        self._lexer = lexer
        self._parse_tree = None

        # Set current token to the first token from the input
        self._current_token = self._lexer.get_next_token()

    def parse(self):
        if self._parse_tree is not None:
            return self._parse_tree

        self._parse_tree = self._program()
        if self._current_token.get_type() != TokenType.EOF:
            self._error()
        return self._parse_tree

    def _program(self):
        """
        program : PROGRAM variable SEMI block DOT
        """
        self._eat(TokenType.PROGRAM)
        var_node = self._variable()
        prog_name = var_node.value
        self._eat(TokenType.SEMI)
        block_node = self._block()
        program_node = Program(name=prog_name, block=block_node)
        self._eat(TokenType.DOT)
        return program_node

    def _block(self):
        """
        block : declarations compound_statement
        """
        declaration_nodes = self._declarations()
        compound_statement_node = self._compound_statement()
        return Block(
            declarations=declaration_nodes,
            compound_statement=compound_statement_node
        )

    def _declarations(self):
        """
        declararions : VAR (variable_declaration SEMI)+
                     | (PROCEDURE ID SEMI block SEMI)*
                     | empty
        """
        declarations = []
        if self._current_token.get_type() == TokenType.VAR:
            self._eat(TokenType.VAR)
            while self._current_token.get_type() == TokenType.ID:
                var_decl = self._variable_declaration()
                declarations.extend(var_decl)
                self._eat(TokenType.SEMI)

        while self._current_token.get_type() == TokenType.PROCEDURE:
            self._eat(TokenType.PROCEDURE)
            proc_name = self._current_token.get_value()
            self._eat(TokenType.ID)
            self._eat(TokenType.SEMI)
            block_node = self._block()
            proc_decl = ProcedureDeclaration(proc_name, block_node)
            declarations.append(proc_decl)
            self._eat(TokenType.SEMI)
        return declarations

    def _variable_declaration(self):
        """
        variable_declaration : ID (COMMA ID)* COLON type_spec
        """
        var_nodes = [Var(self._current_token)] # first ID
        self._eat(TokenType.ID)

        while self._current_token.get_type() == TokenType.COMMA:
            self._eat(TokenType.COMMA)
            var_nodes.append(Var(self._current_token))
            self._eat(TokenType.ID)

        self._eat(TokenType.COLON)
        type_node = self._type_spec()
        return tuple(
            VarDeclaration(var_node, type_node) for var_node in var_nodes
        )

    def _type_spec(self):
        """
        type_spec : INTEGER | REAL
        """
        token = self._current_token
        if self._current_token.get_type() == TokenType.INTEGER:
            self._eat(TokenType.INTEGER)
        elif self._current_token.get_type() == TokenType.REAL:
            self._eat(TokenType.REAL)
        else:
            self._error()

        return Type(token)

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

        operand : factor ((MULTIPLY | INTEGER_DIV | REAL_DIV) factor)*
        """

        node = self._factor()

        types = (TokenType.MULTIPLY, TokenType.INTEGER_DIV, TokenType.REAL_DIV)
        while self._current_token.get_type() in (types):
            token = self._current_token
            if token.get_type() == TokenType.MULTIPLY:
                self._eat(TokenType.MULTIPLY)
            elif token.get_type() == TokenType.INTEGER_DIV:
                self._eat(TokenType.INTEGER_DIV)
            elif token.get_type() == TokenType.REAL_DIV:
                self._eat(TokenType.REAL_DIV)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self._factor())
        return node

    def _factor(self):
        """
        Process factor prodution.

        factor : PLUS factor
               | MINUS factor
               | INTEGER_LITERAL
               | REAL_LITERAL
               | LPAR expr RPAR
               | variable
        """
        token = self._current_token
        if token.get_type() in (TokenType.PLUS, TokenType.MINUS):
            self._eat(token.get_type())
            return UnaryOperation(op=token, right=self._factor())
        elif token.get_type() == TokenType.INTEGER_LITERAL:
            self._eat(TokenType.INTEGER_LITERAL)
            return Number(token)
        elif token.get_type() == TokenType.REAL_LITERAL:
            self._eat(TokenType.REAL_LITERAL)
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
