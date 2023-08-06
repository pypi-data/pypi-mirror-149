"""

"""
from typing import Tuple, List, Dict

from roux.algo.geneweaver.kargers.types import GsidSet, AdjGraph, AdjGraphList, \
    EdgeList, \
    NodeList


def query_result_to_set(result) -> GsidSet:
    """

    :param result:
    :return:
    """
    return {r[0] for r in result}


def adj_graph_set_to_list(graph: AdjGraph) -> AdjGraphList:
    """

    :param graph:
    :return:
    """
    return {k: list(v) for k, v in graph.items()}


def adj_graph_list_to_set(graph: AdjGraphList) -> AdjGraph:
    """

    :param graph:
    :return:
    """
    return {int(k): {int(v) for v in vs} for k, vs in graph.items()}


def adj_graph_to_edge_list(graph: AdjGraph) -> Tuple[NodeList, EdgeList]:
    """

    :param graph:
    :return:
    """
    return ([int(n) for n in graph.keys()],
            [(int(source_node), int(dest_node))
             for source_node, edges in graph.items()
             for dest_node in edges])


def deduplicate_edge_list(edge_list: EdgeList) -> EdgeList:
    result = []
    seen = set()

    for edge in edge_list:
        if edge[0] != edge[1]:
            if edge not in seen and tuple(reversed(edge)) not in seen:
                seen.add(edge)
                result.append(edge)

    return result


def union_find_to_geneset_list(roots: List[int],
                               non_roots: Dict[int, int]) -> List[List[int]]:
    temp = {root: [root] for root in roots}
    for member, root in non_roots.items():
        temp[root].append(member)

    return list(temp.values())


def split_adj_graph(graph: AdjGraph, node_sets: List[List[int]]) -> List[AdjGraph]:
    return [{node: graph[int(node)] for node in node_set} for node_set in node_sets]


def remove_nodes(edges: EdgeList, node):
    res = []
    for edge in edges:
        if edge[0] != node and edge[1] != node:
            res.append(edge)
    return res

def remove_node_adj_graph(graph: AdjGraph, node):
    for key, value_list in graph.items():
        if key == node:
            del graph[key]
        else:
            graph[key] = {v for v in value_list if v != node}


def remove_edge_adj_graph(graph: AdjGraph, edge: Tuple[int, int]):
    try:
        graph[edge[0]].remove(edge[1])
    except KeyError:
        pass

    try:
        graph[edge[1]].remove(edge[0])
    except KeyError:
        pass

