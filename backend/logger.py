class Logger:
    """
        A class representing a logger
    """

    def __init__(self) -> None:
        """
            Class constructor
        """

        self.history = []

    def log(self, text, to_print_text):
        """
            Log function prints the given <text>
            if <to_print_text> is True
        """
        if to_print_text:
            print(text)

        self.history.append(text)
