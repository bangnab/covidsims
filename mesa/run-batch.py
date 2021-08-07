from model import *

nb_batches = 20
running_steps = 1000


def batch_run():
    model = CovidSimple()
    for step in range(running_steps):
        model.step()

    gini = model.datacollector.get_model_vars_dataframe()
    return gini


results = []
for i in range(nb_batches):
    print(f"Running iteration {i}...")
    results.append(batch_run())

nb_virus_defeated = sum(map(lambda x: x.tail(1)["infected"].values[0] < 1, results))
print(f"Percentage of times the virus was defeated: {100.0 * nb_virus_defeated / nb_batches}")
