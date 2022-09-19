from random import randint
from typing import List, Set, Optional, Tuple
from logging import info


class Graph:
    def __init__(self, is_oriented: bool, labels: Optional[List[str]], vectors: List[Set[Tuple[int, Optional[int]]]]):
        self.is_oriented = is_oriented
        self.labels = labels
        self.vectors = vectors
        self.is_oriented = is_oriented

    def add_vector(self, source: int, destination: int, weight: Optional[int]) -> bool:
        if source == destination:
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

    def dominating_set(self):
        info("")
        res = set()
        inverse_res = set(range(len(self.vectors)))
        match_node = inverse_res.copy()
        while match_node:
            max_node = -1
            max_ = -1
            for node in inverse_res:
                count = 1 if node in match_node else 0
                for children in self.vectors[node]:
                    if children[0] in match_node:
                        count += 1
                if count > max_:
                    max_ = count
                    max_node = node

            res.add(max_node)
            inverse_res.discard(max_node)
            match_node.discard(max_node)
            for children in self.vectors[max_node]:
                match_node.discard(children[0])
        return res

    def save(self, path: str):
        with open(path, "w") as f:
            f.write(f"{len(self.vectors)}\n")
            f.write(f"{ 'true' if self.is_oriented else 'false'}\n")
            for source, vectors in enumerate(self.vectors):
                for destination in vectors:
                    f.write(f"{source}->{destination}\n")

    @staticmethod
    def load(path: str):
        with open(path) as f:
            lines = f.readlines()
            nb_node = int(lines[0])
            is_oriented = lines[2].lower().strip() == "true"
            vector = [set() for _ in range(nb_node)]
            for i in range(2, len(lines)):
                line = lines[i]
                source, destination = line.strip().split("->")
                source, destination = int(source), int(destination)
                vector[source].add((destination, None))
            return Graph(is_oriented, None, vector)

    @staticmethod
    def generate_random(nb_node=None, nb_vector=None, is_oriented=False, is_not_oriented=False, is_weighted=False,
                        is_not_weighted=False) -> "Graph":
        if nb_node is None:
            nb_node = int(input("nb_node: "))
        if nb_vector is None:
            nb_vector = int(input("nb_vector: "))
        if not is_not_oriented and not is_not_oriented:
            is_oriented = input("is_oriented: [Y/n]") == "n"
        if not is_weighted and not is_not_weighted:
            is_weighted = input("is_weighted: [Y/n]") == "n"
        graph = Graph(is_oriented, None, [])
        info("Adding nodes")
        for _ in range(nb_node):
            graph.add_node()
        info("Adding vectors")
        for _ in range(nb_vector):
            while not graph.add_vector(randint(0, nb_node - 1), randint(0, nb_node - 1),
                                       randint(0, 100) if is_weighted else None):
                pass

        return graph
