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
        ini_val = product
        try:
            product = product.value
        except:
            product = ini_val
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        return self.value[product].get(0)

    def get_price(self, product):
        ini_val = product
        try:
            product = product.value
        except:
            product = ini_val
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        return self.value[product].get(1)

    def set_amount(self, product, amount: Number):
        ini_val = product
        try:
            product = product.value
        except:
            product = ini_val
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        self.value[product].set(0, amount)

    def set_price(self, product, price: Number):
        ini_val = product
        try:
            product = product.value
        except:
            product = ini_val
        if product not in self.value.keys():
            if self.type[1][0] == 1:
                self.value[product] = List("number", [Number(0)])
            if self.type[1][0] == 2:
                self.value[product] = List("number", [Number(0), Number(0)])
        self.value[product].set(1, price)

    def copy(self, other):
        self.type = other.type
        self.value = other.value

    def __eq__(self, other):
        ans = True
        ans&=self.type == other.type
        ans&=self.value == other.value
        return ans

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return self
        raise Exception("{} does not have any attribute.".format(self))
    
class Entry:
    def __init__(self, attributes) -> None:
        self.attributes = attributes
    
    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return self
        id = dotTail[1][1]
        if id in self.attributes:
            if id == "product":
                ans = String(self.attributes[id])
            else:
                ans = self.attributes[id]
        else:
            raise Exception("{} must be an attribute of {}".format(id, self))
        return ans.get(dotTail[2], process)
    
def convert_book_to_entry_list(book: Book) -> list:
    ans = []
    for product in book.value.keys():
        attributes = dict()
        attributes["product"] = product
        amount = book.value[product].value[0]
        attributes["amount"] = amount
        if len(book.value[product].value) > 1:
            price = book.value[product].value[1]
            attributes["price"] = price
        ans.append(Entry(attributes))
    return ans