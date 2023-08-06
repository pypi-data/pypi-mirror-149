import copy
import logging
import random
import sys

from roux.algo.geneweaver.kargers.types import EdgeList, NodeList
from roux.algo.geneweaver.kargers.union_find import UnionFind


class KargerMinCut:
    N_NODES_STOP: int = 2

    def __init__(self, nodes: NodeList, edges: EdgeList, **kwargs):
        """

        :param nodes:
        :param edges:
        """
        self.edges: EdgeList = edges
        self.nodes: NodeList = nodes
        self.num_nodes: int = len(self.nodes)
        self.num_edges: int = len(self.edges)

        self.global_min_cut_edge = sys.maxsize
        self.best_union_find = None
        self.best_cuts = None

        # We need to run graph.V * graph.V * math.log(graph.V) times to get best results
        # self.max_runs = self.num_nodes ** 2 * math.log(self.num_nodes)
        self.max_runs = 10

        self.random_select_style = kwargs.get('random_select_style', 'pick')
        self.preserve_edge_list_order = kwargs.get('preserve_edge_list_order', False)
        self.always_find_all_cuts = kwargs.get('always_find_all_cuts', False)
        self.max_consecutive_mins = kwargs.get('max_consecutive_mins', None)

    def min_cut(self):
        """

        :return:
        """
        logging.info("Starting Karger's Min Cut")
        run = 0

        if self.preserve_edge_list_order:
            logging.info("Copying to preserve input order...")
            edges_copy = copy.deepcopy(self.edges)
        else:
            edges_copy = self.edges

        consc_gt_min = 0

        while run < self.max_runs:
            logging.info(f"Setting up run: {run + 1} of {self.max_runs}")

            logging.info("Shuffling...")
            random.shuffle(edges_copy)

            logging.info("Setting up union find")
            union_find = UnionFind(self.nodes)
            num_nodes = self.num_nodes

            logging.info(f"Starting Karger's run on {num_nodes} nodes")

            while num_nodes > self.N_NODES_STOP:
                # Randomly pick an edge
                # pick = random.choice(edges_copy)
                for pick in edges_copy:

                    # If two node are not int the same set, merge(contract) them
                    if union_find.find(pick[0]) != union_find.find(pick[1]):

                        # Hook for visualization / user feedback on node contraction
                        self.viz_contract_nodes_hook(pick[0], pick[1])

                        union_find.union(pick[0], pick[1])
                        num_nodes -= 1

                        if num_nodes <= self.N_NODES_STOP:
                            break
                break

            logging.info(f"Edge contraction completed, {num_nodes} remaining")

            min_cut_edge = 0
            cut_edges = []

            logging.info("Starting min cut finding")

            logging.info(f"Scanning {self.num_edges} edges for cuts")
            for edge in self.edges:
                # In the end, if two nodes are not into the same set, means that they
                # belong to different sets(groups)
                if union_find.find(edge[0]) != union_find.find(edge[1]):
                    cut_edges.append(edge)
                    # Hook for visualization / user feedback on found cuts
                    self.viz_cut_found_hook(edge[0], edge[1])

                    min_cut_edge += 1

                    if (
                            not self.always_find_all_cuts
                            and min_cut_edge > self.global_min_cut_edge
                    ):
                        logging.info("Count greater than max, breaking.....")
                        consc_gt_min += 1
                        break

            # Run multiples times, update global optimal value
            if min_cut_edge < self.global_min_cut_edge:
                self.best_union_find = union_find
                self.global_min_cut_edge = min_cut_edge
                self.best_cuts = cut_edges
                consc_gt_min = 0
            else:
                consc_gt_min += 1

            logging.info(f"Global min cut edge is now: {self.global_min_cut_edge},"
                         f" run found {min_cut_edge}")
            run += 1

            if self.global_min_cut_edge == 0:
                logging.info("Global min cut is 0, disconnected graphs found")
                break

            if (
                    self.max_consecutive_mins is not None
                    and consc_gt_min >= self.max_consecutive_mins
            ):
                logging.info(f"Max consecutive mins reached {consc_gt_min}, stopping")

        return self.global_min_cut_edge, self.best_cuts, self.best_union_find

    def viz_contract_nodes_hook(self, node_one, node_two):
        """

        :param node_one:
        :param node_two:
        :return:
        """
        # print(f"Contracting vertices {node_one} and {node_two}")

    def viz_cut_found_hook(self, node_one, node_two):
        """

        :param node_one:
        :param node_two:
        :return:
        """
        # print(f"Found 1 cut {node_one} and {node_two}")
