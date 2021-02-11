
class NodeVisitor:
    def _visit(self, node):
        method_name = "_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method.")
