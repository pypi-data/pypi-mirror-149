"""

"""
import json
from roux.algo.geneweaver.kargers.types import AdjGraph, NodesAndEdges
from roux.algo.geneweaver.kargers.utils.transform import adj_graph_list_to_set, adj_graph_set_to_list

def save_graph(graph: AdjGraph, filepath: str) -> str:
    """

    :param graph:
    :param filepath:
    :return:
    """
    graph = adj_graph_set_to_list(graph)
    with open(filepath, 'w') as f:
        json.dump(graph, f)
    return filepath


def load_graph(filepath: str) -> AdjGraph:
    """

    :param filepath:
    :return:
    """
    with open(filepath, 'r') as f:
        graph = json.load(f)
    graph = adj_graph_list_to_set(graph)
    return graph


def load_nodes_edges(filepath: str) -> NodesAndEdges:
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['nodes'], data['edges']
