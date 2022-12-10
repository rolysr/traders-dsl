from sly import Lexer, Parser

class TradersLexer(Lexer):
    """
        Traders DSL Lexer
    """

    tokens = {ID, INT, FLOAT, ASSIGN, STRING, LET,

              IN, CASE, OTHER, OTHERWISE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, REPEAT,
              WHEN, BEHAVE, STOP, RUN,

              TRUE, FALSE,

              AND, OR, SHR, SHL, INC, DEC, PLUSASGN,
              MINUSASGN, STARASGN, SLASHASGN, MODULOASGN,
              ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN,

              AGENT, ENVIRONMENT, INT_TYPE, FLOAT_TYPE, BOOL_TYPE,
              LIST_TYPE, STRING_TYPE, PIPE,

              FIND, PEERS, MOVE, UP, LEFT, RIGHT, DOWN,
              TRADE, PICK, PUT, AT }

    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.'}

    INC = r'\+\+'
    DEC = r'--'
    PIPE = r'\|>'
    PLUSASGN = r'\+='
    MINUSASGN = r'-='
    STARASGN = r'\*='
    SLASHASGN = r'/='
    MODULOASGN = r'%='
    ANDASGN = r'&='
    ORASGN = r'\|='
    XORASGN = r'^='
    SHLASGN = r'<<='
    SHRASGN = r'>>='
    LESSEQ = r'<='
    GREATEREQ = r'>='
    SHR = r'>>'
    SHL = r'<<'
    LESS = r'<'
    GREATER = r'>'
    NOTEQ = r'!='
    EQEQ = r'=='
    ASSIGN = r'='
    SEP = r';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['let'] = LET

    ID['in'] = IN
    ID['case'] = CASE
    ID['other'] = OTHER
    ID['otherwise'] = OTHERWISE
    ID['repeat'] = REPEAT
    ID['when'] = WHEN
    ID['behave'] = BEHAVE
    ID['agent'] = AGENT
    ID['environment'] = ENVIRONMENT
    ID['stop'] = STOP
    ID['run'] = RUN
    ID['find'] = FIND
    ID['peers'] = PEERS
    ID['move'] = MOVE
    ID['UP'] = UP
    ID['left'] = LEFT
    ID['right'] = RIGHT
    ID['down'] = DOWN
    ID['trade'] = TRADE
    ID['pick'] = PICK
    ID['put'] = PUT
    ID['AT'] = AT

    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['and'] = AND
    ID['or'] = OR
    ID['int'] = INT_TYPE
    ID['float'] = FLOAT_TYPE
    ID['string'] = STRING_TYPE
    ID['bool'] = BOOL_TYPE
    ID['list'] = LIST_TYPE

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\"", "\"")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Illegal character '%s' on line %d" % (t.value[0], self.lineno))
        self.index += 1
