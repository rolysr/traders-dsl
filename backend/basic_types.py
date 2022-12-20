class Number:
    def __init__(self, value: float) -> None:
        self.type = "number"
        self.value = value

class String:
    def __init__(self, value: str) -> None:
        self.type = "string"
        self.value = value

class Bool:
    def __init__(self, value: bool) -> None:
        self.type = "bool"
        self.value = value