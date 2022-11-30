from traders_lexer import TradersLexer
from traders_parser import TradersParser

if __name__ == '__main__':
    lexer = TradersLexer()
    parser = TradersParser()
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
