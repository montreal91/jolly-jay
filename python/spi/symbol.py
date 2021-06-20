
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


class ProcedureSymbol(Symbol):
    def __init__(self, name, params=None):
        super().__init__(name)
        self._type = BuiltinTypeSymbol("procedure")
        self.params = params
        if params is None:
            self.params = []

    def __str__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(name={self.name}, parameters={self.params})>"
        )

    __repr__ = __str__


class ScopedSymbolTable:
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._scope_name = scope_name
        self._scope_level = scope_level
        self._symbols = {}
        self._enclosing_scope = enclosing_scope
        self._init_builtins()

    @property
    def scope_name(self):
        return self._scope_name

    @property
    def scope_level(self):
        return self._scope_level

    @property
    def enclosing_scope(self):
        return self._enclosing_scope

    def __str__(self):
        s = "Symbols: {symbols}".format(
            symbols=[val for val in self._symbols.values()]
        )

    __repr__ = __str__

    def insert(self, symbol):
        self._symbols[symbol.get_name()] = symbol

    def lookup(self, name, go_deep=True):
        if not go_deep:
            return self._symbols.get(name)

        scope = self
        while scope is not None:
            got = scope._symbols.get(name)
            if got is not None:
                return got
            scope = scope.enclosing_scope
        return None

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol("integer"))
        self.insert(BuiltinTypeSymbol("real"))
