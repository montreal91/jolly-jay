from spi.errors import ParserError, ErrorCode
from spi.token import TokenType
from spi.ast import Assign
from spi.ast import BinaryOperation
from spi.ast import Block
from spi.ast import Compound
from spi.ast import NoOp
from spi.ast import Number
from spi.ast import Param
from spi.ast import ProcedureCall
from spi.ast import ProcedureDeclaration
from spi.ast import Program
from spi.ast import Var
from spi.ast import VarDeclaration
from spi.ast import Type
from spi.ast import UnaryOperation


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
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self._current_token
            )
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
        declarations : (VAR (variable_declaration SEMI)+)?
                     | procedure_declaration*
                     | empty
        """
        declarations = []
        while self._current_token.get_type() == TokenType.VAR:
            self._eat(TokenType.VAR)
            while self._current_token.get_type() == TokenType.ID:
                var_decl = self._variable_declaration()
                declarations.extend(var_decl)
                self._eat(TokenType.SEMI)

        while self._current_token.get_type() == TokenType.PROCEDURE:
            declarations.append(self._procedure_declaration())
        return declarations

    def _procedure_declaration(self):
        """
        procedure_declaration :
            PROCEDURE ID (LPAR formal_parameter_list RPAR)? SEMI block SEMI
        """
        self._eat(TokenType.PROCEDURE)
        proc_name = self._current_token.get_value()
        self._eat(TokenType.ID)
        params = []
        if self._current_token.get_type() == TokenType.LPAR:
            self._eat(TokenType.LPAR)
            params = self._formal_parameter_list()
            self._eat(TokenType.RPAR)
        self._eat(TokenType.SEMI)
        block_node = self._block()
        proc_decl = ProcedureDeclaration(proc_name, params, block_node)
        self._eat(TokenType.SEMI)
        return proc_decl

    def _proccall_statement(self):
        """
        proccall_statement: ID LPAR (expr (COMMA expr)*)? RPAR
        """
        token = self._current_token

        proc_name = token.get_value()
        self._eat(TokenType.ID)
        self._eat(TokenType.LPAR)
        actual_params = []

        if self._current_token.get_type() != TokenType.RPAR:
            node = self._expr()
            actual_params.append(node)

        while self._current_token.get_type() == TokenType.COMMA:
            self._eat(TokenType.COMMA)
            node = self._expr()
            actual_params.append(node)

        self._eat(TokenType.RPAR)

        return ProcedureCall(
            proc_name=proc_name,
            actual_params=actual_params,
            token=token
        )

    def _formal_parameter_list(self):
        """
        formal_parameter_list : formal_parameters
                              | formal_parameters SEMI formal_parameter_list
        """
        parameters = self._formal_parameters()
        if self._current_token.get_type() == TokenType.SEMI:
            self._eat(TokenType.SEMI)
            parameters.extend(self._formal_parameter_list())
        return parameters

    def _formal_parameters(self):
        """
        formal_parameters : ID (COMMA ID)* COLON type_spec
        """
        param_nodes = [Var(self._current_token)]
        self._eat(TokenType.ID)
        while self._current_token.get_type() == TokenType.COMMA:
            self._eat(TokenType.COMMA)

            param_nodes.append(Var(self._current_token))
            self._eat(TokenType.ID)

        self._eat(TokenType.COLON)
        type_node = self._type_spec()
        return [
            Param(var_node, type_node) for var_node in param_nodes
        ]

    def _variable_declaration(self):
        """
        variable_declaration : ID (COMMA ID)* COLON type_spec
        """
        var_nodes = [Var(self._current_token)]  # first ID
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
            self._error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=token)

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
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self._current_token
            )

        return results

    def _statement(self):
        """
        statement : compound_statement
                  | proccall_statement
                  | assignment_statement
                  | empty
        """

        if self._current_token.get_type() == TokenType.BEGIN:
            node = self._compound_statement()
        elif self._current_token.get_type() == TokenType.ID:
            if self._lexer.get_current_char() == '(':
                node = self._proccall_statement()
            else:
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

    @staticmethod
    def _empty():
        """
        An empty production.
        """
        return NoOp()

    def _expr(self):
        """
        Process expr production.

        expr    : operand ((PLUS | MINUS) operand)*
        """

        node = self._operand()

        while self._current_token.get_type() in (TokenType.PLUS, TokenType.MINUS):
            token = self._current_token
            if token.get_type() == TokenType.PLUS:
                self._eat(TokenType.PLUS)
            elif token.get_type() == TokenType.MINUS:
                self._eat(TokenType.MINUS)
            else:
                self._error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=token)

            node = BinaryOperation(left=node, op=token, right=self._operand())
        return node

    def _operand(self):
        """
        Process operand production.

        operand : factor ((MULTIPLY | INTEGER_DIV | REAL_DIV) factor)*
        """

        node = self._factor()

        types = (TokenType.MULTIPLY, TokenType.INTEGER_DIV, TokenType.REAL_DIV)
        while self._current_token.get_type() in types:
            token = self._current_token
            if token.get_type() == TokenType.MULTIPLY:
                self._eat(TokenType.MULTIPLY)
            elif token.get_type() == TokenType.INTEGER_DIV:
                self._eat(TokenType.INTEGER_DIV)
            elif token.get_type() == TokenType.REAL_DIV:
                self._eat(TokenType.REAL_DIV)
            else:
                self._error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=token)

            node = BinaryOperation(left=node, op=token, right=self._factor())
        return node

    def _factor(self):
        """
        Process factor production.

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
        self._error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=token)

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
            print(
                f"expected type was {token_type} "
                f"got {self._current_token.get_type()}"
            )
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self._current_token
            )

    def _error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f"{error_code.value} -> {token}",
        )
