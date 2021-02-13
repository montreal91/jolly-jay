
from node_visitor import NodeVisitor
from parser import Parser
from lexer import Lexer
from symbol import ProcedureSymbol
from symbol import ScopedSymbolTable
from symbol import VarSymbol


class SourceToSourceCompiler(NodeVisitor):
    def __init__(self, parser):
        self._lines = []
        self._parser = parser
        self._scope = None

    def compile(self):
        tree = self._parser.parse()
        self._visit(tree)
        return "\n".join(self._lines)

    def _visit_Program(self, node):
        global_scope = ScopedSymbolTable(
            scope_name="Global",
            scope_level=1,
            enclosing_scope=self._scope
        )

        self._scope = global_scope
        self._lines.append(f"PROGRAM {node.name}0;")
        self._visit(node.block)
        self._lines.append("END. {END of %s}" % node.name)

    def _visit_Block(self, node):
        for dec in node.declarations:
            self._visit(dec)
        self._lines.append("    " * (self._scope.scope_level - 1) + "BEGIN")
        self._visit(node.compound_statement)
        if self._scope.scope_level != 1:
            self._lines.append(
                "    " * (self._scope.scope_level - 1) +
                "END; {END of " +
                self._scope.scope_name +
                "}"
            )

    def _visit_Compound(self, node):
        for child in node.children:
            self._visit(child)

    def _visit_VarDeclaration(self, node):
        var_name = node.var_node.value
        type_symbol = self._scope.lookup(node.type_node.value)
        if self._scope.lookup(name=var_name, go_deep=False) is not None:
            raise PascalDuplicateIdentifier(
                f"Error: Duplicate identifier '{var_name}' is found."
            )
        var_symbol = VarSymbol(var_name, type_symbol)
        self._scope.insert(VarSymbol(var_name, type_symbol))
        self._lines.append(
            "    " * self._scope.scope_level +
            f"VAR {var_name}{self._scope.scope_level}: {var_symbol.get_type()};"
        )

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

        for param in node.params:
            param_type = self._scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            var_symbol = VarSymbol(param_name, param_type)
            self._scope.insert(var_symbol)
            proc_symbol.params.append(var_symbol)

        self._lines.append(self._proc_symbol_to_string(proc_symbol))
        self._visit(node.block_node)
        self._scope = self._scope.enclosing_scope

    def _visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self._scope.lookup(var_name)
        if var_symbol is None:
            raise PascalNameError(var_name)

        tab = "    " * self._scope.scope_level
        left = f"<{var_name}{self._scope.scope_level}:{var_symbol.get_type()}>"
        right = self._visit(node.right)
        self._lines.append(tab + f"{left} := {right};")

    def _visit_BinaryOperation(self, node):
        left = self._visit(node.left)
        right = self._visit(node.right)
        return f"{left} {node.op.get_value()} {right}"

    def _visit_Var(self, node):
        var_name = node.value
        var_symbol = self._scope.lookup(var_name)
        return f"<{var_name}{self._scope.scope_level}:{var_symbol.get_type()}>"

    def _visit_NoOp(self, node):
        pass


    def _proc_symbol_to_string(self, symbol):
        level = self._scope.scope_level
        tab = "    " * (level - 1)
        proc = f"PROCEDURE {symbol.get_name()}{level}("
        varz = ", ".join(
            f"{s.get_name()}{level}: {s.get_type()}" for s in symbol.params
        )
        return tab + proc + varz + ");"


def _make_compiler(filename):
    with open(filename) as source:
        return SourceToSourceCompiler(
            parser=Parser(lexer=Lexer(text=source.read()))
        )


if __name__ == "__main__":
    import sys
    s2s = _make_compiler(sys.argv[1])
    print(s2s.compile())
