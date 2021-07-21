from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


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

    def step(self):
        self.model.agent_step(self)


class CovidSimple(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, density=0.8, healing_rate=0.05, infection_rate=0.1, immunization_time=100):
        """ """

        self.height = height
        self.width = width
        self.density = density
        self.healing_rate = healing_rate
        self.infection_rate = infection_rate
        self.time = 0
        self.immunization_time = immunization_time

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.infected = 0
        self.immune = 0
        self.datacollector = DataCollector(
            {"infected": "infected", "immune": "immune"},  # Model-level count of agents
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
            if already_infected:
                self.infected += 1
            self.grid.position_agent(agent, (x, y))
            self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def agent_step(self, agent):
        infected_neighbors = 0
        for neighbor in self.grid.neighbor_iter(agent.pos):
            if neighbor.infected:
                infected_neighbors += 1

        # Immunity disappears after some time
        if agent.immune and abs(agent.infection_time - self.time) > self.immunization_time:
            agent.immune = False
            self.immune -= 1

        # Chance of healing
        if agent.infected and (self.random.random() < self.healing_rate):
            agent.infected = False
            self.infected -= 1
            agent.immune = True
            self.immune += 1

        # If too many infected neighbors, gets infected
        if not agent.immune and not agent.infected and infected_neighbors * self.infection_rate > self.random.random():
            agent.infected = True
            self.infected += 1
            agent.infection_time = self.time

    def step(self):
        """
        Run one step of the model.
        """
        self.time += 1
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)


