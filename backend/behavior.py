class Behavior:
    """
        A behavior class that represents the actions
        an agent can do on an environment
    """

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