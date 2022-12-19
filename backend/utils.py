class Number:
    def __init__(self, value) -> None:
        self.type = "number"
        self.value = value

class String:
    def __init__(self, value) -> None:
        self.type = "string"
        self.value = value

class Bool:
    def __init__(self, value) -> None:
        self.type = "bool"
        self.value = value

class List:
    def __init__(self, element_type, value) -> None:
        self.type = "list"
        self.element_type = element_type
        self.value = value

class Book:
    def __init__(self, value) -> None:
        self.type = "book"
        self.value = value
