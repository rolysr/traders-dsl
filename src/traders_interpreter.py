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
from backend.offer import *


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
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
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
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
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
        if type(parsed) != tuple:
            return parsed
        else:
            action = parsed[0]
            # print(action)

            if action == 'behavior':
                params = parsed[2]
                body = parsed[3]
                self.env.update({parsed[1]: Function(
                    self, params[1], body, self.env)})
                return None

            elif action == 'call':
                func = self.env.find(parsed[1])
                if isinstance(func, Number) or isinstance(func, Bool) or isinstance(func, String) or isinstance(func, List) or isinstance(func, Book):
                    return func

                elif not isinstance(func, Function):
                    if type(func) == type(lambda x: x):
                        args = [self.evaluate(arg) for arg in parsed[2][1]]
                        self.depth += 1
                        res = func(*args)
                        self.depth -= 1
                        return res
                    else:
                        raise ValueError('\'%s\' not a function' % parsed[1])

                args = [self.evaluate(arg) for arg in parsed[2][1]]
                self.depth += 1
                res = func(*args)
                self.depth -= 1
                return res

            elif action == 'talk':
                print(self.stringify(self.evaluate(parsed[1])))
                return None
            elif action == 'stop':
                self.should_return = True
                return None

            elif action == 'primary_bool':
                return Bool(parsed[1])
            elif action == 'primary_number':
                return Number(parsed[1])
            elif action == 'primary_string':
                return String(parsed[1])
            elif action == 'primary_list':
                list_value = []
                # print(parsed[1])
                for expr in parsed[1]:
                    list_value.append(self.evaluate(expr))

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
                            "Every dict element must be of the same type.")

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
                # print(parsed)
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                value = self.evaluate(parsed[3])
                # print(value.type)
                if not ((value.type in ["number", "bool", "string"] and value.type == parsed[2]) or value.type[0] == parsed[2]):
                    raise Exception(
                        "Declaration type and expression assignment does not match")
                self.env.update({name: value})
                return None
            elif action == 'varAssign':
                # print(parsed)

                var = self.evaluate(parsed[1])
                result = self.evaluate(parsed[2])
                if result.type != var.type:
                    raise ValueError("Type of variable '{}' should be '{}' but instead got '{}'".format(
                        parsed[1], self.rtypes[var.type], self.rtypes[type(result)]))
                # print(result.value)
                # self.env.update({parsed[1]: result})
                var.copy(result)
                return None
            elif action == 'repeatStmt':
                cond = self.evaluate(parsed[1])
                if cond.type != 'bool':
                    raise Exception("Cannot cast from {} to Bool".format(cond.type))
                while cond.value:
                    self.run(parsed[2])
                    cond = self.evaluate(parsed[1])
                return None
            elif action == 'foreachStmt':
                iterator_name = parsed[1]
                if iterator_name in self.env:
                    raise Exception("Iterator name must not match any previous variable name.")
                iterable = self.evaluate(parsed[2])
                if type(iterable) == Book:
                    iterable = convert_book_to_entry_list(iterable)
                elif type(iterable) == List:
                    iterable = iterable.value
                else:
                    raise Exception("Unsupported iterable type: {}.".format(iterable.type))
                for value in iterable:
                    actual_env = deepcopy(self.env)
                    self.env[iterator_name] = value
                    self.run(parsed[3])
                    self.env = actual_env
                return None
            elif action == 'incaseStmt' or action == 'inothercaseStmt_0': #in case and in other case general form
                cond = self.evaluate(parsed[1])
                if cond.type != 'bool':
                    raise Exception("condition must be boolean expr")
                if cond.value:
                    self.run(parsed[2])
                    return None
                else:
                    self.evaluate(parsed[3])
                    return None
            elif action == 'inothercaseStmt_1': #otherwise
                self.run(parsed[1])
                return None
            elif action == 'inothercaseStmt_2': #empty inothercaseStmt
                pass
            elif action == 'condition':
                return self.evaluate(parsed[1])
            elif action == 'block':
                return self.run(parsed[1])
            elif action == 'var':
                var = self.env.find(parsed[1])
                if not isinstance(var, Value):
                    return var
                return var.value
            elif action == 'indexing':
                var = self.evaluate(parsed[1])
                index = self.evaluate(parsed[2])
                if index > len(var):
                    raise IndexError('Index out of bounds error')
                    return None
                elif type(index) != int:
                    raise IndexError('List indices must be integers')
                    return None
                return var[index]
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
                    return Bool(not (result == result2))
                raise Exception("unsupported operand type(s) for !=: {0} and {1}".format(
                    result.type, result2.type))
            elif action == '==':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                if result.type == result2.type:
                    return Bool(result == result2)
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
            elif action == '.':
                if type(parsed[1]) == tuple:
                    var = self.evaluate(parsed[1])
                else:
                    var = self.env.find(parsed[1])
                if isinstance(var, Value):
                    res = self.evaluate(var.value[parsed[2]])
                else:
                    res = self.evaluate(var[parsed[2]])
                return res

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


class Env(dict):
    """
    Environment Class
    """

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, name):
        if name in self:
            return self[name]
        elif self.outer is not None:
            return self.outer.find(name)

        raise UnboundLocalError("{} is undefined".format(name))


class Function(object):
    """
    Function object for O Functions and annoymous functions (lambdas)
    """

    def __init__(self, process, params, body, env):
        self.process, self.params, self.body, self.env = process, params, body, env
        self.type = 'function'

    def __call__(self, *args):
        params = []
        for i in range(len(self.params)):
            if type(args[i]) != self.process.types[self.params[i][1]]:
                raise TypeError("Type of parameter {} should be {} but got {}.".format(
                    self.params[i][0], self.params[i][1], self.process.rtypes[type(args[i])]))
            params.append(self.params[i][0])
        return self.process.run(self.body, Env(params, args, self.env))


class Value(object):
    """
    Class container for values inside the Traders Language
    """

    def __init__(self, value, val_type):
        self.value = value
        self.type = val_type

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return "{}: {}".format(self.value, self.type)

    def get(self):
        return self.value
