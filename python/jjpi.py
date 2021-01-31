
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def _evaluate(text):
    interpreter = Interpreter(parser=Parser(lexer=Lexer(text=text)))
    return interpreter.execute()


def main():
    print("Press Ctrl+C to quit.")
    counter = 1
    while True:
        try:
            text = input(f"In [{counter}]: ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print(
                "\n"
                "It is man's natural sickness "
                "to believe that he possesses the Truth."
                "\n"
            )

            break
        if not text:
            continue
        print(f"Out[{counter}]: {_evaluate(text)}")
        counter += 1


if __name__ == "__main__":
    main()
