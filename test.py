from src.traders_lexer import TradersLexer


lexer = TradersLexer()
tokens = lexer.tokenize("""

    let a = 2;

    agent a {

    }

    environment b {

    }

    behave normal{
        move up;
        move down;

        let a = 2;
        repeat when a % 2 == 0 {
            move up;
        } 
    }

""")

for token in tokens:
    print(token)