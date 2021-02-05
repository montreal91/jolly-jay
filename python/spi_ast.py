
class Ast:
    pass


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
