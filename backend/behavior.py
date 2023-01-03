class Behavior:
    """
        A behavior class that represents the actions
        an agent can do on an environment
    """

    def __init__(self, name, statement_list) -> None:
        """
            Class constructor
        """
        self.type = "behave"
        self.name = name
        self.statement_list = statement_list

    def copy(self, other):
        self.statement_list = other.statement_list
    
    def __eq__(self, other):
        ans = True
        ans&=self.statement_list == other.statement_list
        return ans

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return self
        raise Exception("{} does not have any attribute.".format(self))