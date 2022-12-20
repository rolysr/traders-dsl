class Item:
    """
        A class that represents an item
        for trading processes
    """

    def __init__(self, name, amount) -> None:
        """
            Class contructor
        """
        self.type = "item"
        self.name = name
        self.amount = amount