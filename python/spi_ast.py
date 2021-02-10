
class Ast:
    pass


class Program(Ast):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(Ast):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDeclaration(Ast):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(Ast):
    def __init__(self, token):
        self.token = token

    @property
    def value(self):
        return self.token.get_value()


class BinaryOperation(Ast):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOperation(Ast):
    def __init__(self, op, right):
        self.op = op
        self.right = right


class Number(Ast):
    def __init__(self, token):
        self.token = token

    @property
    def value(self):
        return self.token.get_value()


class Compound(Ast):
    def __init__(self):
        self.children = []


class Assign(Ast):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Var(Ast):
    def __init__(self, token):
        self.token = token

    @property
    def value(self):
        return self.token.get_value()


class NoOp(Ast):
    pass
