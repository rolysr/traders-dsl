from backend.behavior import Behavior
from backend.book import Book
from backend.item import Item
from backend.offer import Offer

class TradersAgent:
    """
        A class that represents a trader agent
    """

    def __init__(self, name : str ="", balance : float = 0.0, behavior : Behavior=Behavior("unknown_behavior", []), on_keep : Book=Book((1, 'list', 'number'), {}), on_sale : Book=Book((2, 'list', 'number'), {}), location : tuple()=(-1, -1), attributes : dict={}) -> None:
        """
            Class constructor
        """
        self.type = "agent"
        self.name = name
        self.balance = balance
        self.behavior = behavior
        self.on_keep = on_keep
        self.on_sale = on_sale
        self.location = location 

        # add attributes to the agent's instace
        # attr = (key, value)
        for key in attributes.keys():
            self.__dict__[key] = attributes[key]

    def buy_to_agent(self, agent):
        """
            A method for buying as much as possible to an agent
        """
        for item_name in agent.on_sale.value.keys():
            amount = agent.on_sale.get_amount(item_name)
            self.buy_item_to_agent(agent, item_name, amount)

    def pick_item(self, name, amount):
        """
            Puts on keep an item
        """
        if amount < 1:
            return

        try:
            self.on_keep[name][0] += amount
        except:
            self.on_keep[name] = [amount]

    def drop_item(self, name, amount):
        """
            Drops an item with a given name and an amount
        """
        if amount < 1:
            return

        try:
            if self.on_keep[name][0] >= amount:
                self.on_keep[name][0] -= amount
        except:
            pass

    def buy_item_to_agent(self, agent, name, amount):
        """
            Buys an item in a given amount to an specific agent
        """
        if amount < 1:
            return

        try:
            sale_price = agent.on_sale[name][1]
            sale_amount = agent.on_sale[name][0]
            final_amount = min(sale_amount, amount,
                               self.balance // sale_amount)

            if self.balance >= sale_price*amount or final_amount > 0:

                agent.on_sale[name][0] -= amount
                agent.balance += sale_price*amount

                if agent.on_sale[name][0] == 0:
                    agent.on_sale.pop(name)
                self.balance -= sale_price*amount

                try:
                    self.on_keep[name][0] += amount
                except:
                    self.on_keep[name] = [amount]

        except:
            pass

    def copy(self, other):
        self.balance = other.balance
        self.behavior = other.behavior
        self.on_keep = other.on_keep
        self.on_sale = other.on_sale
        self.location = other.location  
        self.attributes = other.attributes
    
    def __eq__(self, other):
        ans = True
        ans&=self.balance == other.balance
        ans&=self.behavior == other.behavior
        ans&=self.on_keep == other.on_keep
        ans&=self.on_sale == other.on_sale
        ans&=self.location == other.location  
        ans&=self.attributes == other.attributes
        return ans
    
    def get(self, dotTail):
        if len(dotTail) == 0:
            return self
        id = dotTail[1][1]
        if id == "balance":
            ans = self.balance
        elif id == "behavior":
            ans = self.behavior
        elif id == "on_keep":
            ans = self.on_keep
        elif id == "on_sale":
            ans = self.on_sale
        elif id == "location":
            ans = self.location
        else:
            if id in self.attributes:
                ans=self.attributes[id]
            else:
                raise Exception("{} must be an attribute of {}".format(id, self))
        return ans.get(dotTail[1][2])