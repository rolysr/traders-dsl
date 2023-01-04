from backend.basic_types import *

class List:
    def __init__(self, element_type, value) -> None:
        self.type = ("list", element_type)
        self.value = value

    def set(self, index, value):
        if len(self.value)>index and self.type[1]==value.type:
            self.value[index] = value
            return 
        raise Exception("List::set(): indexing out of range or different type of value")

    def push(self, element):
        if element.type == self.type[1]:
            self.value.append(element)
        else:
            raise Exception("List::push(): the element is not of the list type")
        
    def size(self):
        return len(self.value)
    
    def pop(self):
        if len(self.value)>0:
            self.value.pop(len(self.value)-1)
        else:
            raise Exception("List::pop(): list empty")
    
    def reverse(self):
        self.value.reverse()
    
    def copy(self, other):
        self.type = other.type
        self.value = other.value

    def __eq__(self, other):
        ans = True
        ans&=self.type == other.type
        ans&=self.value == other.value
        return ans
    
    def get(self, dotTail, process = None):
        if process == None:
            index = dotTail
            if len(self.value) > index:
                return self.value[index]
            raise Exception("List::get(): indexing out of range")

        if len(dotTail) == 0:
            return (self, (None, False))

        ans = None
        if dotTail[1][0] == 'idTail_1': 
            listFunc = dotTail[1][1][0]
            if listFunc == 'size':
                ans = Number(len(self.value))

            elif listFunc == 'get':
                index = process.evaluate(dotTail[1][1][1])
                if index.type != 'number':
                    raise Exception("Index value must be a number.")
                index = int(index.value)
                if len(self.value) <= index:
                    Exception("Invalid index: Out of range.")
                if index < 0:
                    Exception("Invalid index: Negative index.")
                ans = self.value[index]

            elif listFunc == 'push':
                self.push(process.evaluate(dotTail[1][1][1]))
                ans = self

            elif listFunc == 'pop':
                self.pop()
                ans = self
                
            elif listFunc == 'reverse':
                self.reverse()
                ans = self
        else:
            raise Exception("{} must be an attribute of {}".format(id, self))
        return ans.get(dotTail[2], process)