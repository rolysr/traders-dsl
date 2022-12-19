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
