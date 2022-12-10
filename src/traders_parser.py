from sly import Parser
from traders_lexer import TradersLexer

class TradersParser(Parser):
    """
        Traders DSL Parser
    """

    """
    Parser for the Traders Language
    """
    tokens = TradersLexer.tokens

    precedence = (
        ('right', PLUSASGN, MINUSASGN, STARASGN, SLASHASGN,
         MODULOASGN, ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN),
        ('left', OR),
        ('left', AND),
        ('left', '|'),
        ('left', '^'),
        ('left', '&'),
        ('left', EQEQ, NOTEQ),
        ('left', LESS, LESSEQ, GREATER, GREATEREQ),
        ('left', SHL, SHR),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS', 'UPLUS', 'LOGICALNOT', INC, DEC),
        ('right', '!'),
    )

    @_('declarationList')
    def program(self, p):
        return p.declarations

    @_('empty')
    def program(self, p):
        return ()

    @_('declaration')
    def declarationList(self, p):
        return (p.declaration, )

    @_('declaration declarationList')
    def declarationList(self, p):
        return (p.declaration, ) + p.declarations

    @_('behaveDecl')
    def declaration(self, p):
        return p.behaveDecl

    @_('varDecl')
    def declaration(self, p):
        return p.varDecl

    @_('while_statement')
    def declaration(self, p):
        return p.while_statement
    
    @_('fieldAssign')
    def declaration(self, p):
        return p.fieldAssign
    
    @_('envFunc')
    def declaration(self, p):
        return p.envFunc

    @_('envDecl')
    def declaration(self, p):
        return p.envDecl

    @_('agentDecl')
    def declaration(self, p):
        return p.agentDecl

    @_('ENV ID "{" envBody "}"')
    def envDecl(self, p):
        return ('env', p.ID, ('varDeclList', p.varDeclList))

    @_('AGENT ID "{" agentBody "}"')
    def envDecl(self, p):
        return ('agent', p.ID, ('varDeclList', p.varDeclList))

    @_('BEHAVE ID "{" behaveBody "}"')
    def envDecl(self, p):
        return ('behave', p.ID, ('statementList', p.statementList))

    @_('ID "." ID ASSIGN expression SEP')
    def fieldAssign(self, p):
        return ('assign', ('get', p.ID0, p.ID1), p.expression)

    @_('ID "." RESET SEP')
    def envFunc(self, p):
        return ('reset', p.ID)

    @_('ID "." RUN expression SEP')
    def envFunc(self, p):
        return ('run', p.ID, p.expression)

    @_('LET ID ":" var_type SEP')
    def varDecl(self, p):
        return [(p.ID, p.var_type)]

    @_('LET ID ":" var_type ASSIGN expression SEP')
    def varDecl(self, p):
        return [(p.ID, p.var_type, p.expression)]

    @_('ID ASSIGN expression SEP')
    def varDecl(self, p):
        return ('var_assign', p.ID, p.expression)

    @_('NUMBER_TYPE')
    def var_type(self, p):
        return 'number'

    @_('STRING_TYPE')
    def var_type(self, p):
        return 'string'

    @_('BOOL_TYPE')
    def var_type(self, p):
        return 'bool'

    @_('LIST_TYPE')
    def var_type(self, p):
        return 'list'

    @_('varDeclList')
    def envBody(self, p):
        return p.varDeclList

    @_('varDeclList')
    def agentBody(self, p):
        return p.varDeclList

    @_('FN ID "(" params ")" block')
    def function_definition(self, p):
        return ('fn', p.ID, ('params', p.params), ('block', p.block))

    @_('ID LEFTARROW "{" struct_init_exprs "}" ')
    def expr(self, p):
        return ('init_struct', p.ID, p.struct_init_exprs)

    @_('expr')
    def struct_init_exprs(self, p):
        return [p.expr]

    @_('struct_init_exprs "," expr')
    def struct_init_exprs(self, p):
        return p.struct_init_exprs + [p.expr]

    @_('LAMBDA "(" params ")" ARROW expr')
    def expr(self, p):
        return ('lambda', ('params', p.params), ('block', ('return', p.expr)))
        
    @_('LET var ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.var, p.expr)
        
    @_('LET getter ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.getter, p.expr)

    @_('LET var ":" var_type SEP')
    def statement(self, p):
        return ('var_define_no_expr', p.var, p.var_type)

    @_('TYPEOF expr')
    def expr(self, p):
        return ('typeof', p.expr)

    @_('var_assign SEP')
    def statement(self, p):
        return p.var_assign

    @_('RETURN expr SEP')
    def return_statement(self, p):
        return ('return', p.expr)

    @_('var ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, p.expr)

    @_('var PLUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), p.expr))

    @_('var MINUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), p.expr))

    @_('var STARASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('*', ('var', p.var), p.expr))

    @_('var SLASHASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('/', ('var', p.var), p.expr))

    @_('var MODULOASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('%', ('var', p.var), p.expr))

    @_('var ANDASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('&', ('var', p.var), p.expr))

    @_('var ORASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('|', ('var', p.var), p.expr))

    @_('var XORASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('^', ('var', p.var), p.expr))

    @_('var SHLASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('<<', ('var', p.var), p.expr))

    @_('var SHRASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('>>', ('var', p.var), p.expr))
        
    @_('IF expr block ELSE block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IF expr block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block), None)

    @_('WHILE expr block')
    def while_statement(self, p):
        return ('while', ('condition', p.expr), ('block', p.block))

    @_('FOR var_assign SEP expr SEP var_assign block')
    def for_statement(self, p):
        return (p.var_assign0, ('while', ('condition', p.expr), ('block', p.block + (p.var_assign1, ))))

    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('?:', p.expr0, p.expr1, p.expr2)

    @_('ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))

    @_('ID DOUBLECOLON ID "(" args ")"')
    def expr(self, p):
        return ('class_func_call', p.ID0, p.ID1, ('args', p.args))

    @_('expr PIPE ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', [p.expr] + p.args))

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('==', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ('!=', p.expr0, p.expr1)

    @_('expr LESSEQ expr')
    def expr(self, p):
        return ('<=', p.expr0, p.expr1)

    @_('expr GREATEREQ expr')
    def expr(self, p):
        return ('>=', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('and', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ('or', p.expr0, p.expr1)

    @_('expr LESS expr')
    def expr(self, p):
        return ('<', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def expr(self, p):
        return ('>', p.expr0, p.expr1)

    @_('expr SHL expr')
    def expr(self, p):
        return ('<<', p.expr0, p.expr1)

    @_('expr SHR expr')
    def expr(self, p):
        return ('>>', p.expr0, p.expr1)

    @_('expr "&" expr')
    def expr(self, p):
        return ('&', p.expr0, p.expr1)

    @_('expr "^" expr')
    def expr(self, p):
        return ('^', p.expr0, p.expr1)

    @_('expr "|" expr')
    def expr(self, p):
        return ('|', p.expr0, p.expr1)

    @_('"~" expr %prec LOGICALNOT')
    def expr(self, p):
        return ('~', p.expr)

    @_('expr SEP')
    def statement(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('neg', p.expr)

    @_('"+" expr %prec UPLUS')
    def expr(self, p):
        return p.expr

    @_('"!" expr')
    def expr(self, p):
        return ('!', p.expr)

    @_('INC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), 1))

    @_('DEC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), 1))

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

    @_('expr "%" expr')
    def expr(self, p):
        return ('%', p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('INT')
    def expr(self, p):
        return p.INT

    @_('FLOAT')
    def expr(self, p):
        return p.FLOAT

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('TRUE')
    def expr(self, p):
        return True

    @_('FALSE')
    def expr(self, p):
        return False

    @_('list_val')
    def expr(self, p):
        return p.list_val

    @_('"[" exprs "]"')
    def list_val(self, p):
        return p.exprs

    @_('empty')
    def exprs(self, p):
        return []

    @_('expr')
    def exprs(self, p):
        return [p.expr]

    @_('exprs "," expr')
    def exprs(self, p):
        return p.exprs + [p.expr]

    @_('var "[" expr "]"')
    def expr(self, p):
        return ('indexing', ('var', p.var), p.expr)

    @_('var')
    def expr(self, p):
        return ('var', p.var)

    @_('ID')
    def var(self, p):
        return p.ID

    @_('var "[" expr "]"')
    def var(self, p):
        return ('indexing', ('var', p.var), p.expr)

    @_('NIL')
    def expr(self, p):
        return None

    @_('')
    def empty(self, p):
        pass

    @_('"{" program "}"')
    def block(self, p):
        return p.program

    @_('statement')
    def block(self, p):
        return (p.statement, )

    @_('params "," param')
    def params(self, p):
        return p.params + [p.param]

    @_('param')
    def params(self, p):
        return [p.param]

    @_('empty')
    def params(self, p):
        return []

    @_('ID ":" var_type')
    def param(self, p):
        return (p.ID, p.var_type)

    @_('args "," arg')
    def args(self, p):
        return p.args + [p.arg]

    @_('arg')
    def args(self, p):
        return [p.arg]

    @_('empty')
    def args(self, p):
        return []

    @_('expr')
    def arg(self, p):
        return p.expr

    @_('"{" member_list "}"')
    def expr(self, p):
        return p.member_list

    @_('empty')
    def member_list(self, p):
        return {}

    @_('member')
    def member_list(self, p):
        return p.member

    @_('member_list "," member')
    def member_list(self, p):
        return { **p.member_list, **p.member }

    @_('STRING ":" expr')
    def member(self, p):
        return { p.STRING : p.expr }

    @_('getter "." ID')
    def getter(self, p):
        return ('.', p.getter, p.ID)

    @_('ID')
    def getter(self, p):
        return p.ID

    @_('getter')
    def expr(self, p):
        return p.getter
