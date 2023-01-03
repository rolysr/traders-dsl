from copy import deepcopy
from backend.environment_state import EnvironmentState
from backend.logger import Logger
from backend.basic_types import *
from backend.list import *
from backend.book import *


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

        # create the world's internal representation for items on the ground
        self.matrix = {(i, j): Book((1, 'list', 'number'), {}) for i in range(int(self.rows.value))
                       for j in range(int(self.columns.value))}
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
        if self.is_valid_position(row, column):
            return

        agent.location = List(element_type='number', value=[row, column])
        self.agents.value.append(agent)

    def add_items(self, book: Book, row, column):
        """
            A method that sets an item on an
            environment in a given location
        """
        if self.is_valid_position(row, column):
            return

        # update items' amount on that position
        for item in book.keys():
            self.matrix[(row, column)].set_amount(item, book.get_amount(item))

    def find_peers(self, row, column):
        """
            Method for finding peers in a given location
        """
        if self.is_valid_position(row, column):
            return

        peers = [agent for agent in self.agents.value if agent.location.value[0] == row and agent.location.value[1] == column]
        return List(element_type='agent', value=peers)

    def find_objects(self, row, column):
        """
            Method for finding objects in a given location
        """
        if self.is_valid_position(row, column):
            return

        return self.matrix[(row, column)]

    def is_valid_position(self, row, column):
        """
            Check if the given location is 
            valid on the current environment.
        """
        return 0 <= row.value < self.rows.value and 0 <= column.value < self.columns.value

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