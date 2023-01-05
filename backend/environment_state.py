from copy import deepcopy


class EnvironmentState:
    """
        A class that stores a certain state of an environment.
        It is mostly used for reset function on an environment
    """

    def __init__(self, rows, columns, number_iterations, agents, log, logger, matrix) -> None:
        """
            Class constructor
        """

        self.rows = deepcopy(rows)
        self.columns = deepcopy(columns)
        self.number_iterations = deepcopy(number_iterations)
        self.agents = deepcopy(agents)
        self.log = deepcopy(log)
        self.logger = deepcopy(logger)
        self.matrix = deepcopy(matrix)
