
from math import isclose
from unittest import TestCase
from unittest import skip

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class ProgramTc(TestCase):
    def test_part10(self):
        with open("test/data/part10.pas") as source_file:
            spi = _make_interpreter(text=source_file.read())
            spi.execute()
            self.assertEqual(spi.GLOBAL_SCOPE["a"], 2)
            self.assertEqual(spi.GLOBAL_SCOPE["b"], 25)
            self.assertEqual(spi.GLOBAL_SCOPE["c"], 27)
            self.assertEqual(spi.GLOBAL_SCOPE["number"], 2)
            self.assertEqual(spi.GLOBAL_SCOPE["x"], 11)
            self.assertTrue(isclose(spi.GLOBAL_SCOPE["y"], 5.99714285714))

    def test_empty(self):
        with open("test/data/empty.pas") as source_file:
            spi = _make_interpreter(text=source_file.read())
            spi.execute()
            self.assertEqual(len(spi.GLOBAL_SCOPE), 0)


def _make_interpreter(text):
    return Interpreter(parser=Parser(lexer=Lexer(text=text)))
