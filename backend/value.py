class Value(object):
    """
    Class container for values inside the Traders Language
    """

    def __init__(self, value, val_type):
        self.value = value
        self.type = val_type

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return "{}: {}".format(self.value, self.type)

    def get(self):
        return self.value