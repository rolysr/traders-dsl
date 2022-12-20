from backend.item import Item
from backend.offer import Offer

class Agent:
    """
        A class that represents a trader agent
    """

    def __init__(self, name, balance, behavior, on_keep, on_sale, location, attributes) -> None:
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
        self.attributes = attributes

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
