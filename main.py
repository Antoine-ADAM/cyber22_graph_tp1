from graph import Graph

graph = Graph.generate_random(is_not_oriented=True, nb_vector=15000, nb_node=1000, is_not_weighted=True)
# graph = Graph.load("test")
print(res := graph.dominating_set())
print(len(res))
