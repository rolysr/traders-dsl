from random import randint
from math import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh ,ceil, floor, sqrt, degrees, radians, log
from os.path import exists, dirname, join
from os import getenv
from src.traders_lexer import TradersLexer
from src.traders_parser import TradersParser

def standard_library():
    """
    Function that generates a dictionary that contains all the basic functions
    """
    env = Env()
    env.update({
        'input': lambda prompt: input(prompt),
        'random': lambda max: randint(0, max),
        'is_float': lambda val: isinstance(val, float),
        'is_int': lambda val: isinstance(val, int),
        'is_string': lambda val: isinstance(val, str),
        'is_list': lambda val: isinstance(val, list),
        'is_bool': lambda val: isinstance(val, bool),
        'to_float': lambda val: float(val),
        'to_int': lambda val: int(val),
        'to_string': lambda val: str(val),
        'to_list': lambda val: list(val),
        'to_bool': lambda val: bool(val),
        'append': lambda lst, val: lst.append(val),
        'pop': lambda lst: lst.pop(),
        'pop_at': lambda lst, idx: lst.pop(idx),
        'extend': lambda lst1, lst2: lst1.extend(lst2),
        'len': lambda obj : len(obj),
        'sin': lambda val : sin(val),
        'cos': lambda val : cos(val),
        'tan': lambda val : tan(val),
        'asin': lambda val : asin(val),
        'acos': lambda val : acos(val),
        'atan': lambda val : atan(val),
        'sinh': lambda val : sinh(val),
        'cosh': lambda val : cosh(val),
        'tanh': lambda val : tanh(val),
        'ceil': lambda val : ceil(val),
        'floor': lambda val : floor(val),
        'abs': lambda val : abs(val),
        'sqrt': lambda val : sqrt(val),
        'pow': lambda base, exponent : pow(base, exponent),
        'deg': lambda val : degrees(val),
        'rad': lambda val : radians(val),
        'log': lambda val : log(val),
        'exit': lambda val : exit(val),
        'trim': lambda val : val.strip(),
        'split': lambda val, delimeter=" " : val.split(delimeter),
        'talk': lambda val : print(val),
    })
    return env


class Process:
    """
    The main process the executes Traders Abstract Syntax Tree
    """
    def __init__(self, tree, filename="?", env={}):
        self.tree = tree
        self.file_path = filename
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=standard_library())
            env.update(_env)
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0
        self.types  =  { 'int': int, 'float': float, 'string': str, 'bool': bool, 'list': list, 'dict': dict }
        self.rtypes = { int: 'int', float: 'float', str: 'string', bool: 'bool', list: 'list', dict: 'dict' }

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
        if type(expr) == dict:
            return str(expr)
        elif expr is None:
            return "nil"
        elif expr is True:
            return "true"
        elif expr is False:
            return "false"
        elif expr in self.rtypes:
            return self.rtypes[expr]
        return str(expr)

    def evaluate(self, parsed):
        """
        Evaluating a parsed tree/tuple/expression
        """
        if type(parsed) != tuple:
            return parsed
        else:
            action = parsed[0]
            print(action)

            if action == 'behavior':
                params = parsed[2]
                body = parsed[3]
                self.env.update({parsed[1]: Function(
                    self, params[1], body, self.env)})
                return None

            elif action == 'call':
                func = self.env.find(parsed[1])
                if isinstance(func, Value):
                    func = func.get()

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

            elif action == 'stop':
                result = self.evaluate(parsed[1])
                self.should_return = True
                return result

            elif action == 'var_define':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                result = self.evaluate(parsed[2])
                self.env.update({name: Value(result, type(result))})
                return None
            elif action == 'var_define_no_expr':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                self.env.update({name: Value(None, self.types[parsed[2]])})
                return None
            elif action == 'var_assign':
                if type(parsed[1]) is not tuple:
                    if parsed[1] not in self.env:
                        raise UnboundLocalError('Cannot assign to undefined variable \'%s\'' %
                              parsed[1])
                    result = self.evaluate(parsed[2])
                    var = self.env.find(parsed[1])
                    if type(result) != var.type:
                        raise ValueError("Type of variable '{}' should be '{}' but instead got '{}'".format(parsed[1], self.rtypes[var.type], self.rtypes[type(result)]))

                    # self.env.update({parsed[1]: result})
                    var.value = result
                    return None
                else:
                    var = self.evaluate(parsed[1][1])
                    index = self.evaluate(parsed[1][2])
                    value = self.evaluate(parsed[2])
                    var[index] = value
            elif action == 'in_case':
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                if parsed[3] is not None:
                    return self.evaluate(parsed[3])
            elif action == 'repeat_when':
                cond = self.evaluate(parsed[1])
                while cond:
                    self.evaluate(parsed[2])
                    cond = self.evaluate(parsed[1])
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
            elif action == '+':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result + result2
            elif action == '-':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result - result2
            elif action == '*':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result * result2
            elif action == '/':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result / result2
            elif action == '%':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result % result2
            elif action == '==':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result == result2
            elif action == '!=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result != result2
            elif action == '<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result < result2
            elif action == '>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result > result2
            elif action == '<=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result <= result2
            elif action == '>=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result >= result2
            elif action == '<<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result << result2
            elif action == '>>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result >> result2
            elif action == '&':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result & result2
            elif action == '^':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result ^ result2
            elif action == '|':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result | result2
            elif action == '~':
                result = self.evaluate(parsed[1])
                return ~result
            elif action == 'and':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result and result2
            elif action == 'or':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result or result2
            elif action == '!':
                result = self.evaluate(parsed[1])
                if result == True:
                    return False
                return True
            elif action == '?:':
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                return self.evaluate(parsed[3])
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
                raise TypeError("Type of parameter {} should be {} but got {}.".format(self.params[i][0], self.params[i][1], self.process.rtypes[type(args[i])]))
            params.append(self.params[i][0])
        return self.process.run(self.body, Env(params, args, self.env))
<<<<<<< HEAD

=======
        
>>>>>>> dev
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