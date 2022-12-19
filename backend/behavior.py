class Behavior:
    """
        A behavior class that represents the actions
        an agent can do on an environment
    """

<<<<<<< HEAD
    def __init__(self, name, statement_list) -> None:
        """
            Class constructor
        """
        self.type = "behave"
        self.name = name
        self.statement_list = statement_list
=======
    def __init__(self, name) -> None:
        """
            Class constructor
        """
        
        self.name = name
        self.agent = None
        self.matrix = None
        self.function = None

    def execute(self):
        return self.function(self.agent, self.matrix)
>>>>>>> dev
