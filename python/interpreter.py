
from lexer import PLUS
from lexer import MINUS
from lexer import MULTIPLY
from lexer import DIVIDE


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

    def execute(self):
        """
        Executes the arithmetic expression.

        Input: 42 * (3 + 4 * (12 - 3)) - (256 - 128 - 16 - 8 - 4) * (8 + 2)
        Expected ouptut: 638
        """
        tree = self._parser.parse()
        return self._visit(tree)

    def _visit_BinaryOperation(self, node):
        if node.op.get_type() == PLUS:
            return self._visit(node.left) + self._visit(node.right)
        elif node.op.get_type() == MINUS:
            return self._visit(node.left) - self._visit(node.right)
        elif node.op.get_type() == MULTIPLY:
            return self._visit(node.left) * self._visit(node.right)
        elif node.op.get_type() == DIVIDE:
            return self._visit(node.left) // self._visit(node.right)
        else:
            self._error()

    def _visit_Number(self, node):
        return node.value

    def _error(self):
        raise Exception("Incorrect parse tree.")
