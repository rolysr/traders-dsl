class TradersVisitor:
    """
        Base class for a visitor implementation
    """

    def __init__(self, node_type) -> None:
        self.node_type = node_type

    def visit(self, node):
        pass