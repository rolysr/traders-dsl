from random import randint
from src.traders_lexer import TradersLexer
from src.traders_parser import TradersParser
from backend.list import *
from backend.agent import *
from backend.basic_types import *
from backend.behavior import *
from backend.book import *
from backend.environment import *
from backend.env import *


class TradersSemanticsChecker:
    """
        A class that represents a semantic
        checker for Traders DSL.
    """

    def __init__(self, tree, filename="?", env={}):
        self.tree = tree
        self.file_path = filename
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=Env({}))
            env.update(_env)
        # Context of variables
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0
        # Behave inner variables
        self.actual_agent = None
        self.env_instance = None

    def check(self, tree=None, env={}):
        current_env = self.env
        result = None
        if env != {}:
            self.env = env
        if tree is None:
            for line in self.tree:
                try:
                    result = self.visit(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
        else:
            for line in tree:
                try:
                    result = self.visit(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
        self.env = current_env
        return result

    def visit(self, parsed):
        """
        Evaluating a parsed tree/tuple/expression
        """
        if self.should_return:
            return None

        if type(parsed) != tuple:
            return (False, ())
        else:
            action = parsed[0]

            if action == 'call':
                func = self.env.find(parsed[1])
                if isinstance(func, Number) or isinstance(func, Bool) or isinstance(func, String) or isinstance(func, List) or isinstance(func, Book) or isinstance(func, Entry) or isinstance(func, TradersAgent) or isinstance(func, TradersEnvironment) or isinstance(func, Behavior):
                    ans = func.get_check(parsed[2], self)
                    return ans

                raise Exception("Error while resolving {}.".format(parsed))

            elif action == 'behave':
                self.env.update({parsed[1]: Behavior(
                    name=parsed[1], statement_list=parsed[2])})
                return 'void'

            elif action == 'agent':
                id = parsed[1]
                if id in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % id)

                body = parsed[2]

                self.env = Env(outer=self.env)

                self.env.update({'balance': Number(0)})
                self.env.update({'behavior': Behavior("unknown_behavior", ())})
                self.env.update({'on_keep': Book('number', {})})
                self.env.update({'on_sale': Book('number', {})})
                self.env.update(
                    {'location': List(element_type='number', value=[Number(0), Number(0)])})

                for varOp in body[1]:
                    if varOp[0] == 'varAssign':
                        self.visit(varOp)
                    else:
                        var_name = varOp[1]
                        if var_name in ['balance', 'on_keep', 'on_sale', 'behavior', 'location']:
                            raise AttributeError(
                                'Redeclaring default agent attributes in {}'.format(varOp))
                        self.visit(varOp)

                attributes = {}
                for attr in self.env.keys():
                    if attr not in ['balance', 'on_keep', 'on_sale', 'behavior', 'location']:
                        attributes[attr] = self.env[attr]

                agent = TradersAgent(balance=self.env['balance'],
                                     behavior=self.env['behavior'],
                                     on_keep=self.env['on_keep'],
                                     on_sale=self.env['on_sale'],
                                     location=self.env['location'],
                                     attributes=attributes)
                self.env = self.env.outer
                self.env.update({id: agent})
                return 'void'

            elif action == 'env':
                id = parsed[1]
                if id in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % id)

                body = parsed[2]

                self.env = Env(outer=self.env)

                self.env.update({'rows': Number(1)})
                self.env.update({'columns': Number(1)})
                self.env.update({'number_iterations': Number(0)})
                self.env.update({'log': Bool(True)})
                self.env.update(
                    {'agents': List(element_type='agent', value=[])})

                for varOp in body[1]:
                    if varOp[0] == 'varAssign':
                        self.visit(varOp)
                    else:
                        raise AttributeError(
                            'Env data type does not allow attribute declaration in {}'.format(varOp))  # for now

                environment = TradersEnvironment(rows=self.env['rows'],
                                                 columns=self.env['columns'],
                                                 number_iterations=self.env['number_iterations'],
                                                 log=self.env['log'],
                                                 agents=self.env['agents'])
                self.env = self.env.outer
                self.env.update({id: environment})
                return 'void'

            elif action == 'runEnv':
                if not parsed[1] in self.env:
                    raise Exception(
                        "{0} not found from {1} production.".format(parsed[1], parsed))
                
                env_instance = self.env[parsed[1]]
                if not isinstance(env_instance, TradersEnvironment):
                    raise Exception(
                        "Run statement must be called on an Environment instance in {}".format(parsed))

                if len(parsed) == 3 and self.visit(parsed[2]) not in ['number', 'any']:
                    raise Exception(
                        "Iterations param must be a number in {}".format(parsed))

                return 'void'

            elif action == 'resetEnv':
                if not parsed[1] in self.env:
                    raise Exception(
                        "{0} not found from {1} production.".format(parsed[1], parsed))
                
                env_instance = self.env[parsed[1]]
                if not isinstance(env_instance, TradersEnvironment):
                    raise Exception(
                        "Reset statement must be called on an Environment instance in {}".format(parsed))

                return 'void'

            elif action == 'putEnv':
                # get object to add
                obj_type = self.visit(parsed[2])

                # get environment instance
                if not parsed[1] in self.env:
                    raise Exception(
                        "{0} not found from {1} production.".format(parsed[1], parsed))
                
                env_instance = self.env[parsed[1]]
                if not isinstance(env_instance, TradersEnvironment):
                    raise Exception(
                        "Put statement must be called on an Environment instance in {}".format(parsed))

                # get location
                row = self.visit(parsed[3])
                column = self.visit(parsed[4])

                if row not in ['number', 'any'] or column not in ['number', 'any']:
                    raise ValueError(
                        "Wrong parameter types in {}".format(parsed))

                # check if type is agent or book
                if obj_type not in ['agent', 'any'] and obj_type not in ['book', 'any']:
                    raise ValueError(
                        "Invalid value to add to environment in {}".format(parsed))

                return 'void'

            elif action == 'restart':
                return 'void'

            elif action == 'stop':
                return 'void'

            elif action == 'sell':
                produt_name = self.visit(parsed[1])
                amount = self.visit(parsed[2])
                price = self.visit(parsed[3])

                if produt_name not in ['string', 'any'] or amount not in ['number', 'any'] or price not in ['number', 'any']:
                    return ValueError('Invalid values for sell operation in {}'.format(parsed))

                return 'void'

            elif action == 'pick':
                product_name = self.visit(parsed[1])

                if product_name not in ['string', 'any']:
                    return ValueError("pick function must receive a product name as a String in {}".format(parsed))

                return 'void'

            elif action == 'put':
                product_name = self.visit(parsed[1])
                amount = self.visit(parsed[2])

                if product_name not in ['string', 'any']:
                    return ValueError("put first parameter must be a string representing the product_name in {}".format(parsed))

                if amount not in ['number', 'any']:
                    return ValueError("put second parameter must be a number representing the amount dropped on the floor in {}".format(parsed))

                return 'void'

            elif action == 'moveStmt':
                return self.visit(parsed[1])

            elif action == 'moveStmt_0':
                row = self.visit(parsed[1])
                column = self.visit(parsed[2])

                if row not in ['number', 'any'] or column not in ['number', 'any']:
                    raise ValueError(
                        "Wrong parameter types in {}".format(parsed))

                return 'void'

            elif action == 'moveStmt_1':
                return 'void'

            elif action == 'buyStmt':
                return self.visit(parsed[1])

            elif action == 'buyStmt_0':
                seller_agent = self.visit(parsed[1])
                product_name = self.visit(parsed[2])
                buy_amount = self.visit(parsed[3])

                if seller_agent not in ['agent', 'any'] or product_name not in ['string', 'any'] or buy_amount not in ['number', 'any']:
                    raise ValueError(
                        "Wrong parameter types in {}".format(parsed))

                return 'void'

            elif action == 'buyStmt_1':
                seller_agent = self.visit(parsed[1])

                if seller_agent not in ['agent', 'any']:
                    raise ValueError(
                        "Buy function parameter must be an agent in {}".format(parsed))

                return 'void'

            elif action == 'talk':
                return 'void'

            elif action == 'random':
                low_lim = self.visit(parsed[1])
                sup_lim = self.visit(parsed[2])

                if low_lim not in ['number', 'any'] or sup_lim not in ['number', 'any']:
                    raise ValueError(
                        "Both parameters must be numbers in {}".format(parsed))

                return 'number'

            elif action == 'find':
                if parsed[1] == 'objects':
                    return 'book'
                return ('list', 'agent')

            elif action == 'primary_bool':
                return 'bool'
            elif action == 'primary_number':
                return 'number'
            elif action == 'primary_string':
                return 'string'
            elif action == 'primary_list':
                list_value = []
                for expr in parsed[1]:
                    list_value.append(self.visit(expr))

                if len(list_value) == 0:
                    raise Exception("List must not be empty.")

                for i in range(len(list_value)):
                    for j in range(len(list_value)):
                        if list_value[i] != list_value[j] and list_value[j] != 'any' and list_value[1] != 'any':
                            raise Exception(
                                "Every list element must be of the same type.")

                list_type = 'any'
                for i in range(len(list_value)):
                    if list_value[i] != 'any':
                        list_type = list_value[i]

                return ('list', list_type)

            elif action == 'primary_book':
                dict_value = {}
                for expr in parsed[1]:
                    dict_value[expr[0]] = self.visit(expr[1])

                if len(parsed[1]) == 0:
                    raise Exception("Book must not be empty.")

                return 'book'

            elif action == 'varDecl_0':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                if parsed[2] == "number":
                    instance = Number(0)
                elif parsed[2] == "bool":
                    instance = Bool(0)
                elif parsed[2] == "string":
                    instance = String("")
                else:
                    raise Exception(
                        "List and Book variables must be declared with value")
                self.env.update({name: instance})
                return 'void'

            elif action == 'varDecl_1':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                value = self.visit(parsed[3])
                if (type(value) != tuple and value not in [parsed[2], 'any']) or (type(value) == tuple and value[0] not in [parsed[2], 'any']):
                    raise Exception(
                        "Declaration type and expression assignment do not match in {}".format(parsed))

                instance = None
                if parsed[2] == "number":
                    instance = Number(0)
                elif parsed[2] == "bool":
                    instance = Bool(0)
                elif parsed[2] == "string":
                    instance = String("")
                elif parsed[2] == "list":
                    instance = List(element_type=value[1], value=[])
                elif parsed[2] == "book":
                    instance = Book((1, 'list', 'number'), {})

                self.env.update({name: instance})

                return 'void'

            elif action == 'varAssign':
                var = self.visit(parsed[1])
                result = self.visit(parsed[2])
                if result != var and result != 'any' and var != 'any':
                    raise ValueError("Mismatching types in {0}".format(parsed))

                return 'void'

            elif action == 'repeatStmt':
                cond = self.visit(parsed[1])
                if cond not in ['bool', 'any']:
                    raise ValueError(
                        "Repeat statements must contain bool conditions in {}".format(parsed))

                self.env = Env(outer=self.env)

                self.check(parsed[2])  # Only checked once

                self.env = self.env.outer

                return 'void'

            elif action == 'foreachStmt':
                iterator_name = parsed[1]
                if iterator_name in self.env:
                    raise Exception(
                        "Iterator name must not match any previous variable name in {}".format(parsed))

                iterable = self.visit(parsed[2])
                if not ((type(iterable) == tuple and len(iterable) == 2 and iterable[0] == 'list') or (type(iterable) == str and iterable in ['book', 'any'])):
                    raise Exception(
                        "Unsupported iterable type: {0} in {1}".format(iterable, parsed))

                self.env = Env(outer=self.env)

                if(type(iterable) == str and iterable == 'book'):
                    self.env[iterator_name] = Entry({"product":"", "amount": Number(0), "price": Number(0)})
                else:
                    self.env[iterator_name] = Any()

                self.check(parsed[3])  # Only checked once

                self.env = self.env.outer

                return 'void'

            elif action == 'incaseStmt' or action == 'inothercaseStmt_0':  # in case and in other case general form
                cond = self.visit(parsed[1])
                if cond not in ['bool', 'any']:
                    raise Exception(
                        "Condition must be boolean expr: {}".format(parsed))

                self.check(parsed[1])

                return 'void'

            elif action == 'inothercaseStmt_1':  # otherwise
                self.check(parsed[1])
                return 'void'

            elif action == 'inothercaseStmt_2':  # empty inothercaseStmt
                return 'void'

            elif action in ['and', 'or']:
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result in ['bool', 'any'] and result2 in ['bool', 'any']:
                    return 'bool'
                raise Exception("unsupported operand type(s) for {3}: {0} and {1} in {2}".format(
                    result, result2, parsed, action))

            elif action in ['!=', '==']:
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result == result2 or result == 'any' or result2 == 'any':
                    return 'bool'
                raise Exception("unsupported operand type(s) for {3}: {0} and {1} in {2}".format(
                    result, result2, parsed, action))

            elif action in ['<', '<=', '>=', '>']:
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result in ['number', 'any'] and result2 in ['number', 'any']:
                    return 'bool'
                raise Exception("unsupported operand type(s) for {3}: {0} and {1} in {2}".format(
                    result, result2, parsed, action))

            elif action == '+':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result in ['string', 'any'] and result2 in ['string', 'any']:
                    return 'string'
                if result in ['number', 'any'] and result2 in ['number', 'any']:
                    return 'number'
                raise Exception("unsupported operand type(s) for {3}: {0} and {1} in {2}".format(
                    result, result2, parsed, action))

            elif action in ['-', '*', '/']:
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result in ['number', 'any'] and result2 in ['number', 'any']:
                    return 'number'
                raise Exception("unsupported operand type(s) for {3}: {0} and {1} in {2}".format(
                    result, result2, parsed, action))

            elif action == '!':
                result = self.visit(parsed[1])
                if result in ['bool', 'any']:
                    return 'bool'
                raise Exception(
                    "unsupported operand type(s) for logical negation: {0} in {1}".format(result, parsed))

            elif action == 'neg':
                result = self.visit(parsed[1])
                if result in ['number', 'any']:
                    return 'number'
                raise Exception(
                    "unsupported operand type(s) for negation: {0} in {1}".format(result, parsed))

            else:
                # If the production is not of one of the above types, then try this:
                if len(parsed) > 0 and type(parsed[0]) == tuple:
                    return self.check(parsed)

                raise Exception("Unknown production: {}".format(parsed))
