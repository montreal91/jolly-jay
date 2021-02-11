
from node_visitor import NodeVisitor
from symbol import SymbolTable
from symbol import BuiltinTypeSymbol
from symbol import VarSymbol


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, parser):
        self._symtab = SymbolTable()
        self._parser = parser

    @property
    def symtab(self):
        return self._symtab

    def analyze(self):
        tree = self._parser.parse()
        self._visit(tree)

    def _visit_Block(self, node):
        for dec in node.declarations:
            self._visit(dec)
        self._visit(node.compound_statement)

    def _visit_ProcedureDeclaration(self, node):
        pass

    def _visit_Program(self, node):
        self._visit(node.block)

    def _visit_BinaryOperation(self, node):
        self._visit(node.left)
        self._visit(node.right)

    def _visit_Number(self, node):
        pass

    def _visit_UnaryOperation(self, node):
        self._visit(node.right)

    def _visit_Compound(self, node):
        for child in node.children:
            self._visit(child)

    def _visit_NoOp(self, node):
        pass

    def _visit_VarDeclaration(self, node):
        type_name = node.type_node.value
        type_symbol = self._symtab.lookup(type_name)
        var_name = node.var_node.value
        if self._symtab.lookup(var_name) != None:
            raise PascalDuplicateIdentifier(
                "Error: Duplicate identifier '%s' found" % var_name
            )
        self._symtab.define(VarSymbol(var_name, type_symbol))

    def _visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self._symtab.lookup(var_name)
        if var_symbol is None:
            raise PascalNameError(var_name)

        self._visit(node.right)

    def _visit_Var(self, node):
        var_name = node.value
        var_symbol = self._symtab.lookup(var_name)

        if var_symbol is None:
            raise PascalNameError(var_name)


class PascalError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PascalNameError(PascalError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PascalDuplicateIdentifier(PascalNameError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
