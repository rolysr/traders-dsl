from backend.item import Item
from backend.offer import Offer

class Agent:
    """
        A class that represents a trader agent
    """

    def __init__(self, name, balance, behavior) -> None:
        """
            Class constructor
        """
        self.name = name
        self.balance = balance
        self.behavior = behavior
        self.on_keep = {}
        self.on_sale = {}
        self.location = (-1, -1)  

    def buy_to_agent(self, agent):
        """
            A method for buying as much as possible to an agent
        """  
        for item_name in agent.on_sale.keys():
            amount = agent.on_sale[item_name].amount
            self.buy_item_to_agent(agent, item_name, amount)

    def pick_item(self, name, amount):
        """
            Puts on keep an item
        """
        if amount < 1:
            return

        try:
            self.on_keep[name].amount += amount
        except:
            self.on_keep[name] = Item(name, amount)

    def drop_item(self, name, amount):
        """
            Drops an item with a given name and an amount
        """
        if amount < 1:
            return

        try:
            if self.on_keep[name].amount >= amount:
                self.on_keep[name].amount -= amount
        except:
            pass

    def buy_item_to_agent(self, agent, name, amount):
        """
            Buys an item in a given amount to an specific agent
        """
        if amount < 1:
            return

        try:
            sale_price = agent.on_sale[name].price
            sale_amount = agent.on_sale[name].item.amount
            final_amount = min(sale_amount, amount, self.balance // sale_amount)

            if self.balance >= sale_price*amount or final_amount > 0:
                
                agent.on_sale[name].item.amount -= amount
                agent.balance += sale_price*amount

                if agent.on_sale[name].amount == 0:
                    agent.on_sale.pop(name)
                
                self.balance -= sale_price*amount

                try:
                    self.on_keep[name].amount += amount
                except:
                    self.on_keep[name] = Item(name, amount)

        except:
            pass