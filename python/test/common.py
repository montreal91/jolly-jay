from spi.interpreter import Interpreter
from spi.lexer import Lexer
from spi.parser import Parser


def _make_interpreter(text):
    return Interpreter(parser=Parser(lexer=Lexer(text=text)))
