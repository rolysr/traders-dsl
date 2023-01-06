from src.traders_lexer import TradersLexer
from src.traders_parser import TradersParser
from src.traders_interpreter import Process
from src.traders_semantics_checker import TradersSemanticsChecker
import sys


def exec_file():
    lexer = TradersLexer()
    parser = TradersParser()
    with open(sys.argv[1]) as opened_file:
        text = opened_file.read()
        tokens = lexer.tokenize(text)

        tree = parser.parse(tokens)

        checker = TradersSemanticsChecker(tree)
        checker.check()

        if checker.ok:
            program = Process(tree)
            program.run()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        exec_file()
    else:
        print("Must provide a file to compile and run.")
