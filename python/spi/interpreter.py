from spi.token import TokenType
from spi.node_visitor import NodeVisitor
from spi.semantic_analyzer import SemanticAnalyzer


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self._parser = parser
        self._semantic_analyzer = SemanticAnalyzer(parser)
        self.GLOBAL_SCOPE = dict()

    def execute(self):
        """
        Executes the arithmetic expression.

        Input: 42 * (3 + 4 * (12 - 3)) - (256 - 128 - 16 - 8 - 4) * (8 + 2)
        Expected output: 638
        (At this point integer and float division work the same way).
        """
        self._semantic_analyzer.analyze()
        tree = self._parser.parse()
        return self._visit(tree)

    def _visit_ProcedureDeclaration(self, node):
        pass

    def _visit_Program(self, node):
        self._visit(node.block)

    def _visit_Block(self, node):
        for decl in node.declarations:
            self._visit(decl)
        self._visit(node.compound_statement)

    def _visit_VarDeclaration(self, node):
        # Do nothing
        pass

    def _visit_Type(self, node):
        # Do nothing
        pass

    def _visit_BinaryOperation(self, node):
        if node.op.get_type() == TokenType.PLUS:
            return self._visit(node.left) + self._visit(node.right)
        elif node.op.get_type() == TokenType.MINUS:
            return self._visit(node.left) - self._visit(node.right)
        elif node.op.get_type() == TokenType.MULTIPLY:
            return self._visit(node.left) * self._visit(node.right)
        elif node.op.get_type() == TokenType.INTEGER_DIV:
            return self._visit(node.left) // self._visit(node.right)
        elif node.op.get_type() == TokenType.REAL_DIV:
            return self._visit(node.left) / self._visit(node.right)
        else:
            self._error()

    def _visit_Number(self, node):
        return node.value

    def _visit_UnaryOperation(self, node):
        val = self._visit(node.right)
        if node.op.get_type() == TokenType.MINUS:
            return -val
        return val

    def _visit_Compound(self, node):
        for child in node.children:
            self._visit(child)

    def _visit_NoOp(self, node):
        pass

    def _visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self._visit(node.right)

    def _visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def _error(self):
        raise Exception("Incorrect parse tree.")
