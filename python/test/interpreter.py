
from random import randint
from unittest import TestCase

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


MIN, MAX = 100, 1000


def _make_interpreter(text):
    return Interpreter(parser=Parser(lexer=Lexer(text=text)))


class InterpreterTc(TestCase):
    def test_num(self):
        i = _make_interpreter("42")
        self.assertEqual(i.execute(), 42)

    def test_num_rnd(self):
        x = randint(MIN, MAX)
        i = _make_interpreter(f"{x}")
        self.assertEqual(i.execute(), x)

    def test_plus(self):
        i = _make_interpreter("30 + 12")
        self.assertEqual(i.execute(), 42)

    def test_plus_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} + {x2}")
        self.assertEqual(i.execute(), x1 + x2)

    def test_minus(self):
        i = _make_interpreter("100 - 58")
        self.assertEqual(i.execute(), 42)

    def test_minus_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} - {x2}")
        self.assertEqual(i.execute(), x1 - x2)

    def test_plus_minus(self):
        i = _make_interpreter("30 + 30 - 18")
        self.assertEqual(i.execute(), 42)

    def test_plus_minus_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        x3 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} + {x2} - {x3}")
        self.assertEqual(i.execute(), x1 + x2 - x3)

    def test_multiply(self):
        i = _make_interpreter("7 * 6")
        self.assertEqual(i.execute(), 42)

    def test_multiply_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} * {x2}")
        self.assertEqual(i.execute(), x1 * x2)

    def test_divide(self):
        i = _make_interpreter("1764 / 42")
        self.assertEqual(i.execute(), 42)

    def test_divide_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} / {x2}")
        self.assertEqual(i.execute(), x1 // x2)

    def test_divide_multiply_divide(self):
        i = _make_interpreter("336 / 48 * 54 / 9")
        self.assertEqual(i.execute(), 42)

    def test_divide_multiply_divide_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        x3 = randint(MIN, MAX)
        x4 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} / {x2} * {x3} / {x4}")
        self.assertEqual(i.execute(), x1 // x2 * x3 // x4)


    def test_plus_multiply_minus(self):
        i = _make_interpreter("4 + 5 * 8 - 2")
        self.assertEqual(i.execute(), 42)

    def test_plus_multiply_minus_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        x3 = randint(MIN, MAX)
        x4 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} + {x2} * {x3} - {x4}")
        self.assertEqual(i.execute(), x1 + x2 * x3 - x4)

    def test_parentheses(self):
        i = _make_interpreter("(16 + 5) * 2")
        self.assertEqual(i.execute(), 42)

    def test_parentheses_rnd(self):
        x1 = randint(MIN, MAX)
        x2 = randint(MIN, MAX)
        x3 = randint(MIN, MAX)
        i = _make_interpreter(f"{x1} * ({x2} + {x3})")
        self.assertEqual(i.execute(), x1 * (x2 + x3))

    def test_trailing_whitespace(self):
        i = _make_interpreter("42 * (3 + 4 * (12 - 3))   ")
        self.assertEqual(i.execute(), 1638)

    def test_preceeding_whitespace(self):
        i = _make_interpreter("     42 * (3 + 4 * (12 - 3))")
        self.assertEqual(i.execute(), 1638)
