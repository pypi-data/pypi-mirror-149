import random
from typing import Dict, Set

def kragers_poc_1(graph_al: Dict[int, Set[int]]):

    STOP_CONST = 2
    MAX = 10
    counter = 0
    # print("Start: ", graph_al)

    meta = {k: k for k in graph_al.keys()}

    while len(graph_al) > STOP_CONST and counter < MAX:
        key = random.choice(list(graph_al.keys()))
        print(key)
        to_merge: Set[int] = set()

        if len(graph_al[key]) > 0:
            edge_node = random.choice(list(graph_al[key]))

            if edge_node != key:
                print(f'Merging {edge_node}')
                edges_to_merge = graph_al.get(edge_node, set())
                to_merge.update(edges_to_merge)
                meta[edge_node] = key

                print(f"to_merge ")

                try:
                    del graph_al[edge_node]
                except KeyError:
                    continue
            else:
                print('edge is key (self loop)')

            graph_al[key].update(to_merge)
            graph_al[key].discard(key)
            for key, values in graph_al.items():
                graph_al[key] = {meta[v] for v in values if meta[v] != key}

        # print("End: ", graph_al, len(graph_al), meta)
        counter += 1
