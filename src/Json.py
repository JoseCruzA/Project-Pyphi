import json
import pathlib
from PyphiClass import Pyphi
from Graph import Graph

file = open("assets/graphs.json", "r")
data = json.load(file)[0]

for i in data["graphs"]:
    graph = Graph()
    graph.create_graph(i)
    if len(graph.cm) > 0:
        for path in pathlib.Path('config').iterdir():
            if path.is_file():
                if "emd_bi.yml" in path.name or "emd_tri.yml" in path.name or "l1_bi.yml" in path.name:
                    pyphi = Pyphi(graph, path.name, True)
                    pyphi.calculate()
                pyphi = Pyphi(graph, path.name)
                pyphi.calculate()


file.close()