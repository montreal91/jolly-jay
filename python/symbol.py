
from node_visitor import NodeVisitor


class Symbol:
    def __init__(self, name, the_type=None):
        self._name = name
        self._type = the_type

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self._name

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, the_type):
        super().__init__(name, the_type)

    def __str__(self):
        return f"<{self._name}:{self._type}>"

    __repr__ = __str__


class SymbolTable:
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def __str__(self):
        s = "Symbols: {symbols}".format(
            symbols=[val for val in self._symbols.values()]
        )

    __repr__ = __str__

    def define(self, symbol):
        self._symbols[symbol.get_name()] = symbol

    def lookup(self, name):
        return self._symbols.get(name)

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol("INTEGER"))
        self.define(BuiltinTypeSymbol("REAL"))


class SymbolTableBuilder(NodeVisitor):
    def __init__(self, parser):
        self._symtab = SymbolTable()
        self._parser = parser

    @property
    def symtab(self):
        return self._symtab

    def build(self):
        tree = self._parser.parse()
        self._visit(tree)

    def _visit_Block(self, node):
        for dec in node.declarations:
            self._visit(dec)
        self._visit(node.compound_statement)

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
        self._symtab.define(VarSymbol(var_name, type_symbol))

    def _visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self._symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(var_name)

        self._visit(node.right)

    def _visit_Var(self, node):
        var_name = node.value
        var_symbol = self._symtab.lookup(var_name)

        if var_symbol is None:
            raise NameError(var_name)
