from graph import Graph
import logging

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
graph = Graph.generate_random(is_not_oriented=True, nb_vector=15000, nb_node=1000, is_not_weighted=True)
# number of lines in the file is 2*nb_vector + 2 (x2 because the undirected graph is implemented as a directed graph)
graph.save("graph.txt")
# graph = Graph.load("graph.txt")
print("Result:", res := graph.dominating_set())
print("length:", len(res))
