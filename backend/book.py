from backend.list import *
from backend.basic_types import *


class Book:
    def __init__(self, value_type, value: dict()) -> None:
        """
            The value_types can be:
            - (1, list, number): a list of one element of type number, this number should
            mean amount.
            - (2, list, number): a list of two elements of type number, the first number 
            should mean amount and the second the price.
        """
        self.type = ("book", value_type)
        # must be a dictionary of str : list of instances of basic types
        self.value = value

    def get_amount(self, product):
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        return self.value[product].get(0)

    def get_price(self, product):
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        return self.value[product].get(1)

    def set_amount(self, product, amount):
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        self.value[product].set(0, amount)

    def set_price(self, product, price):
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        self.value[product].set(1, price)
