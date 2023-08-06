import logging
from typing import Optional, Dict

from roux.algo.geneweaver.kargers.krager_min_cut import KargerMinCut
from roux.algo.geneweaver.kargers.types import AdjGraph
from roux.algo.geneweaver.kargers.utils import transform as tf
from roux.algo.geneweaver.kargers.utils import load_save_graph as ls


def meta_kargers(graph: AdjGraph, max_level: Optional[int] = None):

    n_levels_max = max_level or 5
    logging.info(f"Starting meta run with {n_levels_max} levels.")
    store: Dict[str, dict] = {'0': {'parent': graph}}
    add_children(store, 0, n_levels_max)
    return store

def add_children(graphs, n, max_n):
    if n >= max_n:
        return
    n += 1

    logging.info(f"Starting level {n}")

    for idx, graph in graphs.items():
        logging.info(f"Starting graph {idx}")

        graph['children'] = {
            idx: {'parent': subgraph}
            for idx, subgraph in enumerate(split_graph_kargers(graph['parent']))
        }

        add_children(graph['children'], n, max_n)


def karger_wrap(graph: AdjGraph):
    nodes, edges = tf.adj_graph_to_edge_list(graph)
    edges = tf.deduplicate_edge_list(edges)

    kmc = KargerMinCut(nodes, edges)

    return kmc.min_cut()


def split_graph_kargers(graph: AdjGraph):
    min_cut, best_cuts, result = karger_wrap(graph)
    distinct_graphs = tf.split_adj_graph(graph,
                                         tf.union_find_to_geneset_list(result.roots(),
                                                                       result.non_roots()))
    if min_cut != 0:
        for cut in best_cuts:
            for d_graph in distinct_graphs:
                tf.remove_edge_adj_graph(d_graph, cut)
    return distinct_graphs


def demo_meta(graph_file: str):
    logging.getLogger().setLevel('INFO')
    logging.info("Loading graph file")
    graph = ls.load_graph(graph_file)
    return meta_kargers(graph, 3)
