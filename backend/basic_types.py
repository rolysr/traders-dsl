class Number:
    def __init__(self, value: float) -> None:
        self.type = "number"
        self.value = value

    def copy(self, other):
        self.value = other.value

    def __eq__(self, other):
        ans = True
        ans &= self.value == other.value
        return ans

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return (self, (None, False))
        raise Exception("{} does not have any attribute.".format(self))

    def get_check(self, dotTail, process):
        if len(dotTail) == 0:
            return 'number'
        raise Exception("{} does not have any attribute.".format(self))


class String:
    def __init__(self, value: str) -> None:
        self.type = "string"
        self.value = value

    def copy(self, other):
        self.value = other.value

    def __eq__(self, other):
        ans = True
        ans &= self.value == other.value
        return ans

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return (self, (None, False))
        raise Exception("{} does not have any attribute.".format(self))

    def get_check(self, dotTail, process):
        if len(dotTail) == 0:
            return 'string'
        raise Exception("{} does not have any attribute.".format(self))


class Bool:
    def __init__(self, value: bool) -> None:
        self.type = "bool"
        self.value = value

    def __eq__(self, other):
        ans = True
        ans &= self.value == other.value
        return ans

    def copy(self, other):
        self.value = other.value

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return (self, (None, False))
        raise Exception("{} does not have any attribute.".format(self))

    def get_check(self, dotTail, process):
        if len(dotTail) == 0:
            return 'bool'
        raise Exception("{} does not have any attribute.".format(self))


class Any:
    def __init__(self) -> None:
        self.type = "any"

    def __eq__(self, other):
        return True

    def copy(self, other):
        pass

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return (self, (None, False))
        raise Exception("{} does not have any attribute.".format(self))

    def get_check(self, dotTail, process):
        if len(dotTail) == 0:
            return 'any'
        raise Exception("{} does not have any attribute.".format(self))
