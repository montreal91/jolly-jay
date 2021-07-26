
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


class ProcedureDeclaration(Ast):
    def __init__(self, proc_name, params, block_node):
        self.proc_name = proc_name
        self.params = params
        self.block_node = block_node

    def __str__(self):
        param_str = " ".join(str(param) for param in self.params)
        return f"Procedure {self.proc_name}({param_str})"

    __repr__ = __str__


class NoOp(Ast):
    pass


class Param(Ast):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

    def get_identifier(self):
        return self.var_node.value

    def __str__(self):
        return f"{self.var_node.value} : {self.type_node.value}"

    __repr__ = __str__


class ProcedureCall(Ast):
    def __init__(self, proc_name, actual_params, token):
        self.proc_name = proc_name
        self.actual_params = actual_params
        self.token = token
