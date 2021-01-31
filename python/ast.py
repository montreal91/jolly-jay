
class Ast:
    pass


class BinaryOperation(Ast):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number(Ast):
    def __init__(self, token):
        self.token = token

    @property
    def value(self):
        return self.token.get_value()
