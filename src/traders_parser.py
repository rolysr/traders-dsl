from sly import Parser
from src.traders_lexer import TradersLexer


class TradersParser(Parser):
    """
    Parser for the Traders DLS
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

    @_('statements')
    def program(self, p):
        return p.statements

    @_('empty')
    def program(self, p):
        return ()

    @_('statement')
    def statements(self, p):
        return (p.statement, )

    @_('statements statement')
    def statements(self, p):
        return p.statements + (p.statement, )

    @_('behavior_statement')
    def statement(self, p):
        return p.behavior_statement

    @_('stop_statement')
    def statement(self, p):
        return p.stop_statement

    @_('repeat_when_statement')
    def statement(self, p):
        return p.repeat_when_statement
    
    @_('in_case_statement')
    def statement(self, p):
        return p.in_case_statement

    @_('empty')
    def behavior_statement(self, p):
        return []

    @_('behavior_definition')
    def behavior_statement(self, p):
        return [p.behavior_definition]

    @_('INT_TYPE')
    def var_type(self, p):
        return 'int'

    @_('FLOAT_TYPE')
    def var_type(self, p):
        return 'float'

    @_('STRING_TYPE')
    def var_type(self, p):
        return 'string'

    @_('BOOL_TYPE')
    def var_type(self, p):
        return 'bool'

    @_('LIST_TYPE')
    def var_type(self, p):
        return 'list'

    @_('DICT_TYPE')
    def var_type(self, p):
        return 'dict'

    @_('var_define SEP')
    def statement(self, p):
        return p.var_define

    @_('BEHAVIOR ID "(" params ")" block')
    def behavior_definition(self, p):
        return ('behavior', p.ID, ('params', p.params), ('block', p.block))

    @_('LET var ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.var, p.expr)
        
    @_('LET getter ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.getter, p.expr)

    @_('LET var ":" var_type SEP')
    def statement(self, p):
        return ('var_define_no_expr', p.var, p.var_type)

    @_('var_assign SEP')
    def statement(self, p):
        return p.var_assign

    @_('STOP expr SEP')
    def stop_statement(self, p):
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
        
    @_('IN CASE expr block OTHERWISE block')
    def in_case_statement(self, p):
        return ('in_case', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IN CASE expr block in_other_case_statement')
    def in_case_statement(self, p):
        return ('in_case', ('condition', p.expr), ('block', p.block), (p.in_other_case_statement))

    @_('IN CASE expr block')
    def in_case_statement(self, p):
        return ('in_case', ('condition', p.expr), ('block', p.block), None)

    @_('IN OTHER CASE expr block in_other_case_statement')
    def in_other_case_statement(self, p):
        return ('in_case', ('condition', p.expr), ('block', p.block), (p.in_other_case_statement))

    @_('IN OTHER CASE expr block OTHERWISE block')
    def in_other_case_statement(self, p):
        return ('in_case', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IN OTHER CASE expr block')
    def in_other_case_statement(self, p):
        return ('in_case', ('condition', p.expr), ('block', p.block))

    @_('REPEAT WHEN expr block')
    def repeat_when_statement(self, p):
        return ('repeat_when', ('condition', p.expr), ('block', p.block))

    @_('ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))

    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('?:', p.expr0, p.expr1, p.expr2)

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
