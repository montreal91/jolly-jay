
from node_visitor import NodeVisitor
from symbol import BuiltinTypeSymbol
from symbol import ProcedureSymbol
from symbol import ScopedSymbolTable
from symbol import VarSymbol


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, parser):
        self._scope = None
        self._parser = parser

    @property
    def scope(self):
        return self._scope

    def analyze(self):
        tree = self._parser.parse()
        self._visit(tree)

    def _visit_Block(self, node):
        for dec in node.declarations:
            self._visit(dec)
        self._visit(node.compound_statement)

    def _visit_ProcedureDeclaration(self, node):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        self._scope.insert(proc_symbol)

        procedure_scope = ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self._scope.scope_level + 1
        )
        self._scope = procedure_scope

        # Insert params into the procedure scope
        for param in node.params:
            param_type = self._scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self._scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self._visit(node.block_node)


    def _visit_Program(self, node):
        self._scope = ScopedSymbolTable(scope_name="Global", scope_level=1)
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
        type_symbol = self._scope.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        self._scope.insert(VarSymbol(var_name, type_symbol))

    def _visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self._scope.lookup(var_name)
        if var_symbol is None:
            raise PascalNameError(var_name)

        self._visit(node.right)

    def _visit_Var(self, node):
        var_name = node.value
        var_symbol = self._scope.lookup(var_name)

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
