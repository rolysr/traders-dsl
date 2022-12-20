class List:
    def __init__(self, element_type, value) -> None:
        self.type = ("list", element_type)
        self.value = value
    
    def get(self, index):
        if len(self.value)>index:
            return self.value[index]
        raise Exception("List::get(): indexing out of range")

    def set(self, index, value):
        if len(self.value)>index and self.type[1]==value.type:
            self.value[index] = value
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