from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter                                               
from model import CovidSimple


class InfectedElement(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "Infected agents: " + str(model.infected)


class ImmuneElement(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        return "Immune agents: " + str(model.immune)


def covid_draw(agent):
    # 1
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    # 2
    if agent.infected:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    elif agent.immune:
        portrayal["Color"] = ["#00FFFF", "#99FFFF"]
        portrayal["stroke_color"] = "#0000F0"
    else:
        portrayal["Color"] = ["#00000F", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    return portrayal


# 3
infected_element = InfectedElement()
immune_element = ImmuneElement()
canvas_element = CanvasGrid(covid_draw, 20, 20, 500, 500)
infected_chart = ChartModule([{"Label": "infected", "Color": "Black"}, {"Label": "immune", "Color": "Blue"}])

# 4
model_params = {
    "height": 20,
    "width": 20,
    "density": UserSettableParameter("slider", "Initial infection density", 0.01, 0.01, 0.5, 0.01),
    "infection_rate": UserSettableParameter("slider", "Infection rate", 0.1, 0.00, 1.0, 0.05),
    "healing_rate": UserSettableParameter("slider", "Healing rate", 0.05, 0.00, 1.0, 0.01),
    "immunization_time": UserSettableParameter("slider", "Immunization time", 100, 1, 1000, 5)
}

# 5
server = ModularServer(CovidSimple,
                       [canvas_element, infected_element, immune_element, infected_chart],
                       "CovidSimple", model_params)

