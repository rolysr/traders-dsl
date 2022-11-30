from sly import Lexer, Parser

class TradersLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, TRUE, FALSE, NAME, PLUS, 
               MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE, 
               LPAREN, RPAREN, AND, OR}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    LPAREN = r'\('
    RPAREN = r'\)'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and keywords
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['and'] = AND
    NAME['or'] = OR
    NAME['True'] = TRUE
    NAME['False'] = FALSE

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1