from src.traders_lexer import TradersLexer
from src.traders_parser import TradersParser
from src.traders_interpreter import Process
import sys


def repl():
    lexer = TradersLexer()
    parser = TradersParser()
    env = {}
    program = Process((), env=env)
    while True:
        try:
            text = input('>> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)

            try:
                tree = parser.parse(tokens)
                program.tree = tree
                program.run()
            except TypeError as e:
                if str(e).startswith("'NoneType' object is not iterable"):
                    print("Syntax Error")
                else:
                    print(e)


def exec_file():
    lexer = TradersLexer()
    parser = TradersParser()
    with open(sys.argv[1]) as opened_file:
        text = opened_file.read()
        tokens = lexer.tokenize(text)

        tree = parser.parse(tokens)

        program = Process(tree)
        program.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        exec_file()
