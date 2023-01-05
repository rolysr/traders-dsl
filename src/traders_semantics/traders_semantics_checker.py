class TradersSemanticsChecker:
    """
        A class that represents an object
        oriented to semantics checking
    """

    def check_semantics(self, tree=None):
        """
            A method that computes the phases
            related to semantic checking
        """
        if tree is None:
            raise ValueError("Can not check semantics for a None program") 

        type_collector = TradersTypeCollectorVisitor()
        type_collector.visit(tree)

        type_builder = TradersTypeBuilderVisitor(context=type_collector.context)
        type_builder.visit(tree)

        type_checker = TradersTypeCheckerVisitor(context=type_builder.context)
        type_checker.visit(tree);