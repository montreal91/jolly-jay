
from unittest import TestCase

from test.common import _make_interpreter


class ProgramTc(TestCase):
    def test_part10(self):
        # TODO: Think of a better way to test call stack state during execution
        #       and more general question is how to test an interpreter or
        #       or a compiler.

        with open("test/data/part10.pas") as source_file:
            spi = _make_interpreter(text=source_file.read())
            spi.execute()
            self.assertEqual(
                len(spi._call_stack),
                0,
                "After program execution the call stack should be empty"
            )

    def test_empty(self):
        with open("test/data/empty.pas") as source_file:
            spi = _make_interpreter(text=source_file.read())
            spi.execute()
            self.assertEqual(len(spi._call_stack), 0)

    def test_part12(self):
        with open("test/data/part12.pas") as source_file:
            spi = _make_interpreter(text=source_file.read())
            spi.execute()
            self.assertTrue(True)

    def test_part16(self):
        with open("test/data/part16.pas") as source_file:
            spi = _make_interpreter(text=source_file.read())
            spi.execute()
            self.assertTrue(True)
