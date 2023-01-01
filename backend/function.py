from backend.env import Env


class Function(object):
    """
    Function object for Traders Functions
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