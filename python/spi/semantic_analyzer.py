from spi.errors import SemanticError, ErrorCode
from spi.node_visitor import NodeVisitor
from spi.symbol import ProcedureSymbol
from spi.symbol import ScopedSymbolTable
from spi.symbol import VarSymbol


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

    def _throw_error(self, error_code, token):
        raise SemanticError(
            error_code=error_code,
            token=token,
            message=f"{error_code.value} -> {token}"
        )

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
            scope_level=self._scope.scope_level + 1,
            enclosing_scope=self._scope
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
        self._scope = self._scope.enclosing_scope


    def _visit_Program(self, node):
        global_scope = ScopedSymbolTable(
            scope_name="Global",
            scope_level=1,
            enclosing_scope=self._scope
        )
        self._scope = global_scope
        self._visit(node.block)
        self._scope = global_scope

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
        if self._scope.lookup(name=var_name, go_deep=False) is not None:
            self._throw_error(
                error_code=ErrorCode.DUPLICATE_ID,
                token=node.var_node.token
            )

        self._scope.insert(VarSymbol(var_name, type_symbol))

    def _visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self._scope.lookup(var_name)
        if var_symbol is None:
            self._throw_error(
                error_code=ErrorCode.ID_NOT_FOUND,
                token=node.token
            )

        self._visit(node.right)

    def _visit_Var(self, node):
        var_name = node.value
        var_symbol = self._scope.lookup(var_name)

        if var_symbol is None:
            self._throw_error(
                error_code=ErrorCode.ID_NOT_FOUND,
                token=node.token
            )
