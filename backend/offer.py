from backend.item import Item


class Offer:
    """
        A class that represents an item
        for trading processes
    """

    def __init__(self, name, price, amount) -> None:
        """
            Class contructor
        """
        self.type = "offer"
        self.item = Item(name, amount)
        self.price = price