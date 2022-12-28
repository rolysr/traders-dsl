from copy import deepcopy
from backend.environment_state import EnvironmentState
from backend.logger import Logger
from backend.basic_types import *
from backend.list import *


class TradersEnvironment:
    """
        A class for representing an
        environment where agents can move and
        trade among them 
    """

    def __init__(self, rows: Number = Number(1),
                 columns: Number = Number(1),
                 number_iterations: Number = Number(0),
                 log: Bool = Bool(False),
                 agents: List = List(element_type='agent', value=[])) -> None:
        """
            Class constructor
        """
        self.type = "env"
        self.rows = rows
        self.columns = columns
        self.number_iterations = number_iterations
        self.number_executed_iterations = 0
        self.agents = agents
        self.log = log
        self.logger = Logger()

        # create the world's internal representation
        self.matrix = {(i, j): [] for i in range(int(self.rows.value))
                       for j in range(int(self.columns.value))}

    def run(self, number_iterations):
        """
            Execute <number_iterations> iterations
            on the environment if possible
        """

        if number_iterations < 0 or number_iterations + self.number_executed_iterations > self.number_iterations:
            self.logger.log(
                "Invalid run execution. The number of iterations is not valid", self.log)

        self.reset_state = EnvironmentState(self.rows, self.columns, self.number_iterations,
                                            self.number_executed_iterations, self.agents, self.log, self.logger, self.matrix)

        # for each agent, execute its behavior, and return the updated world state
        for agent in self.agents:
            self.matrix = agent.behave(self.matrix)

        self.number_executed_iterations += number_iterations

    def reset(self):
        """
            Resets the environment to its initial state
        """
        self.rows = deepcopy(self.reset_state.rows)
        self.columns = deepcopy(self.reset_state.columns)
        self.number_iterations = deepcopy(self.reset_state.number_iterations)
        self.number_executed_iterations = deepcopy(
            self.reset_state.number_executed_iterations)
        self.agents = deepcopy(self.reset_state.agents)
        self.log = deepcopy(self.reset_state.log)
        self.logger = deepcopy(self.reset_state.logger)
        self.matrix = deepcopy(self.reset_state.matrix)

    def add_agent(self, agent, row, column):
        """
            A method that sets an agent on an
            environment in a given location
        """
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return

        self.agents.append(agent)
        self.matrix[(row, column)].append(agent)

    def add_item(self, item, row, column):
        """
            A method that sets an item on an
            environment in a given location
        """
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return

        self.matrix[(row, column)].append(item)

    def get(self, dotTail, process):
        if len(dotTail) == 0:
            return self
        id = dotTail[1][1]
        if id == "rows":
            ans = self.rows
        elif id == "columns":
            ans = self.columns
        elif id == "number_iterations":
            ans = self.number_iterations
        elif id == "agents":
            ans = self.agents
        elif id == "log":
            ans = self.log
        else:
            raise Exception("{} must be an attribute of {}".format(id, self))
        return ans.get(dotTail[2], process)
