from copy import deepcopy
from backend.behavior import Behavior
from backend.book import Book
from backend.list import List
from backend.basic_types import *


class TradersAgent:
    """
        A class that represents a trader agent
    """

    def __init__(self, balance: Number = Number(0),
                 behavior: Behavior = Behavior("unknown_behavior", ()),
                 on_keep: Book = Book((1, 'list', 'number'), {}),
                 on_sale: Book = Book((2, 'list', 'number'), {}),
                 location: List = List(element_type='number', value=[
                                       Number(0), Number(0)]),
                 attributes: dict = {}) -> None:
        """
            Class constructor
        """
        self.type = "agent"
        self.balance = deepcopy(balance)
        self.behavior = deepcopy(behavior)
        self.on_keep = deepcopy(on_keep)
        self.on_sale = deepcopy(on_sale)
        # location[0] is x coordinate and location[1] is y coordinate
        self.location = deepcopy(location)
        self.attributes = deepcopy(attributes)

    def buy_to_agent(self, agent):
        """
            A method for buying as much as possible to an agent
        """
        for item_name in agent.on_sale.value.keys():
            amount = agent.on_sale.get_amount(item_name).value
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

    def buy_item_to_agent(self, agent, name: str, amount: int):
        """
            Buys an item in a given amount to an specific agent
        """
        if amount < 1:
            return

        try:
            sale_price = agent.on_sale.get_price(name).value
            sale_amount = agent.on_sale.get_amount(name).vale
            final_amount = min(sale_amount, amount,
                               self.balance.value // sale_amount)

            if self.balance.value >= sale_price*amount or final_amount > 0:

                agent.on_sale.set_amount(
                    name, Number(sale_amount - final_amount))
                agent.balance.value += sale_price*amount

                if agent.on_sale.get_amount(name) == 0:
                    agent.on_sale.pop(name)

                self.balance.value -= sale_price*amount
                actual_amount = self.on_keep.get_amount(name).value
                self.on_keep.set_amount(
                    name, Number(actual_amount + final_amount))

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
        ans &= self.balance == other.balance
        ans &= self.behavior == other.behavior
        ans &= self.on_keep == other.on_keep
        ans &= self.on_sale == other.on_sale
        ans &= self.location == other.location
        ans &= self.attributes == other.attributes
        return ans

    def get(self, dotTail, process):
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
                ans = self.attributes[id]
            else:
                raise Exception(
                    "{} must be an attribute of {}".format(id, self))
        return ans.get(dotTail[2], process)
