
# from lexer import PLUS
# from lexer import MINUS
# from lexer import MULTIPLY
# from lexer import DIVIDE

from lexer import TokenType


class NodeVisitor:
    def _visit(self, node):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method.")


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self._parser = parser
        self.GLOBAL_SCOPE = dict()

    def execute(self):
        """
        Executes the arithmetic expression.

        Input: 42 * (3 + 4 * (12 - 3)) - (256 - 128 - 16 - 8 - 4) * (8 + 2)
        Expected ouptut: 638
        """
        tree = self._parser.parse()
        return self._visit(tree)

    def _visit_BinaryOperation(self, node):
        if node.op.get_type() == TokenType.PLUS:
            return self._visit(node.left) + self._visit(node.right)
        elif node.op.get_type() == TokenType.MINUS:
            return self._visit(node.left) - self._visit(node.right)
        elif node.op.get_type() == TokenType.MULTIPLY:
            return self._visit(node.left) * self._visit(node.right)
        elif node.op.get_type() == TokenType.DIVIDE:
            return self._visit(node.left) // self._visit(node.right)
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
