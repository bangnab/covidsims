from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import random


class CovidAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model, infected):
        """
        Create a new Schelling agent.
        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           infected: Indicator for the agent's health
        """
        super().__init__(pos, model)
        self.pos = pos
        self.infected = infected
        self.infection_time = 0
        self.immune = False
        self.healing_time = 0

    def step(self):
        infected_neighbors = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.infected:
                infected_neighbors += 1

        # Immunity disappears after some time
        if self.immune and abs(self.infection_time - self.model.time) > self.model.immunization_time:
            self.immune = False
            self.model.immune -= 1

        # Chance of healing
        if self.infected and (self.model.random.random() < self.model.healing_rate):
            self.infected = False
            self.model.infected -= 1
            self.immune = True
            self.model.immune += 1

        # If too many infected neighbors, gets infected
        if not self.immune and infected_neighbors * self.model.infection_rate > self.model.random.random():
            self.infected = True
            self.model.infected += 1
            self.infection_time = self.model.time


class CovidSimple(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, density=0.8, healing_rate=0.05, infection_rate=0.1):
        """ """

        self.height = height
        self.width = width
        self.density = density
        self.healing_rate = healing_rate
        self.infection_rate = infection_rate
        self.time = 0
        self.immunization_time = 100

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.infected = 0
        self.immune = 0
        self.datacollector = DataCollector(
            {"infected": "infected"},  # Model-level count of happy agents
        #    {"immune": "immune"},
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            already_infected = self.random.random() < self.density
            agent = CovidAgent((x, y), self, already_infected)
            self.grid.position_agent(agent, (x, y))
            self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model.
        """
        self.infected = 0  # Reset counter of happy agents
        self.immune = 0
        self.time += 1
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)


