
from spi.interpreter import NodeVisitor
from spi.lexer import PLUS
from spi.lexer import MINUS
from spi.lexer import MULTIPLY
from spi.lexer import DIVIDE
from spi.lexer import Lexer
from parser import Parser


class ExprConverter(NodeVisitor):
    def __init__(self, parser):
        self._parser = parser

    def convert(self):
        tree = self._parser.parse()
        return self._visit(tree)


    def _visit_Number(self, node):
        return str(node.value)

    def _visit_BinaryOperation(self, node):
        left = self._visit(node.left)
        right = self._visit(node.right)
        if node.op.get_type() == PLUS:
            return f"(+ {left} {right})"
        elif node.op.get_type() == MINUS:
            return f"(- {left} {right})"
        elif node.op.get_type() == MULTIPLY:
            return f"(* {left} {right})"
        elif node.op.get_type() == DIVIDE:
            return f"(/ {left} {right})"
        else:
            self._error()

    def _error(self):
        raise Exception("Incorrect parse tree.")


def _convert(text):
    converter = ExprConverter(parser=Parser(lexer=Lexer(text=text)))
    return converter.convert()


def main():
    print("Press Ctrl+C to quit.")
    counter = 1
    while True:
        try:
            text = input(f"In [{counter}]: ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n")
            break
        if not text:
            continue
        print(f"Out[{counter}]: {_convert(text)}")
        counter += 1


if __name__ == "__main__":
    main()
