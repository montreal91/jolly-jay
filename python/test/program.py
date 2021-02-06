
from unittest import TestCase

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


class ProgramTc(TestCase):
    def test_program0(self):
        from test.data.programs import program0
        spi = _make_interpreter(text=program0)
        spi.execute()

        self.assertEqual(len(spi.GLOBAL_SCOPE), 0)

    def test_program1(self):
        from test.data.programs import program1
        spi = _make_interpreter(text=program1)
        spi.execute()

        self.assertEqual(spi.GLOBAL_SCOPE["a"], 2)
        self.assertEqual(spi.GLOBAL_SCOPE["b"], 25)
        self.assertEqual(spi.GLOBAL_SCOPE["c"], 27)
        self.assertEqual(spi.GLOBAL_SCOPE["x"], 11)
        self.assertEqual(spi.GLOBAL_SCOPE["number"], 2)

    def test_program1_case_insensitive(self):
        from test.data.programs import program1_case_insensitive
        spi = _make_interpreter(text=program1_case_insensitive)
        spi.execute()

        self.assertEqual(spi.GLOBAL_SCOPE["a"], 2)
        self.assertEqual(spi.GLOBAL_SCOPE["b"], 25)
        self.assertEqual(spi.GLOBAL_SCOPE["c"], 27)
        self.assertEqual(spi.GLOBAL_SCOPE["x"], 11)
        self.assertEqual(spi.GLOBAL_SCOPE["number"], 2)

    def test_program1_integer_div(self):
        from test.data.programs import program1_integer_div
        spi = _make_interpreter(text=program1_integer_div)
        spi.execute()

        self.assertEqual(spi.GLOBAL_SCOPE["a"], 2)
        self.assertEqual(spi.GLOBAL_SCOPE["b"], 25)
        self.assertEqual(spi.GLOBAL_SCOPE["c"], 27)
        self.assertEqual(spi.GLOBAL_SCOPE["x"], 11)
        self.assertEqual(spi.GLOBAL_SCOPE["number"], 2)

    def test_program_underscore_id(self):
        from test.data.programs import program_with_underscore_id
        spi = _make_interpreter(text=program_with_underscore_id)
        spi.execute()

        self.assertEqual(spi.GLOBAL_SCOPE["_x_"], 42)


def _make_interpreter(text):
    return Interpreter(parser=Parser(lexer=Lexer(text=text)))
