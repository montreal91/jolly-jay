
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
