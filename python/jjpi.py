
from argparse import ArgumentParser

from spi.lexer import Lexer
from spi.parser import Parser
from spi.interpreter import Interpreter


def _evaluate(path_to_source, should_log_stack=False):
    with open(path_to_source) as source_file:
        interpreter = Interpreter(
            should_log_stack=should_log_stack,
            parser=Parser(lexer=Lexer(text=source_file.read()))
        )
    return interpreter.execute()


def main():
    parser = ArgumentParser(
        description="JJPI - Simple Pascal Interpreter"
    )
    parser.add_argument("input_file", help="Pascal source file.")
    parser.add_argument(
        "--stack",
        help="Print stack information during execution.",
        action="store_true"
    )
    args = parser.parse_args()
    _evaluate(args.input_file, args.stack)


if __name__ == "__main__":
    main()
