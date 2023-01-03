from sly import Parser
from src.traders_lexer import TradersLexer


class TradersParser(Parser):
    """
    Parser for the Traders DLS
    """
    tokens = TradersLexer.tokens
    start = 'program'
    debugfile = 'aiuda.pofavo'

    precedence = (
        ('right', PLUSASGN, MINUSASGN, STARASGN, SLASHASGN,
         MODULOASGN, ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN),
        ('left', OR),
        ('left', AND),
        ('left', EQEQ, NOTEQ),
        ('left', LESS, LESSEQ, GREATER, GREATEREQ),
        ('left', SHL, SHR),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS', INC, DEC),
        ('right', '!'),
    )

    @_('declarationList')
    def program(self, p):
        return ('program', p.declarationList)

    #Declarations productions:

    @_('declaration declarationList')
    def declarationList(self, p):
        return (p.declaration, ) + p.declarationList

    @_('empty')
    def declarationList(self, p):
        return ()

    @_('envDecl')
    def declaration(self, p):
        return p.envDecl

    @_('agentDecl')
    def declaration(self, p):
        return p.agentDecl

    @_('behaveDecl')
    def declaration(self, p):
        return p.behaveDecl

    @_('varDecl')
    def declaration(self, p):
        return p.varDecl

    @_('varAssign')
    def declaration(self, p):
        return p.varAssign

    @_('envFunc')
    def declaration(self, p):
        return p.envFunc

    @_('ENV ID "{" envBody "}"')
    def envDecl(self, p):
        return ('env', p.ID, p.envBody)

    @_('AGENT ID "{" agentBody "}"')
    def agentDecl(self, p):
        return ('agent', p.ID, p.agentBody)

    @_('BEHAVE ID "{" behaveBody "}"')
    def behaveDecl(self, p):
        return ('behave', p.ID, p.behaveBody)

    @_('LET ID ":" type SEP')
    def varDecl(self, p):
        return ('varDecl_0', p.ID, p.type)

    @_('LET ID ":" type ASSIGN expr SEP')
    def varDecl(self, p):
        return ('varDecl_1', p.ID, p.type, p.expr)

    @_('getter ASSIGN expr SEP')
    def varAssign(self, p):
        return ('varAssign', p.getter , p.expr)

    @_('RESET ID SEP')
    def envFunc(self, p):
        return ('resetEnv', p.ID)

    @_('RUN ID WITH expr ITERATIONS SEP')
    def envFunc(self, p):
        return ('runEnv', p.ID, p.expr)

    @_('PUT ID IN ID AT expr "," expr SEP')
    def envFunc(self, p):
        return ('putEnv', p.ID0, p.ID1, p.expr0, p.expr1)

    #Declarations productions end

    #Bodies productions:

    @_('varList')
    def envBody(self, p):
        return ('envBody', p.varList)

    @_('varList')
    def agentBody(self, p):
        return ('agentBody', p.varList)

    @_('statementList')
    def behaveBody(self, p):
        return ('behaveBody', p.statementList)

    @_('varDecl varList')
    def varList(self, p):
        return (p.varDecl, ) + p.varList

    @_('varAssign varList')
    def varList(self, p):
        return (p.varAssign, ) + p.varList

    @_('empty')
    def varList(self, p):
        return ( )

    @_('statement statementList')
    def statementList(self, p):
        return (p.statement, ) + p.statementList

    @_('empty')
    def statementList(self, p):
        return ( )

    #Bodies productions end
    
    #Statements productions:
    
    ##Statement types
    @_('varDecl')
    def statement(self, p):
        return p.varDecl

    @_('varAssign')
    def statement(self, p):
        return p.varAssign
        
    @_('repeatStmt')
    def statement(self, p):
        return p.repeatStmt
        
    @_('foreachStmt')
    def statement(self, p):
        return p.foreachStmt
        
    @_('incaseStmt')
    def statement(self, p):
        return p.incaseStmt
        
    @_('primFuncStmt')
    def statement(self, p):
        return p.primFuncStmt

    ## Loops and conditionals
    @_('REPEAT WHEN expr "{" statementList "}" ')
    def repeatStmt(self, p):
        return ('repeatStmt', p.expr, p.statementList)

    @_('FOREACH ID IN expr "{" statementList "}" ')
    def foreachStmt(self, p):
        return ('foreachStmt', p.ID, p.expr, p.statementList)

    @_('IN CASE expr "{" statementList "}" inothercaseStmt')
    def incaseStmt(self, p):
        return ('incaseStmt', p.expr, p.statementList, p.inothercaseStmt)

    @_('IN OTHER CASE expr "{" statementList "}" inothercaseStmt')
    def inothercaseStmt(self, p):
        return ('inothercaseStmt_0', p.expr, p.statementList, p.inothercaseStmt)

    @_('OTHERWISE "{" statementList "}"')
    def inothercaseStmt(self, p):
        return ('inothercaseStmt_1', p.statementList)

    @_('empty')
    def inothercaseStmt(self, p):
        return ('inothercaseStmt_2')
    
    ##Primitive Functions Statements

    @_('TALK expr SEP')
    def primFuncStmt(self, p):
        return ('talk', p.expr)

    @_('moveStmt SEP')
    def primFuncStmt(self, p):
        return ('moveStmt', p.moveStmt)

    @_('buyStmt SEP')
    def primFuncStmt(self, p):
        return ('buyStmt', p.buyStmt)

    @_('SELL expr "," expr "," expr SEP')
    def primFuncStmt(self, p):
        return ('sell', p.expr0, p.expr1, p.expr2)
        
    @_('RESTART BEHAVE SEP')
    def primFuncStmt(self, p):
        return ('restart')
        
    @_('STOP SEP')
    def primFuncStmt(self, p):
        return ('stop')
        
    @_('PICK expr SEP')
    def primFuncStmt(self, p):
        return ('pick', p.expr)
        
    @_('PUT expr "," expr SEP')
    def primFuncStmt(self, p):
        return ('put', p.expr0, p.expr1)

    @_('getter "." listVoidFunc SEP')
    def primFuncStmt(self, p):
        return ('listVoidFunc', p.getter, p.listVoidFunc)

    @_('PUSH expr')
    def listVoidFunc(self, p):
        return ('push', p.expr)

    @_('POP')
    def listVoidFunc(self, p):
        return ('pop', ())

    @_('REVERSE')
    def listVoidFunc(self, p):
        return ('reverse', ())

    @_('MOVE expr "," expr')
    def moveStmt(self, p):
        return ('moveStmt_0', p.expr0, p.expr1)

    @_('MOVE UP')
    def moveStmt(self, p):
        return ('moveStmt_1', 'up')

    @_('MOVE DOWN')
    def moveStmt(self, p):
        return ('moveStmt_1', 'down')

    @_('MOVE LEFT')
    def moveStmt(self, p):
        return ('moveStmt_1', 'left')

    @_('MOVE RIGHT')
    def moveStmt(self, p):
        return ('moveStmt_1', 'down')

    @_('BUY expr "," expr "," expr')
    def buyStmt(self, p):
        return ('buyStmt_0', p.expr0, p.expr1, p.expr2)

    @_('BUY expr')
    def buyStmt(self, p):
        return ('buyStmt_1', p.expr)
    

    #Expression productions
    @_('expr OR expr')
    def expr(self, p):
        return ('or', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('and', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ('!=', p.expr0, p.expr1)

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('==', p.expr0, p.expr1)

    @_('expr LESS expr')
    def expr(self, p):
        return ('<', p.expr0, p.expr1)

    @_('expr LESSEQ expr')
    def expr(self, p):
        return ('<=', p.expr0, p.expr1)

    @_('expr GREATEREQ expr')
    def expr(self, p):
        return ('>=', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def expr(self, p):
        return ('>', p.expr0, p.expr1)

    @_('expr "+" expr')
    def expr(self, p):
        return ('+', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('-', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('*', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('/', p.expr0, p.expr1)

    @_('"!" expr')
    def expr(self, p):
        return ('!', p.expr)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('neg', p.expr)

    @_('call')
    def expr(self, p):
        return p.call

    #Expression productions end

    #Calling productions

    @_('primary')
    def call(self, p):
        return p.primary

    @_('primitiveValue')
    def call(self, p):
        return p.primitiveValue

    @_('ID dotTail')
    def call(self, p):
        return ('call', p.ID, p.dotTail)

    @_('ID dotTail')
    def getter(self, p):
        return ('call', p.ID, p.dotTail)

    @_('"." idTail dotTail')
    def dotTail(self, p):
        return ('dotTail', p.idTail, p.dotTail)

    @_('empty')
    def dotTail(self, p):
        return ()

    @_('ID')
    def idTail(self, p):
        return ('idTail_0', p.ID)

    @_('listValueFunc')
    def idTail(self, p):
        return ('idTail_1', p.listValueFunc)

    @_('GET expr')
    def listValueFunc(self, p):
        return ('get', p.expr)

    @_('SIZE')
    def listValueFunc(self, p):
        return ('size')

    @_('RANDOM FROM expr TO expr')
    def primitiveValue(self, p):
        return ('random', p.expr0, p.expr1)
        
    @_('FIND OBJECTS')
    def primitiveValue(self, p):
        return ('find', 'objects')
        
    @_('FIND PEERS')
    def primitiveValue(self, p):
        return ('find', 'peers')

    @_('TRUE')
    def primary(self, p):
        return ('primary_bool', True)

    @_('FALSE')
    def primary(self, p):
        return ('primary_bool', False)

    @_('NUMBER')
    def primary(self, p):
        return ('primary_number', p.NUMBER)

    @_('STRING')
    def primary(self, p):
        return ('primary_string', p.STRING)

    @_('"[" listItems "]"')
    def primary(self, p):
        return ('primary_list', p.listItems)

    @_('"{" bookItems "}"')
    def primary(self, p):
        return ('primary_book', p.bookItems)

    @_('"(" expr ")"')
    def primary(self, p):
        return p.expr

    @_('expr "," listItems')
    def listItems(self, p):
        return (p.expr, ) + p.listItems

    @_('empty')
    def listItems(self, p):
        return ( )

    @_('STRING ":" "(" listItems ")" "," bookItems')
    def bookItems(self, p):
        return ((p.STRING, ('primary_list', p.listItems)), ) + p.bookItems

    @_('empty')
    def bookItems(self, p):
        return ( )

    @_('NUMBER_TYPE')
    def type(self, p):
        return 'number'

    @_('BOOL_TYPE')
    def type(self, p):
        return 'bool'

    @_('STRING_TYPE')
    def type(self, p):
        return 'string'

    @_('LIST_TYPE')
    def type(self, p):
        return 'list'

    @_('BOOK_TYPE')
    def type(self, p):
        return 'book'
    
    @_('')
    def empty(self, p):
        pass
