from random import randint
from math import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, ceil, floor, sqrt, degrees, radians, log
from os.path import exists, dirname, join
from os import getenv
from src.traders_lexer import TradersLexer
from src.traders_parser import TradersParser
from backend.list import *
from backend.agent import *
from backend.basic_types import *
from backend.behavior import *
from backend.book import *
from backend.environment import *
from backend.env import *


class Process:
    """
    The main process the executes Traders Abstract Syntax Tree
    """

    def __init__(self, tree, filename="?", env={}):
        self.tree = tree
        self.file_path = filename
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=Env({}))
            env.update(_env)
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0
        self.types = {'int': int, 'float': float, 'string': str,
                      'bool': bool, 'list': list, 'dict': dict}
        self.rtypes = {int: 'int', float: 'float', str: 'string',
                       bool: 'bool', list: 'list', dict: 'dict'}
        self.actual_agent = None
        self.env_instance = None

    def run(self, tree=None, env={}):
        current_env = self.env
        result = None
        if env != {}:
            self.env = env
        if tree is None:
            for line in self.tree:
                try:
                    result = self.evaluate(line)
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
                    result = self.evaluate(line)
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

    def stringify(self, expr):
        """
        Preparing values for printing
        """
        if type(expr) in {Number, Bool, String}:
            return str(expr.value)
        if type(expr) == List:
            ans = "["
            for item in expr.value:
                ans += self.stringify(item)+", "
            ans += "]"
            return ans
        if type(expr) == Book:
            ans = "{"
            for item in expr.value.keys():
                ans += item+" : "+self.stringify(expr.value[item])+", "
            ans += "}"
            return ans
        elif expr is None:
            return "nil"
        return str(expr)

    def evaluate(self, parsed):
        """
        Evaluating a parsed tree/tuple/expression
        """
        if self.should_return:
            return None

        if type(parsed) != tuple:
            return parsed
        else:
            action = parsed[0]

            if action == 'behave':
                self.env.update({parsed[1]: Behavior(
                    name=parsed[1], statement_list=parsed[2])})
                return None

            elif action == 'agent':
                id = parsed[1]
                if id in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % id)

                body = parsed[2]

                self.env = Env(outer=self.env)

                self.env.update({'balance': Number(0)})
                self.env.update({'behavior': Behavior("unknown_behavior", ())})
                self.env.update({'on_keep': Book((1, 'list', 'number'), {})})
                self.env.update({'on_sale': Book((2, 'list', 'number'), {})})
                self.env.update(
                    {'location': List(element_type='number', value=[Number(0), Number(0)])})

                for varOp in body[1]:
                    if varOp[0] == 'varAssign':
                        self.evaluate(varOp)
                    else:
                        var_name = varOp[1]
                        if var_name in ['balance', 'on_keep', 'on_sale', 'behavior', 'location']:
                            raise AttributeError(
                                'Redeclaring default agent attributes.')
                        self.evaluate(varOp)

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
                return None

            elif action == 'env':
                id = parsed[1]
                if id in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % id)

                body = parsed[2]

                self.env = Env(outer=self.env)

                self.env.update({'rows': Number(1)})
                self.env.update({'columns': Number(1)})
                self.env.update({'number_iterations': Number(0)})
                self.env.update({'log': Bool(False)})
                self.env.update(
                    {'agents': List(element_type='agent', value=[])})

                for varOp in body[1]:
                    if varOp[0] == 'varAssign':
                        self.evaluate(varOp)
                    else:
                        raise AttributeError(
                            'Env data type does not allow attribute declaration.')  # for now

                environment = TradersEnvironment(rows=self.env['rows'],
                                                 columns=self.env['columns'],
                                                 number_iterations=self.env['number_iterations'],
                                                 log=self.env['log'],
                                                 agents=self.env['agents'])
                self.env = self.env.outer
                self.env.update({id: environment})
                return None

            elif action == 'runEnv':
                env_instance = self.env[parsed[1]]
                if env_instance.type != 'env':
                    raise Exception(
                        "Run statement must be called on an Environment instance.")

                iterations = self.evaluate(parsed[2])
                if iterations.type != 'number':
                    raise Exception("Iterations param must be a number.")

                agents = env_instance.agents.value
                self.env_instance = env_instance

                for iter in range(int(iterations.value)):
                    for agent in agents:
                        inner_context = Env()
                        actual_context = self.env

                        # building inner context
                        inner_context.update({'balance': agent.balance})
                        inner_context.update({'on_keep': agent.on_keep})
                        inner_context.update({'on_sale': agent.on_sale})
                        inner_context.update({'location': agent.location})
                        for attr in agent.attributes.keys():
                            inner_context.update(
                                {attr: agent.attributes[attr]})
                        # up to add extra predefined variables
                        self.env = deepcopy(inner_context)
                        self.actual_agent = agent

                        # print("xxx: {}".format(self.stringify(self.env['location'])))
                        # print(self.should_return)
                        self.run(agent.behavior.statement_list)

                        # up to code getting back to actual context
                        self.should_return = False
                        self.env = actual_context
                        self.actual_agent = None
                
                self.env_instance = None

            elif action == 'resetEnv':
                env_instance = self.env[parsed[1]]
                if env_instance.type != 'env':
                    raise Exception(
                        "Reset statement must be called on an Environment instance.")

                env_instance.reset()

            elif action == 'putEnv':
                # get object to add
                obj = None
                try:
                    obj = self.env[parsed[1]]
                except:
                    raise Exception("There is no instance for {} object.".format(parsed[1]))

                # get environment instance
                env_instance = self.env[parsed[2]]
                if env_instance.type != 'env':
                    raise Exception(
                        "Put statement must be called on an Environment instance.")

                # get location 
                row = self.evaluate(parsed[3])
                column = self.evaluate(parsed[4])

                # check if type is agent
                if obj.type == 'agent':
                    env_instance.add_agent(obj, row, column)

                # check if type is item
                if obj.type == 'item':
                    env_instance.add_item(obj, row, column)

            elif action == 'restart':
                # Copying changed variables
                for attr in ['balance','on_keep', 'on_sale', 'location']:
                    self.actual_agent.__dict__[attr] = deepcopy(self.env[attr])
                for attr in self.actual_agent.attributes.keys():
                    self.actual_agent.attributes[attr] = deepcopy(self.env[attr])

                inner_context = Env()
                actual_context = self.env

                # building inner context
                inner_context.update({'balance': self.actual_agent.balance})
                inner_context.update({'on_keep': self.actual_agent.on_keep})
                inner_context.update({'on_sale': self.actual_agent.on_sale})
                inner_context.update({'location': self.actual_agent.location})
                for attr in self.actual_agent.attributes.keys():
                    inner_context.update(
                        {attr: self.actual_agent.attributes[attr]})

                # up to add extra predefined variables
                self.env = deepcopy(inner_context)
                # print(self.stringify(self.actual_agent.location))
                # print(" ")

                self.run(self.actual_agent.behavior.statement_list)

                # up to code getting back to actual context
                self.should_return = True
                self.env = actual_context
                return None

            elif action == 'stop':
                self.should_return = True
                return None

            elif action == 'call':
                func = self.env.find(parsed[1])
                if isinstance(func, Number) or isinstance(func, Bool) or isinstance(func, String) or isinstance(func, List) or isinstance(func, Book) or isinstance(func, Entry) or isinstance(func, TradersAgent) or isinstance(func, TradersEnvironment):
                    return func.get(parsed[2], self)

                elif isinstance(func, Behavior):
                    return func
                raise Exception("Error while resolving {}.".format(parsed)) 

            elif action == 'sell':
                produt_name = parsed[1]
                amount = parsed[2]
                price = parsed[3]

                on_keep = self.env['on_keep']
                on_sale = self.env['on_sale']

                if produt_name not in on_keep.keys() or amount < 1 or amount > on_keep.get_amount(produt_name) or price < 0:
                    raise ValueError('Invalid values for sell operation')
                
                # update on_keep
                on_keep.set_amount(produt_name, on_keep.get_amount(produt_name) - amount)

                if produt_name in on_sale.keys():
                    amount = on_sale.get_amount(produt_name) + amount
                    price = min(price, on_sale.get_price(produt_name))

                on_sale.set_amount(produt_name, amount)
                on_sale.set_price(produt_name, price)

            elif action == 'moveStmt_0':
                try:
                    row = self.evaluate(parsed[1])
                    column = self.evaluate(parsed[2])

                    # check if valid move
                    if self.env_instance.is_valid_position(row, column):
                        location = List(element_type='number', value=[row, column])
                        self.env['location'] = location
                    else:
                        raise IndexError('Location out of range')
                except:
                    pass

            elif action == 'moveStmt_1':
                direction = parsed[1]
                location = deepcopy(self.env['location'])
                row = location[0].value
                column = location[1].value

                if direction == 'up':
                    location.value[0] = Number(row.value - 1)
                elif direction == 'left':
                    location.value[1] = Number(column.value - 1)
                elif direction == 'right':
                    location.value[1] = Number(column.value + 1)
                elif direction == 'down':
                    location.value[0] = Number(row.value + 1)
                else:
                    raise ValueError("Invalid move direction")
                
                if self.env_instance.is_valid_position(location.value[0], location.value[1]):
                    self.env['location'] = location
                else:
                    raise IndexError('Location out of range')

            elif action == 'talk':
                print(self.stringify(self.evaluate(parsed[1])))
                return None

            elif action == 'primary_bool':
                return Bool(parsed[1])
            elif action == 'primary_number':
                return Number(parsed[1])
            elif action == 'primary_string':
                return String(parsed[1])
            elif action == 'primary_list':
                list_value = []
                for expr in parsed[1]:
                    list_value.append(deepcopy(self.evaluate(expr)))

                if len(list_value) == 0:
                    raise Exception("List must not be empty.")

                for i in range(1, len(list_value)):
                    if list_value[i].type != list_value[0].type:
                        raise Exception(
                            "Every list element must be of the same type.")

                return List(list_value[0].type, list_value)

            elif action == 'primary_book':
                dict_value = {}
                for expr in parsed[1]:
                    dict_value[expr[0]] = self.evaluate(expr[1])

                if len(parsed[1]) == 0:
                    raise Exception("Book must not be empty.")
                element_type = (
                    len(dict_value[parsed[1][0][0]].value), )+dict_value[parsed[1][0][0]].type
                for p_name in dict_value.keys():
                    if (len(dict_value[p_name].value), )+dict_value[p_name].type != element_type:
                        raise Exception(
                            "Every book element must be of the same type.")

                return Book(element_type, dict_value)

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
                return None

            elif action == 'varDecl_1':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                value = self.evaluate(parsed[3])
                if not ((value.type in ["number", "bool", "string"] and value.type == parsed[2]) or value.type[0] == parsed[2]):
                    raise Exception(
                        "Declaration type and expression assignment does not match")
                self.env.update({name: value})
                return None

            elif action == 'varAssign':
                var = self.evaluate(parsed[1])
                result = self.evaluate(parsed[2])
                if result.type != var.type:
                    raise ValueError("Type of variable '{}' should be '{}' but instead got '{}'".format(
                        parsed[1], self.rtypes[var.type], self.rtypes[type(result)]))

                var.copy(result)
                return None

            elif action == 'repeatStmt':
                cond = self.evaluate(parsed[1])
                while isinstance(cond, Bool) and cond.value:
                    self.run(parsed[2])
                    cond = self.evaluate(parsed[1])
                return None

            elif action == 'foreachStmt':
                iterator_name = parsed[1]
                if iterator_name in self.env:
                    raise Exception(
                        "Iterator name must not match any previous variable name.")

                iterable = self.evaluate(parsed[2])
                if type(iterable) == Book:
                    iterable = convert_book_to_entry_list(iterable)
                elif type(iterable) == List:
                    iterable = iterable.value
                else:
                    raise Exception(
                        "Unsupported iterable type: {}.".format(iterable.type))

                for value in iterable:
                    actual_env_vars = list(self.env.keys())

                    self.env[iterator_name] = value
                    self.run(parsed[3])

                    to_erase = []
                    for var in self.env.keys():
                        if var not in actual_env_vars:
                            to_erase.append(var)
                    for var in to_erase:
                        self.env.pop(var)
                return None

            elif action == 'incaseStmt' or action == 'inothercaseStmt_0':  # in case and in other case general form
                cond = self.evaluate(parsed[1])
                if cond.type != 'bool':
                    raise Exception("condition must be boolean expr")

                if cond.value:
                    self.run(parsed[2])
                    return None
                else:
                    self.evaluate(parsed[3])
                    return None

            elif action == 'inothercaseStmt_1':  # otherwise
                self.run(parsed[1])
                return None

            elif action == 'inothercaseStmt_2':  # empty inothercaseStmt
                pass

            elif action == 'or':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'bool' and result2.type == 'bool':
                    return Bool(result.value or result2.value)
                raise Exception("unsupported operand type(s) for \'and\': {0} and {1}".format(
                    result.type, result2.type))

            elif action == 'and':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'bool' and result2.type == 'bool':
                    return Bool(result.value and result2.value)
                raise Exception("unsupported operand type(s) for \'and\': {0} and {1}".format(
                    result.type, result2.type))

            elif action == '!=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == result2.type:
                    return Bool(not (result.value == result2.value))
                raise Exception("unsupported operand type(s) for !=: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '==':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == result2.type:
                    return Bool(result.value == result2.value)
                raise Exception("unsupported operand type(s) for ==: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Bool(result.value < result2.value)
                raise Exception("unsupported operand type(s) for <: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '<=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Bool(result.value <= result2.value)
                raise Exception("unsupported operand type(s) for <=: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '>=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Bool(result.value >= result2.value)
                raise Exception("unsupported operand type(s) for >=: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Bool(result.value > result2.value)
                raise Exception("unsupported operand type(s) for >: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '+':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'string' and result2.type == 'string':
                    return String(result.value+result2.value)
                if result.type == 'number' and result2.type == 'number':
                    return Number(result.value+result2.value)
                raise Exception(
                    "unsupported operand type(s) for +: {0} and {1}".format(result.type, result2.type))

            elif action == '-':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Number(result.value-result2.value)
                raise Exception(
                    "unsupported operand type(s) for -: {0} and {1}".format(result.type, result2.type))

            elif action == '*':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Number(result.value*result2.value)
                raise Exception(
                    "unsupported operand type(s) for *: {0} and {1}".format(result.type, result2.type))

            elif action == '/':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == 'number' and result2.type == 'number':
                    return Number(result.value/result2.value)
                raise Exception(
                    "unsupported operand type(s) for /: {0} and {1}".format(result.type, result2.type))

            elif action == '!':
                result = self.evaluate(parsed[1])
                if result.type == 'bool':
                    return Bool(not result.value)
                raise Exception(
                    "unsupported operand type(s) for logical negation: {0}".format(result.type))

            elif action == 'neg':
                result = self.evaluate(parsed[1])
                if result.type == 'number':
                    return Number(-result.value)
                raise Exception(
                    "unsupported operand type(s) for negation: {0}".format(result.type))

            else:
                if len(parsed) > 0 and type(parsed[0]) == tuple:
                    return self.run(parsed)

                print(parsed)
                return None

    def import_contents(self, file_contents):
        lexer = TradersLexer()
        parser = TradersParser()
        tokens = lexer.tokenize(file_contents)
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()
        self.env.update(program.env)