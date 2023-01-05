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

        self.call_owner = None
        self.is_protected = False

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
                    (ans, (self.call_owner, self.is_protected)
                     ) = func.get(parsed[2], self)
                    if self.actual_agent is not None:
                        if parsed[1] in ['balance', 'on_keep', 'on_sale', 'location']:
                            self.call_owner = self.actual_agent
                            self.is_protected = True
                        if parsed[1] in self.actual_agent.attributes.keys():
                            self.call_owner = self.actual_agent
                            self.is_protected = False
                    return (True, ans.type)

                raise Exception("Error while resolving {}.".format(parsed))

            elif action == 'behave':
                self.env.update({parsed[1]: Behavior(
                    name=parsed[1], statement_list=parsed[2])})
                return (True, 'void')

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
                        pass
                    else:
                        var_name = varOp[1]
                        if var_name in ['balance', 'on_keep', 'on_sale', 'behavior', 'location']:
                            raise AttributeError(
                                'Redeclaring default agent attributes.')

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
                return (True, ())

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
                        pass
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
                return (True, ())

            elif action == 'runEnv':
                env_instance = self.env[parsed[1]]
                if not isinstance(env_instance, TradersEnvironment):
                    raise Exception(
                        "Run statement must be called on an Environment instance.")

                iterations = env_instance.number_iterations
                if len(parsed) == 3:
                    pass
                if not isinstance(iterations, Number):
                    raise Exception("Iterations param must be a number.")

                env_instance.save()

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
                        self.env = inner_context
                        self.actual_agent = agent

                        # print("xxx: {}".format(self.stringify(self.env['location'])))
                        # print(self.should_return)

                        # up to code getting back to actual context
                        self.should_return = False
                        self.env = actual_context
                        self.actual_agent = None

                self.env_instance = None
                return (True, ())

            elif action == 'resetEnv':
                env_instance = self.env[parsed[1]]
                if env_instance.type != 'env':
                    raise Exception(
                        "Reset statement must be called on an Environment instance.")

                return (True, ())

            elif action == 'putEnv':
                # get object to add
                obj_result, obj_type = self.visit(parsed[2])

                if obj_result == False:
                    return (False, ())

                # get environment instance
                env_instance = self.env[parsed[1]]
                if env_instance.type != 'env':
                    raise Exception(
                        "Put statement must be called on an Environment instance.")

                # get location
                row = self.visit(parsed[3])
                column = self.visit(parsed[4])

                # check if type is agent or book
                if obj_type != "agent" and obj_type[0] != 'book':
                    raise ValueError("Invalid value to add to environment")
                
                return (True, ())

            elif action == 'restart':
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

                return (True, ())

            elif action == 'stop':
                self.should_return = True
                return (True, ())

            elif action == 'sell':
                produt_name = self.visit(parsed[1])
                amount = self.visit(parsed[2])
                price = self.visit(parsed[3])

                if not (isinstance(produt_name, String) and isinstance(amount, Number) and isinstance(price, Number)):
                    return ValueError('Invalid values for sell operation')

                return (True, ())

            elif action == 'pick':
                product_name = self.visit(parsed[1])

                if not isinstance(product_name, String):
                    return ValueError("pick function must receive a product name as a String.")

                return (True, ())

            elif action == 'put':
                product_name = self.visit(parsed[1])
                amount = self.visit(parsed[2])

                if not isinstance(product_name, String):
                    return ValueError("put first parameter must be a string representing the product_name.")

                if not isinstance(amount, Number):
                    return ValueError("put second parameter must be a number representing the amount dropped on the floor.")

                if amount.value < 0:
                    return ValueError("The dropped amount must not be negative.")

                return (True, ())

            elif action == 'moveStmt':
                return self.visit(parsed[1])

            elif action == 'moveStmt_0':
                try:
                    row = self.visit(parsed[1])
                    column = self.visit(parsed[2])

                    return (True, ())
                except:
                    raise Exception("Some error accoured when moving")

            elif action == 'moveStmt_1':
                return (True, ())

            elif action == 'buyStmt':
                return self.visit(parsed[1])

            elif action == 'buyStmt_0':
                seller_agent = self.visit(parsed[1])
                product_name = self.visit(parsed[2])
                buy_amount = self.visit(parsed[3])

                if not (isinstance(seller_agent, TradersAgent) and isinstance(product_name, String) and isinstance(buy_amount, Number)):
                    raise ValueError("buyStmt_0: Wrong parameter types.")

                return (True, ())

            elif action == 'buyStmt_1':
                seller_agent = self.visit(parsed[1])

                if not isinstance(seller_agent, TradersAgent):
                    raise ValueError(
                        "buy function parameter must be an agent.")

                return (True, ())

            elif action == 'talk':
                if  not self.env_instance is None and not self.env_instance.log.value:
                    raise ValueError("Invalid value to print")
                return (True, None)

            elif action == 'random':
                low_lim = self.visit(parsed[1])
                sup_lim = self.visit(parsed[2])

                if not (isinstance(low_lim, Number) and isinstance(sup_lim, Number)):
                    raise ValueError("random: Both parameters must numbers.")

                return (True, 'number')

            elif action == 'find':
                return (True, ())

            elif action == 'primary_bool':
                return (True, 'bool')
            elif action == 'primary_number':
                return (True, 'number')
            elif action == 'primary_string':
                return (True, 'string')
            elif action == 'primary_list':
                list_value = []
                for expr in parsed[1]:
                    list_value.append(deepcopy(self.visit(expr)))

                if len(list_value) == 0:
                    raise Exception("List must not be empty.")

                for i in range(1, len(list_value)):
                    if list_value[i].type != list_value[0].type:
                        raise Exception(
                            "Every list element must be of the same type.")

                return (True, list_value[0].type)

            elif action == 'primary_book':
                dict_value = {}
                for expr in parsed[1]:
                    dict_value[expr[0]] = self.visit(expr[1])

                if len(parsed[1]) == 0:
                    raise Exception("Book must not be empty.")
                element_type = (
                    len(dict_value[parsed[1][0][0]].value), )+dict_value[parsed[1][0][0]].type
                for p_name in dict_value.keys():
                    if (len(dict_value[p_name].value), )+dict_value[p_name].type != element_type:
                        raise Exception(
                            "Every book element must be of the same type.")

                return (True, 'book')

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
                return (True, instance.type)

            elif action == 'varDecl_1':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                value = self.evaluate(parsed[3])
                if not ((value.type in ["number", "bool", "string"] and value.type == parsed[2]) or value.type[0] == parsed[2]):
                    raise Exception(
                        "Declaration type and expression assignment does not match")
                self.env.update({name: value})
                return (True, ())

            elif action == 'varAssign':
                var = self.visit(parsed[1])

                owner = self.call_owner
                is_protected = self.is_protected

                if self.actual_agent is not None and owner is not None:  # Means we are inside a behave call
                    if owner is not self.actual_agent:
                        raise Exception(
                            'Illegal assignment, other agent assigment : {}'.format(parsed))
                    if is_protected:
                        raise Exception(
                            'Illegal assignment, protected attributes assignment : {}'.format(parsed))

                result = self.evaluate(parsed[2])
                if type(result) != type(var):
                    raise ValueError("Mismatching types in assignment.")

                var.copy(result)
                return (True, ())

            elif action == 'repeatStmt':
                cond = self.visit(parsed[1])
                if not isinstance(cond, Bool):
                    raise ValueError("Repeat statements must contain bool conditions")
                return (True, ())

            elif action == 'foreachStmt':
                iterator_name = parsed[1]
                if iterator_name in self.env:
                    raise Exception(
                        "Iterator name must not match any previous variable name.")

                iterable = self.visit(parsed[2])
                if type(iterable) == Book:
                    iterable = convert_book_to_entry_list(iterable)
                elif type(iterable) == List:
                    iterable = iterable.value
                else:
                    raise Exception(
                        "Unsupported iterable type: {}.".format(iterable.type))

                return (True, ())

            elif action == 'incaseStmt' or action == 'inothercaseStmt_0':  # in case and in other case general form
                cond = self.evaluate(parsed[1])
                if cond.type != 'bool':
                    raise Exception("condition must be boolean expr")

                return (True, ())

            elif action == 'inothercaseStmt_1':  # otherwise
                return (True, ())

            elif action == 'inothercaseStmt_2':  # empty inothercaseStmt
                return (True, ())

            elif action == 'or':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Bool) and isinstance(result2, Bool):
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for \'and\': {0} and {1}".format(
                    result.type, result2.type))

            elif action == 'and':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Bool) and isinstance(result2, Bool):
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for \'and\': {0} and {1}".format(
                    result.type, result2.type))

            elif action == '!=':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result is not None and result2 is not None and result.type == result2.type:
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for !=: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '==':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if result is not None and result2 is not None and result.type == result2.type:
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for ==: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '<':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Number) and isinstance(result2, Number):
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for <: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '<=':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Number) and isinstance(result2, Number):
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for <=: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '>=':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Number) and isinstance(result2, Number):
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for >=: {0} and {1}".format(
                    result.type, result2.type))

            elif action == '>':
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Number) and isinstance(result2, Number):
                    return (True, 'bool')
                raise Exception("unsupported operand type(s) for >: {0} and {1}".format(
                    result.type, result2.type))

            elif action in ['+']:
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, String) and isinstance(result2, String):
                    return (True, 'string')
                if isinstance(result, Number) and isinstance(result2, Number):
                    return (True, 'number')
                raise Exception(
                    "unsupported operand type(s) for +: {0} and {1}".format(result.type, result2.type))

            elif action in ['-', '*', '/']:
                result = self.visit(parsed[1])
                result2 = self.visit(parsed[2])
                if isinstance(result, Number) and isinstance(result2, Number):
                    return (True, 'number')
                raise Exception(
                    "unsupported operand type(s) for +: {0} and {1}".format(result.type, result2.type))

            elif action == '!':
                result = self.visit(parsed[1])
                if isinstance(result, Bool):
                    return (True, 'bool')
                raise Exception(
                    "unsupported operand type(s) for logical negation: {0}".format(result.type))

            elif action == 'neg':
                result = self.visit(parsed[1])
                if isinstance(result, Number):
                    return (True, 'number')
                raise Exception(
                    "unsupported operand type(s) for negation: {0}".format(result.type))

            else:
                # If the production is not of one of the above types, then try this:
                if len(parsed) > 0 and type(parsed[0]) == tuple:
                    return self.visit(parsed)

                print(parsed)
                return (True, ())

    def import_contents(self, file_contents):
        lexer = TradersLexer()
        parser = TradersParser()
        tokens = lexer.tokenize(file_contents)
        tree = parser.parse(tokens)
        program = TradersSemanticsChecker(tree)
        program.run()
        self.env.update(program.env)