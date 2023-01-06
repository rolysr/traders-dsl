from sly import Lexer


class TradersLexer(Lexer):
    """
        Traders DSL Lexer
    """

    tokens = {ID, NUMBER, ASSIGN, STRING, LET,

              IN, CASE, OTHER, OTHERWISE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, REPEAT, WITH, ITERATIONS,
              WHEN, FOREACH, BEHAVE, RESTART, STOP, RUN, RESET,

              TRUE, FALSE,

              AND, OR,

              AGENT, ENV, NUMBER_TYPE, BOOK_TYPE, BOOL_TYPE,
              LIST_TYPE, STRING_TYPE,

              PUSH, POP, SIZE, REVERSE,

              RANDOM, FROM, TO, OBJECTS, FIND, PEERS, MOVE, UP, LEFT, RIGHT, DOWN,
              SELL, BUY, PICK, PUT, AT, TALK}

    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.'}

    LESSEQ = r'<='
    GREATEREQ = r'>='
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
    ID['foreach'] = FOREACH
    ID['behave'] = BEHAVE
    ID['agent'] = AGENT
    ID['env'] = ENV
    ID['restart'] = RESTART
    ID['stop'] = STOP
    ID['run'] = RUN
    ID['reset'] = RESET
    ID['random'] = RANDOM
    ID['find'] = FIND
    ID['peers'] = PEERS
    ID['move'] = MOVE
    ID['up'] = UP
    ID['left'] = LEFT
    ID['right'] = RIGHT
    ID['down'] = DOWN
    ID['sell'] = SELL
    ID['buy'] = BUY
    ID['pick'] = PICK
    ID['put'] = PUT
    ID['at'] = AT
    ID['talk'] = TALK
    ID['with'] = WITH
    ID['iterations'] = ITERATIONS
    ID['from'] = FROM
    ID['to'] = TO
    ID['objects'] = OBJECTS

    ID['push'] = PUSH
    ID['pop'] = POP
    ID['size'] = SIZE
    ID['reverse'] = REVERSE

    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['and'] = AND
    ID['or'] = OR
    ID['number'] = NUMBER_TYPE
    ID['bool'] = BOOL_TYPE
    ID['string'] = STRING_TYPE
    ID['list'] = LIST_TYPE
    ID['book'] = BOOK_TYPE

    @_(r'\d+\.\d+')
    def NUMBER(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUMBER(self, t):
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
