from random import randint
from typing import List, Set, Optional, Tuple
from logging import info, debug


class Graph:
    def __init__(self, is_oriented: bool, labels: Optional[List[str]], vectors: List[Set[Tuple[int, Optional[int]]]]):
        self.is_oriented = is_oriented
        self.labels = labels
        self.vectors = vectors
        self.is_oriented = is_oriented

    def add_vector(self, source: int, destination: int, weight: Optional[int]) -> bool:
        # Check if the vector points to itself
        if source == destination:
            return False
        # Check if the vector already exists
        if (destination, weight) in self.vectors[source]:
            return False
        self.vectors[source].add((destination, weight))
        if not self.is_oriented:
            self.vectors[destination].add((source, weight))
        return True

    def add_node(self, label: Optional[str] = None) -> int:
        self.vectors.append(set())
        if self.labels is not None:
            self.labels.append(label)
        return len(self.vectors) - 1

    def dominating_set(self) -> Set[int]:
        info("[DOMINATING SET] Initializing...")
        res = set()
        inverse_res = set(range(len(self.vectors)))
        match_node = inverse_res.copy()
        info("[DOMINATING SET] Starting...")
        while match_node:
            max_node = -1
            max_ = -1
            debug(f"[DOMINATING SET] {len(match_node)} nodes not targeted")
            for node in inverse_res:
                count = 1 if node in match_node else 0
                # score = 0 if node is targeted else 1
                for children in self.vectors[node]:
                    # add 1 if the child is not targeted
                    if children[0] in match_node:
                        count += 1
                # compare the score
                if count > max_:
                    max_ = count
                    max_node = node
            debug(f"[DOMINATING SET] {max_node} is the best node, with {max_} children targeted")
            # add the node to the result
            res.add(max_node)
            inverse_res.discard(max_node)
            match_node.discard(max_node)
            # remove the children in the not targeted nodes
            for children in self.vectors[max_node]:
                match_node.discard(children[0])
        debug(f"[DOMINATING SET] {len(res)} nodes in the dominating set")
        info("[DOMINATING SET] Done.")
        return res

    def save(self, path: str):
        info("[SAVE] Saving...")
        with open(path, "w") as f:
            info("[SAVE] Writing...")
            # write the number of nodes in first line, and if the graph is oriented in second line
            f.write(f"{len(self.vectors)}\n")
            f.write(f"{ 'true' if self.is_oriented else 'false'}\n")
            # write the vectors
            for source, vectors in enumerate(self.vectors):
                for destination in vectors:
                    f.write(f"{source}->{destination[0]}\n")
        info("[SAVE] Done.")

    @staticmethod
    def load(path: str) -> "Graph":
        info("[LOAD] Loading...")
        with open(path) as f:
            lines = f.readlines()
            info("[LOAD] Reading...")
            nb_node = int(lines[0])
            is_oriented = lines[2].lower().strip() == "true"
            info("[LOAD] nodes: %s, oriented: %s", nb_node, is_oriented)
            info("[LOAD] Creating...")
            vector = [set() for _ in range(nb_node)]
            for i in range(2, len(lines)):
                line = lines[i]
                source, destination = line.strip().split("->")
                source, destination = int(source), int(destination)
                vector[source].add((destination, None))
            info("[LOAD] Done.")
            return Graph(is_oriented, None, vector)

    @staticmethod
    def generate_random(nb_node=None, nb_vector=None, is_oriented=False, is_not_oriented=False, is_weighted=False,
                        is_not_weighted=False) -> "Graph":
        info("[RANDOM GRAPH] Initializing...")
        # If the parameters are not defined, they are asked to the user
        if nb_node is None:
            nb_node = int(input("nb_node: "))
        if nb_vector is None:
            nb_vector = int(input("nb_vector: "))
        if not is_not_oriented and not is_not_oriented:
            is_oriented = input("is_oriented: [Y/n]") == "n"
        if not is_weighted and not is_not_weighted:
            is_weighted = input("is_weighted: [Y/n]") == "n"
        graph = Graph(is_oriented, None, [])
        info("[RANDOM GRAPH] Adding nodes...")
        for _ in range(nb_node):
            graph.add_node()
        info("[RANDOM GRAPH] Adding vectors...")
        for _ in range(nb_vector):
            while not graph.add_vector(randint(0, nb_node - 1), randint(0, nb_node - 1),
                                       randint(0, 100) if is_weighted else None):
                pass
        info("[RANDOM GRAPH] Done.")
        return graph
